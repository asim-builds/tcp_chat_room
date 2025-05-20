import socket

HOST = '127.0.0.1'
PORT = 65432        # The same port as the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")
    while True:
        message = input("You: ")
        if message.lower() == 'exit':
            print("Exiting chat.")
            break
        s.sendall(message.encode())