import socket

HEADER = 64
#The first message the server expects is a 64-byte header that says the length of the rest of the message.
#Doing it this way runs the risk that the header is not as big as the message
PORT = 5050
FORMAT = 'utf-8'

DISCONNECT_MESSAGE = "!disconnect"
#If users do not propperly disconnect by sending this message, the server may keep their connection ope, then they can't reconnect

SERVER = "172.28.210.193"

ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    #Can't send a packet if the message is not bytes.

    msg_length = len(message)
    #The length (in bytes) of the encoded message

    send_length = str(msg_length).encode(FORMAT)
    #the length (in bytes) of the encoded message, itself encoded
    send_length += b' ' * (HEADER - len(send_length))
    # b"" converts a string to bytes, 
    # we're padding the send_length with spaces (in bytes) up to HEADER bytes (64)

    client.send(send_length)

    client.send(message)

send("Hello World!")
send("TEst 2")
send("HELLLLLLLLLO")
send(DISCONNECT_MESSAGE)

    
