# LEARNhoneypot
Learning and understanding how to create a SSH honeypot with python!

### At line 33
**netstat -tnlp | grep 2222** terminal command: 
- _netstat_ provides information about network connections, ports in use, and processes using them
- _-tnlp;_ t: displays TCP sockets, n: ensures numerical addresses are shown instead of resolving hostnames, 
l: lists only listening sockets (those waiting for incoming connections), p: displays process ID and program name associated with each socket

- _grep_ from the output of netstat, grep finds the lines containing the specific pattern, in this case port 2222

**Output from the terminal command**: 
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 0.0.0.0:2222            0.0.0.0:*               LISTEN      8106/python3

**nc 127.0.0.1 2222** terminal command:
- _nc_: netcat, that reads and writes data across network connections using TCP/UDP protocol
- 1st arg is the loopback IP address that points back to the local machine itself (basically refers to current system)
- 2nd arg is the post number that netcat attemps to connect to
- So overall, netcat is establishing a connection to the local machine on port 2222, its as if we are the client.

So at this point we can directly connect and start connection (TCP packet has gone out to port 2222) to socket, but there is nothing to accept the socket.

### From line 34 to 39
When the client (our local machine) is trying to connect (_nc 127.0.0.1 2222_), the server socket accepts connection. Then sends a Hello! message to the client side. So if we open another bash terminal while running the server, we can see that we receive a Hello! and connection is successful.

From client side, if we type something else in the terminal, we will receive it on the server side.

The while loop makes the server to keep listening. 

### Line 3
Since we want to build a ssh server, we cant just use the TCP/IP socket. We can instead pass this to a higher level library, **Paramiko**

### Line 12 and 13
Instead of generating a public key each time, we can use _ssh-keygen_ to generate a key file, and in **Line 30** we gett paramiko to use that key.

### Line 4
This library is to create threads

### Line 41, 42
Rather than waiting for the connection to finish, and thereafter accepting another connection, we start a thread for each established connection to handle the connection, so 2 clients can connect at the same time. 

We have to remember to start the thread. 

_ssh localhost -p 2222_ is the command to connect to the server. 

## How is this a SSH honeypot?
This is a decoy designed to look like a easy target to attackers, so it only baits, but is not the actual production server. 

This code sets up a SSH server on port 2222. When an attacker is trying to connect to the port, it triggers the honeypot. 
1. Server listens on port
2. Handle connection function is invoked when attacker is trying to connect. 
3. Paramiko transport object is created using client socket. 
4. RSA key is associated and the server SSH class is used as server interface. 
5. TRansport starts the SSH server. 
6. Attacker script will think its connected to real SSH server.
7. But this server doesnt authenticate the attacker, returns AUTH failed.
8. Attacker will just be stuck.

[Youtube link] (https://www.youtube.com/watch?v=HO1h57CiF98)