#server handles multiple client connections
#client data in memory
#Socket Setup
#client handling
#Client data management
#command processing
#connection limits

import socket
import threading
import datetime
import os  # To interact with the file system

# Global variables
client_count = 0
max_clients = 3
clients_info = {}

# Path to the file repository
FILE_REPOSITORY_PATH = './repository'

def client_thread(conn, addr, client_id):
    global clients_info, client_count
    
    client_name = f"Client{client_id:02}"
    conn.sendall(f"Your client name is {client_name}".encode())
    clients_info[client_name] = {"start_time": datetime.datetime.now(), 'end_time': None}

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data or data.lower() == 'exit':
                break

            if data.lower() == 'status':
                status = "\n".join([f"{name}: {info['start_time']} - {info.get('end_time', 'Connected')}" for name, info in clients_info.items()])
                conn.sendall(status.encode())

            elif data.lower() == 'list':  # List all files in the repository
                files = os.listdir(FILE_REPOSITORY_PATH)
                if files:
                    file_list = "\n".join(files)
                    conn.sendall(f"Available files:\n{file_list}".encode())
                else:
                    conn.sendall("No files available in the repository.".encode())

            elif data.lower().startswith('get '):  # Handle file request
                filename = data[4:].strip()  # Extract the file name
                filepath = os.path.join(FILE_REPOSITORY_PATH, filename)

                if os.path.exists(filepath):
                    conn.sendall(f"Streaming file: {filename}".encode())
                    with open(filepath, 'rb') as f:
                        while chunk := f.read(1024):
                            conn.sendall(chunk)
                    conn.sendall(b"EOF")  # Indicate the end of the file
                else:
                    conn.sendall(f"File {filename} not found.".encode())

            else:
                response = f"{data} ACK"
                conn.sendall(response.encode())

        except ConnectionResetError:
            break

    # Handle client disconnection and update client info
    clients_info[client_name]['end_time'] = datetime.datetime.now()
    conn.close()
    client_count -= 1


def main():
    host = '127.0.0.1'
    port = 65432
    global client_count

    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print("Server is listening for connections")

    while True:
        if client_count < max_clients:
            conn, addr = server_socket.accept()  # Accept new client connection
            client_count += 1
            thread = threading.Thread(target=client_thread, args=(conn, addr, client_count))
            thread.start()  # Handle each client in a new thread
        else:
            print("Max clients reached. Connection rejected")


if __name__ == "__main__":
    main()
