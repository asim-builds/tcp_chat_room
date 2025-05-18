import socket

HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Socket for IPv4 and TCP
server_socket.bind((HOST, PORT))    # Tells the OS to listen on the specified host and port
server_socket.listen()
print(f"Server listening on {HOST}:{PORT}")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connected by {addr}")