import socket

class Server:
    def __init__(self, address, port, backlog=5):
        # Defining a TCP socket
        self.listening_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.listening_socket.bind((address, port))
        self.backlog = backlog
    
    def start(self):
        self.listening_socket.listen(self.backlog)
        while True:
            connection, client_address = self.listening_socket.accept()
    
    def handle(self, connection: socket.socket, client_address: tuple):
        
