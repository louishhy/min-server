import socket
from typing import Literal, Optional
import abc
import logging
from concurrent.futures import ThreadPoolExecutor

class SocketLayer:
    pass
    

class TCPSocketLayer(SocketLayer):
    def __init__(self, host: str, port: int, backlog: Optional[int] = None, max_workers: int = 10):
        self.host = host
        self.port = port
        self.listening_socket = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
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
            self.executor.submit(self.handle_client, client_socket)
    
    def handle_client(self, client_socket):
        bytesinfo = client_socket.recv(1024)
        # Parse into utf-8 string
        info = bytesinfo.decode("utf-8")
        self.logger.info(f"Received: {info}")