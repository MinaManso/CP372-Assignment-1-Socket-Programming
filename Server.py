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

#global variables
client_count = 0
max_clients = 3
clients_info = {}

def client_thread(conn, addr, client_id):
    global clients_info
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

            else:
                response = f"{data} ACK"
                conn.sendall(response.encode())

        except ConnectionResetError:
            break


    clients_info[client_name]['end_time'] = datetime.datetime.now()
    conn.close()
                

def main():
    host = '127.0.0.1'
    port = 65432
    global client_count

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print("Server is listening for connections")


    while True:
        if client_count < max_clients:
            conn, addr = server_socket.accept()
            client_count += 1
            thread = threading.Thread(target=client_thread, args=(conn, addr, client_count))
            thread.start()
        else:
            print("Max clients reached. Connection rejected")
        
        

