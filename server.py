#Credit to "Python Socket Programming Tutorial" by 'Tech With Tim' on Youtube

import socket
import threading

#I would tell everyone a UDP joke, but I'm not sure anyone would get it.

HEADER = 64
#The first message the server expects is a 64-byte header that says the length of the rest of the message.
#Doing it this way runs the risk that the header is not as big as the message
PORT = 5050
FORMAT = 'utf-8'

DISCONNECT_MESSAGE = "!disconnect"
#If users do not propperly disconnect by sending this message, the server may keep their connection ope, then they can't reconnect

SERVER = socket.gethostbyname(socket.gethostname())



ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    #Handle individual connections, takes a connection, and an address
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        #wait until something is recieved
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            #The most-first-est message the server recieves is blank and is for establishing the connection
            #if msg_length checks the message is not blank
            msg_length = int(msg_length)

            #The first message the server expects is a 64-byte header that says the length of the rest of the message.
            #Doing it this way runs the risk that the header is not as big as the message

            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(f'[DISCONNECT] {addr} disconnected.')

            print(f'[{addr}] {msg}')

    conn.close()

def start():
    #Listens for new connections
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        #threading opens up a new thread (process) for each client
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()