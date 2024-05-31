import socket

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 65432)
client_socket.connect(server_address)

try:
    # Send data
    message = "Hello, Server!"
    print(f"Sending: {message}")
    client_socket.sendall(message.encode())

    # Look for the response
    data = client_socket.recv(1024)
    print(f"Received: {data.decode()}")

finally:
    # Close the socket
    client_socket.close()
