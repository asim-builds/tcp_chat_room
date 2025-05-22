import socket
import threading

HOST = '127.0.0.1'
PORT = 65432        # The same port as the server

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024)  # Buffer size is 1024 bytes
            if not msg:
                print("Disconnected from server.")
                break  # No message means the server has closed the connection
            print("\r(Friend) " + msg.decode() + "\nYou: ", end="")
        except ConnectionResetError:
            print("Connection reset by server")
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")
    
    # Ask for a username
    username = input("Enter your username: ")
    s.sendall(username.encode()) # Send username to server
    # print("You can start chatting! Type 'exit' to leave the chat.")

    # Start a thread to receive messages
    threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

    while True:
        message = input("You: ")
        if message.lower() == 'exit':
            print("Exiting chat.")
            break
        s.sendall(message.encode())