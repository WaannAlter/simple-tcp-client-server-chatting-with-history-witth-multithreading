import socket
import threading
import datetime


class ChatClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None
        self.username = ""

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))

    def send_message(self, message):
        self.client_socket.send(message.encode())

    def receive_message(self):
        return self.client_socket.recv(1024).decode()

    def save_chat_history(self, message):
        with open("chat_history.txt", "a") as file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp}: {message}\n")

    def start_chat(self):
        self.username = input("Masukkan username Anda: ")
        self.send_message(self.username)

        threading.Thread(target=self.receive_messages).start()

        menu_active = True
        while menu_active:
            print("\nMenu Pilihan:")
            print("1. Aplikasi chatting")
            print("2. Melihat percakapan sebelumnya")
            print("3. Hapus history")
            choice = input("Pilih menu: ")

            if choice == "1":
                while True:
                    if self.username:
                        message_prompt = "pesan anda: "
                    else:
                        message_prompt = ""

                    message = input(message_prompt)
                    if message == ":q":
                        break
                    self.send_message(message)
                    self.save_chat_history(f"{self.username}: {message}")

                confirm = input("Kembali ke menu? (y/n): ")
                if confirm.lower() != "y":
                    menu_active = False

            elif choice == "2":
                self.show_chat_history()
            elif choice == "3":
                self.clear_chat_history()
            else:
                print("Menu tidak valid. Silakan pilih menu yang sesuai.")

            confirm = input("Apakah ingin kembali ke menu? (y/n): ")
            if confirm.lower() != "y":
                menu_active = False

    def receive_messages(self):
     while True:
        message = self.receive_message()
        if message:
            if self.username:
                sender_username, received_message = message.split(":", 1)
                sender_username = sender_username.strip()
                if sender_username == self.username:
                    print(f"pesan anda: {received_message.strip()}")
                else:
                    print(f"{sender_username}: {received_message.strip()}")
            else:
                print(f"pesan anda: {message.strip()}")

    def show_chat_history(self):
        with open("chat_history.txt", "r") as file:
            print("\nPercakapan Sebelumnya:")
            print(file.read())

    def clear_chat_history(self):
        with open("chat_history.txt", "w") as file:
            file.write("")
        print("\nHistory chat telah dihapus.")


client = ChatClient("192.168.175.131", 8765)
client.connect_to_server()
client.start_chat()
