import select
import socket
from typing import Optional


class SocketReader:
    @staticmethod
    def read_bytes_from_socket(sock: socket.socket, bufsize: int = 1024) -> bytes:
        return sock.recv(bufsize)

    @staticmethod
    def read_all_bytes_from_socket(sock: socket.socket, timeout=0) -> bytes:
        data = b""
        while True:
            ready_to_read, _, _ = select.select([sock], [], [], timeout)
            if ready_to_read:
                chunk = sock.recv(1024)
                if not chunk:
                    break
                data += chunk
            else:
                break
        return data

    @staticmethod
    def read_utf8_string_from_socket(
        sock: socket.socket, bufsize: Optional[int] = None
    ) -> str:
        if bufsize:
            return sock.recv(bufsize).decode("utf-8")
        else:
            bytedata = SocketReader.read_all_bytes_from_socket(sock)
            return bytedata.decode("utf-8")
