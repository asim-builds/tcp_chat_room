import socket
import threading # For handling multiple clients

# This is a simple server that listens for incoming connections and can handle multiple clients.
HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Socket for IPv4 and TCP
server_socket.bind((HOST, PORT))    # Tells the OS to listen on the specified host and port
server_socket.listen()
print(f"Server listening on {HOST}:{PORT}")

clients = []  # List to keep track of connected clients

def handle_client(client_socket, addr):
    print(f"Connected by {addr}")
    while True:
        try:
            msg = client_socket.recv(1024)  # Buffer size is 1024 bytes
            if not msg:
                break  # No message means the client has closed the connection
            # Broadcast the message to all clients
            for client in clients:
                if client != client_socket:  # Don't send the message back to the sender
                    client.sendall(msg)
        except ConnectionResetError:
            print(f"Connection reset by {addr}")
            break
    client_socket.close()
    clients.remove(client_socket)
    print(f"Connection closed by {addr}")

while True:
    client_socket, addr = server_socket.accept()
    clients.append(client_socket)  # Add the new client to the list
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()  # Start a new thread for the client