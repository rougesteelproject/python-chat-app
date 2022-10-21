#Credit to "Python Socket Programming Tutorial" by 'Tech With Tim' on Youtube
#Credit to "Simple TCP Chat Room in Python" by 'NeuralNine' on Youtube

import socket
import threading

#I would tell everyone a UDP joke, but I'm not sure anyone would get it.

FORMAT = 'utf-8'

DISCONNECT_MESSAGE = "!disconnect"
#If users do not propperly disconnect by sending this message, the server may keep their connection ope, then they can't reconnect
SET_NICKNAME_MESSAGE = "!nick"

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#SOCK_STREAM is TCP
server.bind((HOST, PORT))

clients = []
nicknames = []

#TODO store a list of new messages, send to clients

def disconnect_client(client):
    index=clients.index(client)
    clients.remove(client)
    client.close()
    nickname = nicknames[index]
    broadcast(f'[DISCONNECT] {nickname} has left the chat'.encode(FORMAT))
    nicknames.remove(nickname)


def handle_client(client):   
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            #1024 bytes
            #TODO too many bytes?
            if message == DISCONNECT_MESSAGE:
                disconnect_client(client)
                break

            if message == SET_NICKNAME_MESSAGE:
                client.send(SET_NICKNAME_MESSAGE)

            index=clients.index(client)
            nickname = nicknames[index]

            new_message = f'{nickname}: {message}'.encode(FORMAT)
            #adds nicknames to messages so that we don't have to instead /remove/ nicknames from messages
                
            broadcast(new_message)
        except:
            disconnect_client(client)
            break

def recieve_client():
    while True:
        client, address = server.accept()
        #threading opens up a new thread (process) for each client
        print(f"[CONNECTION] connected with {str(address)}")

        client.send(SET_NICKNAME_MESSAGE.encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)
        nicknames.append(nickname)

        clients.append(client)

        print(f"[CONNECTION] nickname of client is {nickname}")

        broadcast(f"{nickname} has joined the chat.".encode(FORMAT))

        client.send("Connected to the server.".encode(FORMAT))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

def start():
    #Listens for new connections
    server.listen()
    print(f"[LISTENING] server is listening on {HOST}")
    recieve_client()

def broadcast(message):
    #TODO this only works on clients who are connected.
    #Clients who are not connected will not see mesages they missed
    for client in clients:
        client.send(message)


print("[STARTING] server is starting...")
start()