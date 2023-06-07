import socket
import threading
import datetime


class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_sockets = []
        self.lock = threading.Lock()

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Server chat telah dimulai.")
        print("Menunggu koneksi dari client...")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print("Koneksi baru diterima dari:", client_address)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        with self.lock:
            self.client_sockets.append(client_socket)

        username = client_socket.recv(1024).decode()
        print("User", username, "telah bergabung ke dalam chat.")

        while True:
            message = client_socket.recv(1024).decode()
            if message:
                print("Pesan diterima dari", username + ":", message)
                self.save_chat_history(f"{username}: {message}")

                with self.lock:
                    for client in self.client_sockets:
                        client.send(f"{username}: {message}".encode())

                # Jika pesan dari client adalah ":q", keluar dari loop
                if message == ":q":
                    break

        with self.lock:
            self.client_sockets.remove(client_socket)
        print("User", username, "telah meninggalkan chat.")
        client_socket.close()

    def save_chat_history(self, message):
        with open("chat_history.txt", "a") as file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp}: {message}\n")


server = ChatServer("192.168.175.131", 8765)
server.start()
