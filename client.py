from msilib.schema import Error
import socket
import threading

import tkinter as tk
import traceback

#Creadit to "Simple GUI Chat in Python" by NeuralNine on youtube

class Client():
    def __init__(self, server, port) -> None:

        self.FORMAT = 'utf-8'

        self.DISCONNECT_MESSAGE = "!disconnect"
        #If users do not propperly disconnect by sending this message, the server may keep their connection ope, then they can't reconnect
        self.SET_NICKNAME_MESSAGE = "!nick"

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #SOCK_STREAM is TCP
        self.sock.connect((server, port))

        self._gui_done = False
        self._running - True

        gui_thread = threading.Thread(target=self.gui_loop)
        gui_thread.start

        recieve_thread = threading.Thread(target=self.recieve)
        recieve_thread.start()

    def recieve(self):
        while True:
            try:
                message = self.sock.recv(1024).decode(self.FORMAT)
                print(message)
                #TODO a debug thing

                if message == self.SET_NICKNAME_MESSAGE:
                    #GET AND SEND NICKNAME
                    self._text_area.insert('end', "Choose a nickname:")

                if self._gui_done:
                    self._text_area.config(state='normal')
                    #Allow changing the text
                    self._text_area.insert('end', message)
                    #Add recieved messages to the end
                    self._text_area.yview('end')
                    #scroll to the end
                    self._text_area.config(state='disabled')

            except ConnectionAbortedError:
                break
            except Error:
                traceback.print_exception()
                self.sock.close()
                break

    def write(self):

        message = self._input_area.get()
        self.sock.send(message.encode(self.FORMAT))
        self._input_area.delete()

        if message == self.DISCONNECT_MESSAGE:
            self.stop()

    def gui_loop(self):
        self.window = tk.Tk()
        self.window.configure(bg="lightgray")

        self._chat_label = tk.Label(self.window, text="Chat", bg="lightgray")
        self._chat_label.pack()

        self._text_area = tk.scrolledtext.ScrolledText(self.window)
        self._text_area.pack()
        self._text_area.confing(state='disabled')
        #Need to set the state to 'default' when making changes.

        self._message_label = tk.Label(self.window, text="message", bg="lightgray")
        self._message_label.pack()

        self._input_area = tk.Text(self.window, height=3)
        self._input_area.pack()

        self._send_button = tk.Button(self.window, text="send", command=self.write)
        self._send_button.pack()

        self._gui_done = True

        self.window.protocol("WM_DELETE_WINDOW", self.stop)

    def stop(self):
        self._running = False
        self.window.destroy()
        self.sock.close()
        exit(0)

SERVER = "172.28.210.193"
PORT = 5050

new_client = Client(SERVER, PORT)