import logging
import socket

from minhttp.middleware import MiddlewareManager
from minhttp.request import HTTPRequest
from minhttp.response import HTTPResponse
from minhttp.router import Router
from minhttp.socketreader import SocketReader
from minhttp.utils import internal_error_response

logging.basicConfig(level=logging.INFO)


class MinHTTPServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        # SSL Related settings
        self.logger = logging.Logger(self.__class__.__name__)
        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket.bind((self.host, self.port))
        self.listening_socket.listen()
        self.middleware_manager = MiddlewareManager()
        self.router = Router()

    def run(self):
        logging.info(f"Starting server on {self.host}:{self.port}...")
        while True:
            self._main_loop()

    def _main_loop(self):
        try:
            connection, client_address = self.listening_socket.accept()
            logging.info(f"Accepted connection from {client_address}")
            self._handle_connection(connection, client_address)
        except KeyboardInterrupt:
            self._shutdown()
        except Exception:
            self._internal_error_handler(connection)
            raise
            

    def _handle_connection(self, connection: socket.socket, client_address: tuple):
        logging.info(f"Handling connection from {client_address}")
        # Read the raw payload string
        string_payload: str = SocketReader.read_utf8_string_from_socket(connection)
        # Parse the string into an HTTPRequest object
        request: HTTPRequest = HTTPRequest(string_payload)
        # Run the request through the middleware
        middleware_resp = self.middleware_manager.process_request(request)
        # If a middleware returns a response, indicating short-circuiting and early return
        if middleware_resp and isinstance(middleware_resp, HTTPResponse):
            connection.sendall(str(middleware_resp).encode("utf-8"))
            connection.close()
            return
        # Route the request to a handler
        handler = self.router.route(request)
        # Handle the request and generate a response
        params = request.params
        response: HTTPResponse = handler(request, **params)
        # Run the response through the middleware
        middleware_resp = self.middleware_manager.process_response(response)
        # If a middleware returns a response, indicating short-circuiting and early return
        if middleware_resp and isinstance(middleware_resp, HTTPResponse):
            connection.sendall(str(middleware_resp).encode("utf-8"))
            connection.close()
            return
        # Turn the response into a string
        response_str = str(response)
        # Send the response to the client
        connection.sendall(response_str.encode("utf-8"))
        # Close the connection
        connection.close()

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

    def _shutdown(self):
        self.listening_socket.close()
        logging.info("Server shut down.")

    def _internal_error_handler(self, connection: socket.socket):
        connection.sendall(str(internal_error_response()).encode("utf-8"))
        connection.close()
