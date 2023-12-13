import socket
import threading

# Create a list to store client sockets
clients = []

# Create a socket for the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 1234
server.bind((host, port))
server.listen(5)

print("Server is listening on port", port)

def broadcast_message(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                # Remove the client if unable to send the message
                remove_client(client)

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast_message(message, client_socket)
        except Exception as e:
            print("Error:", str(e))
            remove_client(client_socket)
            break

while True:
    client_socket, client_addr = server.accept()
    print("Accepted connection from", client_addr)
    clients.append(client_socket)
    
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
