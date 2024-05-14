#!/usr/bin/env python3
import socket
import paramiko
import threading

class SSHServer(paramiko.ServerInterface):
    def check_auth_password(self, username: str, password: str) -> int:
        return paramiko.AUTH_FAILED

def handle_connection(client_socket):
    transport = paramiko.Transport(client_socket) # use this socket connection established to run a ssh server
    # server_key = paramiko.RSAKey.generate(2048) # ssh server needs a key
    server_key = paramiko.RSAKey.from_private_key_file('ssh_key')
    transport.add_server_key(server_key)
    ssh = SSHServer()
    transport.start_server(server=ssh)

def main(): 
    # creating a TCP socket
    # 1st argument means we want it to be IP based socket
    # 2nd argument means we are using TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # at socket level (1st arg), if we close this socket, we dont want the OS to keep listening for packets and instead make it immediately available so we can run it again
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

    # bind the socket, takes tuple (interface it listens on- empty means all interfaces, port number)
    server_socket.bind(('', 2222))

    # once server socket is bound, then we want to listen in on port
    server_socket.listen(223)

    #input() # application is running on port 2222, and is waiting for input
    while True:
        client_socket, client_address = server_socket.accept() # check the queue to see if any socket is trying to connect
        # and establish the connection and return another socket to continue listening
        print(f"Connection from {client_address[0]}: {client_address[1]}")
        # client_socket.send(b"Hello!\n")
        # print(client_socket.recv(256).decode())

        t = threading.Thread(target=handle_connection, args=((client_socket)))
        t.start()

if __name__ == "__main__":
    main()