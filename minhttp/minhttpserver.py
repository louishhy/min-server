import socketlayer
import logging

logging.basicConfig(level=logging.INFO)

class MinHTTPServer:
    def __init__(self, host: str, port: int):
        self.socket_layer: socketlayer.SocketLayer = None
        self._initialize_socket_layer(socketlayer.TCPSocketLayer(
            host=host,
            port=port
        ))

    def _initialize_socket_layer(self, socket_layer: socketlayer.SocketLayer):
        self.socket_layer = socket_layer

    def run(self):
        logging.info(
            f"Starting server on {self.socket_layer.host}:{self.socket_layer.port}..."
        )
        self.socket_layer.start()