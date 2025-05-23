import socket
import threading # For handling multiple clients
from datetime import datetime # For timestamping messages

# This is a simple server that listens for incoming connections and can handle multiple clients.
HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Socket for IPv4 and TCP
server_socket.bind((HOST, PORT))    # Tells the OS to listen on the specified host and port
server_socket.listen()
print(f"Server listening on {HOST}:{PORT}")

clients = []  # List to keep track of connected clients
usernames = {}  # Dictionary to map client sockets to usernames

def handle_client(client_socket, addr):
    try:
        username = client_socket.recv(1024).decode()
        usernames[client_socket] = username
        print(f"{username} connected from {addr}")

        current_users = [usernames[c] for c in clients if c != client_socket]
        if current_users:
            user_list_msg = "People in this room: " + ", ".join(current_users)
            client_socket.sendall(user_list_msg.encode())

        # Notify all clients about the new connection
        join_msg = f"*** {username} has joined the chat! ***"
        for client in clients:
            if client != client_socket:
                client.sendall(join_msg.encode())

        while True:
            msg = client_socket.recv(1024)
            if not msg:
                break
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            full_msg = f"[{timestamp}] {username}: {msg.decode()}"
            for client in clients:
                if client != client_socket:
                    client.sendall(full_msg.encode())
    except ConnectionResetError:
        print(f"Connection reset by {addr}")
    finally:
        # Notify all clients about the disconnection
        if client_socket in clients:
            leave_msg = f"*** [{datetime.now().strftime('%H:%M:%S')}] {usernames[client_socket]} has left the chat! ***"
            for client in clients:
                if client != client_socket:
                    client.sendall(leave_msg.encode())

        client_socket.close()
        clients.remove(client_socket)
        print(f"Connection closed by {addr}")
        if client_socket in usernames:
            del usernames[client_socket]

while True:
    client_socket, addr = server_socket.accept()
    clients.append(client_socket)  # Add the new client to the list
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()  # Start a new thread for the client