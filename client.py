import socket
import threading
import tkinter as tk

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_server():
    try:
        client_socket.connect(('127.0.0.1', 12345))
        chat_log.insert(tk.END, "Connected to the server!\n")
        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.start()
    except ConnectionRefusedError:
        chat_log.insert(tk.END, "Failed to connect. Start the server first!\n")

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            chat_log.insert(tk.END, f"Server: {message}\n")
        except:
            break

def send_message():
    message = message_entry.get()
    if message:
        client_socket.sendall(message.encode())
        chat_log.insert(tk.END, f"You: {message}\n")
        message_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Client Chat")

chat_log = tk.Text(root)
chat_log.pack()

message_entry = tk.Entry(root)
message_entry.pack()

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

connect_thread = threading.Thread(target=connect_to_server, daemon=True)
connect_thread.start()

root.mainloop()
