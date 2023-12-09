import sys
import os
import logging
import socket
import tkinter as tk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import QR_Scan as scan
import retrivedata as check

class CreatedDeletedEventHandler(FileSystemEventHandler):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def on_created(self, event):
        if event.is_directory:
            return
        
        event_type = "file created"
        message = f"{event_type}: {event.src_path}\n"
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)  # Automatically scroll to the bottom

        # Transfer the file over TCP/IP
        self.transfer_file(event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        
        event_type = "file deleted"
        message = f"{event_type}: {event.src_path}\n"
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)  # Automatically scroll to the bottom

    def transfer_file(self, file_path):
        host = '192.168.153.128'  # Replace this with the server's IP address
        port = 12345        # Choose a port number for communication

        # Create a TCP/IP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client_socket.connect((host, port))
            logging.info(f"Connected to server at {host}:{port}")

            # Send the filename to the server
            filename = os.path.basename(file_path)
            client_socket.sendall(filename.encode())

            # Send the file content to the server
            with open(file_path, "rb") as file:
                logging.info(f"Transferring {filename}...")
                while True:
                    data = file.read(1024)
                    if not data:
                        break
                    client_socket.sendall(data)

            logging.info(f"{filename} transferred successfully.")
            message = f"{filename} transferred successfully.\n"
            self.text_widget.insert(tk.END, message)
            self.text_widget.see(tk.END)
        except Exception as e:
            logging.error(f"Error transferring file: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = r'D:\document\95IDEAL\code\QR_Event-main\facepath'

    root = tk.Tk()
    root.title("File System Events Monitor")

    text_widget = tk.Text(root, wrap=tk.WORD, font=("Courier New", 12))
    text_widget.pack(fill=tk.BOTH, expand=True)

    event_handler = CreatedDeletedEventHandler(text_widget)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        root.mainloop()
    finally:
        observer.stop()
        observer.join()