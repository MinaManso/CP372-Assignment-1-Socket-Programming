import socket

def main():
    host = '127.0.0.1'
    port = 65432

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))

        # Receive and display the welcome message (client name)
        welcome_message = client_socket.recv(1024).decode()
        print(welcome_message)

        while True:
            message = input("Enter message to send or 'exit' to disconnect: ")
            try:
                client_socket.sendall(message.encode())

                if message.lower() == 'exit':
                    break

                if message.lower() == 'list':  # Request list of files from the server
                    response = client_socket.recv(1024).decode()
                    print("Server Response:\n", response)
                
                elif message.lower().startswith('get '):  # Request a specific file from the server
                    filename = message[4:].strip()
                    client_socket.sendall(message.encode())
                    response = client_socket.recv(1024).decode()
                    print(response)

                    if response.startswith("Streaming file"):
                        with open(f"downloaded_{filename}", 'wb') as f:
                            while True:
                                data = client_socket.recv(1024)
                                if data == b"EOF":  # End of file indicator
                                    break
                                f.write(data)
                        print(f"File {filename} has been downloaded as downloaded_{filename}")

                else:
                    response = client_socket.recv(1024).decode()
                    print("Server Response: ", response)

            except (ConnectionResetError, ConnectionAbortedError) as e:
                print("Connection error: ", e)
                break

    finally:
        client_socket.close()


if __name__ == "__main__":
    main()