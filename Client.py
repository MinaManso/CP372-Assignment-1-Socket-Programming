import socket

def main():
    host = '127.0.0.1'
    port = 65432

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    welcome_message = client_socket.recv(1024).decode()
    print(welcome_message)

    try:
        while True:
            message = input("Enter message to send or 'exit' to disconnect: ")
            client_socket.sendall(message.encode())
            if message.lower() == 'exit':
                break
            response = client_socket.recv(1024).decode()
            print("Server Response: ", response)
        
    finally:
        client_socket.close()