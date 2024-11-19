import socket
import threading

class ChatServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(10)
        self.clients = []

        print(f"Сервер запущен на {host}:{port}")
        self.accept_connections()

    def accept_connections(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Подключен клиент: {addr}")
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket, addr), daemon=True).start()

    def handle_client(self, client_socket, addr):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"{addr}: {message}")
                    self.broadcast(message, client_socket)
                else:
                    break
            except:
                break
        client_socket.close()
        self.clients.remove(client_socket)
        print(f"Отключен клиент: {addr}")

    def broadcast(self, message, sender_socket):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    client.close()
                    self.clients.remove(client)

if __name__ == "__main__":
    ChatServer()
