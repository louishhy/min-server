import logging
import os
import signal
import socket
import ssl
import threading
from concurrent.futures import ThreadPoolExecutor

import utils
from middleware import MiddlewareManager
from request import HTTPRequest
from response import HTTPResponse
from router import Router
from socketreader import SocketReader

logging.basicConfig(level=logging.INFO)
DEFAULT_CERT_PATH = os.path.join(os.path.dirname(__file__), "cert.pem")
DEFAULT_KEY_PATH = os.path.join(os.path.dirname(__file__), "key.pem")


class MinHTTPServer:
    def __init__(self, host: str, port: int, ssl_enabled: bool = False):
        self.host = host
        self.port = port
        # SSL Related settings
        self.ssl_enabled = ssl_enabled
        if self.ssl_enabled:
            self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.ssl_context.load_cert_chain(
                certfile=DEFAULT_CERT_PATH, keyfile=DEFAULT_KEY_PATH
            )
        self.logger = logging.Logger(self.__class__.__name__)
        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket.bind((self.host, self.port))
        self.listening_socket.listen()
        self.thread_executor = ThreadPoolExecutor(max_workers=5)
        self.middleware_manager = MiddlewareManager()
        self.router = Router()
        self._is_shutting_down = threading.Event()
        signal.signal(signal.SIGINT, self._signal_handler)

    def run(self):
        logging.info(f"Starting server on {self.host}:{self.port}...")
        while not self._is_shutting_down.is_set():
            self._main_loop()

    def _main_loop(self):
        self.listening_socket.settimeout(1)
        try:
            connection, client_address = self.listening_socket.accept()
            logging.info(f"Accepted connection from {client_address}")
            # Wrap the connection with SSL if enabled
            if self.ssl_enabled:
                try:
                    connection = self._create_ssl_socket(connection)
                except ssl.SSLError as e:
                    logging.exception(f"SSL Error: {e}")
                    connection.close()
                    return
            self.thread_executor.submit(
                self._handle_connection, connection, client_address
            )
        except socket.timeout:
            pass

    @utils.log_exceptions
    def _handle_connection(self, connection: socket.socket, client_address: tuple):
        logging.info(f"Handling connection from {client_address}")
        # Read the raw payload string
        string_payload: str = SocketReader.read_utf8_string_from_socket(connection)
        # Parse the string into an HTTPRequest object
        request: HTTPRequest = HTTPRequest(string_payload)
        # Run the request through the middleware
        self.middleware_manager.process_request(request)
        # Route the request to a handler
        handler = self.router.route(request)
        # Handle the request and generate a response
        params = request.params
        response: HTTPResponse = handler(request, **params)
        # Run the response through the middleware
        self.middleware_manager.process_response(response)
        # Turn the response into a string
        response_str = str(response)
        # Send the response to the client
        connection.sendall(response_str.encode("utf-8"))
        # Close the connection
        connection.close()

    def _create_ssl_socket(self, sock: socket.socket) -> ssl.SSLSocket:
        ssl_socket = self.ssl_context.wrap_socket(sock, server_side=True)
        return ssl_socket

    # Decorators that helps with registering middlewares or routes
    def request_middleware(self, func):
        self.middleware_manager.add_request_middleware(func)
        return func

    def response_middleware(self, func):
        self.middleware_manager.add_response_middleware(func)
        return func

    def get(self, path: str):
        def decorator(func):
            self.router.add_route("GET", path, func)
            return func

        return decorator

    def post(self, path: str):
        def decorator(func):
            self.router.add_route("POST", path, func)
            return func

        return decorator

    def shutdown(self):
        self._is_shutting_down.set()
        self.listening_socket.close()
        self.thread_executor.shutdown(cancel_futures=True)
        logging.info("Server shut down.")

    # Signal handler for SIGINT
    def _signal_handler(self, signum, frame):
        logging.info("Shutting down server...")
        self.shutdown()
