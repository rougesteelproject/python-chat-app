import socket
import threading
import traceback

SERVER = "172.28.210.193"
PORT = 5050

FORMAT = 'utf-8'

DISCONNECT_MESSAGE = "!disconnect"
#If users do not propperly disconnect by sending this message, the server may keep their connection ope, then they can't reconnect
SET_NICKNAME_MESSAGE = "!nick"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#SOCK_STREAM is TCP
client.connect((SERVER, PORT))

def set_nickname():
    nickname = input("Choose a nickname: ")
    return nickname

def recieve():
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            if message == SET_NICKNAME_MESSAGE:
                #GET AND SEND NICKNAME
                client.send(set_nickname())
            else:
                print(message)
        except:
            traceback.print_exception()
            client.close()
            break

def write():
    while True:
        message = f"{input('')}"
        client.send(message.encode(FORMAT))

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()