# CP372-Assignment-1
Requirements:
1. Design a client-server communication application (chatting application between clients and the server).

2. Clients and the server are to communicate using TCP sockets ONLY. You will launch only one
server, with as many clients as the server can serve.

3. Once created, clients are assigned a name in the form of [“Client” + incremental number starting with
1]. That is, the first client is “Client01”, the second client is “Client02”, and so on.

4. Once a connection is accepted, the client will communicate its name to the server.

5. The server will maintain an in-memory cache of accepted clients during the current session, along with 2 of 3 the date and time the connection was accepted, and the date and time the connection was finished.
Cache will be only in memory, no need to use files for cache.


7. Points 3 and 6 are easier to implement on the server side, but you can implement them on both sides if
desired.

8. Once connected and after sending its name to the server, a client can send any string using CLI
(Command Line Interface). The server on the other side should echo the same string back, appending
the word “ACK”.

9. A client can send a message “status” to the server to ask the server for the content of the cache. The
server prints the content of the cache in response.

10. Once a client finishes sending messages, it can send an “exit” message to terminate the connection.
Upon receiving a connection closure request, the server should close the connection to free resources
for other clients.

11. Bonus: the server will have a repository of files. After accepting the client’s connection, the client sends
a “list” message to the server. The server should then reply with the list of files in its repository. The
client can then request a file by name, and the server should stream the file to the client. You should
handle all cases, like when a file name doesn’t exist