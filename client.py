import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog
import time
 
class ChatApp:
    def __init__(self, root, host='localhost', port=12345):
        self.root = root
        self.root.title("P2P Chat")
 
        self.chat_box = scrolledtext.ScrolledText(self.root, state='disabled', wrap=tk.WORD)
        self.chat_box.pack(padx=10, pady=10)
 
        self.message_entry = tk.Entry(self.root)
        self.message_entry.pack(padx=10, pady=5)
 
        self.send_button = tk.Button(self.root, text="Отправить", command=self.send_message)
        self.send_button.pack(padx=10, pady=5)
 
        # Запрос ника у пользователя
        self.nickname = simpledialog.askstring("Ник", "Введите ваш ник:", parent=self.root)
        if not self.nickname:
            self.nickname = "Гость"  # Установка ника по умолчанию
 
        self.host = host
        self.port = port
        self.socket = None
 
        # Запуск потока для подключения к серверу
        self.connect_thread = threading.Thread(target=self.connect_to_server, daemon=True)
        self.connect_thread.start()
 
        # Привязка нажатия клавиши Enter к отправке сообщения
        self.message_entry.bind("<Return>", lambda event: self.send_message())
 
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
 
    def connect_to_server(self):
        while True:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
                self.display_message("Подключено к серверу.")
                self.receive_messages()  # Запускаем получение сообщений после успешного подключения
                break  # Выход из цикла, если подключение успешно
            except ConnectionRefusedError:
                self.display_message("Не удалось подключиться к серверу. Повторная попытка через 1 секунду...")
                time.sleep(1)  # Ждем 1 секунду перед повторной попыткой
 
    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    self.display_message(message)
                else:
                    break
            except:
                self.display_message("Соединение с сервером потеряно. Попытка переподключения...")
                self.connect_to_server()  # Пытаемся переподключиться
                break
 
    def send_message(self):
        message = self.message_entry.get()
        if message:
            full_message = f"{self.nickname}: {message}"
            try:
                self.socket.send(full_message.encode('utf-8'))
                self.display_message(f"Я: {message}")
                self.message_entry.delete(0, tk.END)
            except:
                self.display_message("Ошибка при отправке сообщения.")
 
    def display_message(self, message):
        self.chat_box.config(state='normal')
        self.chat_box.insert(tk.END, message + "\n")
        self.chat_box.config(state='disabled')
        self.chat_box.yview(tk.END)  # Прокрутка вниз
 
    def on_closing(self):
        if self.socket:
            self.socket.close()
        self.root.destroy()
 
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
