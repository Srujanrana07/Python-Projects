import socket
import threading

HOST = '127.0.0.1'
PORT = 55555


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

clients = []


def broadcast(message):
    for client in clients:
        client.send(message)

# Handle client connections
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            
            clients.remove(client)
            client.close()
            break


def start_server():
    server.listen()
    print(f"Server is listening on {HOST}:{PORT}")
    while True:
        client, address = server.accept()
        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

start_server()
