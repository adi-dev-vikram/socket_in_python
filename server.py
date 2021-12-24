import threading 
import socket
import os

host = '127.0.0.1'

port =  55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET is for Ipv4 address networking and 
# The SOCK_STREAM socket type is used for reliable flow-controlled data streams, such as those provided by TCP. UDP, on the other hand, requires a packet-based socket type, SOCK_DGRAM.

server.bind((host,port))

server.listen()

print('Listening at', server.getsockname())

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:

        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nicknames} left the chat!'.encode('ascii'))
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('Adi'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        broadcast(f'{nickname} joined the chart!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))

        thread.start()
        ipt = input('') 
        if ipt == 'q':
            print('Closing all connections...')
            for connection in server.connections:
                connection.sc.close()
            print('Shutting down the server...')
            os._exit(0)

print("Server is listening...")
receive()
            
