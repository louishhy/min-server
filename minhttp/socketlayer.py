import socket
from typing import Literal, Optional
import abc
import logging
import ssl

class SocketLayer:
    pass
    

class TCPSocketLayer(SocketLayer):
    def __init__(self, host: str, 
                 port: int, 
                 backlog: Optional[int] = None, 
                 ssl_enabled: bool = False,
                 verbose: bool = True):
        self.host = host
        self.port = port
        self.listening_socket = None
        self.logger = logging.getLogger(self.__class__.__name__)
        # Enabling you to see more details :)
        if verbose:
            self.logger.setLevel(logging.INFO)
        self.ssl_enabled = ssl_enabled
        self._initialize_listening_socket(backlog)
    
    def _initialize_listening_socket(self, backlog):
        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket.bind((self.host, self.port))
        if backlog:
            self.listening_socket.listen(backlog)
        else:
            self.listening_socket.listen()
        
    def start(self):
        while True:
            client_socket, address = self.listening_socket.accept()
            self.logger.info(f"Accepted connection from {address}")
            if self.ssl_enabled:
                self.handle_client_with_ssl(client_socket)
            else:
                self.handle_client(client_socket)
    
    def handle_client(self, client_socket: socket.socket):
        bytesinfo = client_socket.recv(1024)
        # Parse into utf-8 string
        info = bytesinfo.decode("utf-8")
        self.logger.info(f"Received: {info}")
    
    def handle_client_with_ssl(self, client_socket: socket.socket):
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
        context.wrap_socket()