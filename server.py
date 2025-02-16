import socket
import threading
import tkinter as tk

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 12345))
server_socket.listen(1)  # Only allow one client for now

conn, addr = None, None  # Global variable for connection

def accept_client():
    global conn, addr
    conn, addr = server_socket.accept()
    chat_log.insert(tk.END, f"Connected to {addr}\n")
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

def receive_messages():
    while True:
        try:
            message = conn.recv(1024).decode()
            if not message:
                break
            chat_log.insert(tk.END, f"Client: {message}\n")
        except:
            break

def send_message():
    message = message_entry.get()
    if conn:  # Check if client is connected
        conn.sendall(message.encode())
        chat_log.insert(tk.END, f"You: {message}\n")
        message_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Server Chat")

chat_log = tk.Text(root)
chat_log.pack()

message_entry = tk.Entry(root)
message_entry.pack()

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

server_thread = threading.Thread(target=accept_client, daemon=True)
server_thread.start()

root.mainloop()
