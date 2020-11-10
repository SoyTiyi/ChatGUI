import threading
import socket
import argparse
import sys
import os
import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from tkinter.ttk import *
from datetime import datetime
import math
from Crypto.Cipher import XOR
import base64

class Send(threading.Thread):
    def __init__(self,sock,name):
        super().__init__()
        self.sock = sock
        self.name = name

    def decrypt(self, ciphertext):
        keyCipher='notsosecretkey'
        cipher = XOR.new(keyCipher)
        return cipher.decrypt(base64.b64decode(ciphertext))

    def run(self):
        while True:
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]
            if message == 'quit()':
                self.sock.sendall('Server: {} ha dejado el chat'.format(self.name).encode('utf-8'))
                break
            else:
                #print(message)
                self.sock.sendall('{}'.format(self.decrypt(message)).encode('utf-8'))
        self.sock.close()
        os._exit(0)

class Receive(threading.Thread):
    def __init__(self,sock,name):
        super().__init__()
        self.message = None
        self.sock = sock
        self.name = name
        
    def decrypt(self, ciphertext):
        ciphertext=ciphertext.decode('utf-8')
        keyCipher='notsosecretkey'
        cipher = XOR.new(keyCipher)
        return cipher.decrypt(base64.b64decode(ciphertext))

    def run(self):
        while True:
            now = datetime.now()
            message = self.sock.recv(1024)
            print("ESTE ES EL MENSAJE------> "+str(message))
            print("ESTE ES EL MENSAJE DECRYPTADO------> ")
            #print(self.decrypt(str(message)))
            if message: 
                if self.message:
                    self.message.insert(tk.END, str(now) +' '+ str(message))
            else: 
                self.sock.close()
                os._exit(0)

class Client:
    def __init__(self,host,port):
        self.port = port
        self.host = host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.messages = None
        self.msg = None

    def encrypt(self,msg):
        keyCipher='notsosecretkey'
        cipher = XOR.new(keyCipher)
        return base64.b64encode(cipher.encrypt(msg))
    
    

    def start(self):
        self.sock.connect((self.host, self.port))
        now = datetime.now()
        print('Ingresa tu nombre....')
        self.name = input('Nombre: ')
        print('Hola {}!!'.format(self.name))
        send = Send(self.sock, self.name)
        receive = Receive(self.sock, self.name)
        send.start()
        receive.start()
        #self.sock.sendall('Server: {} se ha unido al chat!'.format(self.name).encode('utf-8'))
        return receive

    def send(self, text_input):
        message = text_input.get()
        text_input.delete(0, tk.END)
        now = datetime.now()
        self.messages.insert(tk.END, '{} ~{}: {}'.format(now,self.name, message))
        if message == 'quit()':
            #self.sock.sendall('Server: {} se ha ido del chat'.format(self.name).encode('utf-8'))
            self.sock.close()
            os._exit(0)
        else:
            print("Este es el mensaje sin encriptar ---> "+message)
            self.sock.sendall('{}: {}'.format(self.name, self.encrypt(message)).encode('utf-8'))

def main(host,port):
    client = Client(host,port)
    receive = client.start()
    interfaz = tk.Tk()
    #Tiene que cambiar la direccion de la imagen dependiendo de donde descarguen el repositorio
    interfaz.iconphoto(False, tk.PhotoImage(file='/home/kali/ChatGUI/python.png'))
    interfaz.title("Cripto chat!!!")
    def change_bg():
        interfaz.config(background='red')
    s = ttk.Style()
    s.configure('message.TFrame', bg='black', fg='green')
    frame_mensajes = tk.Frame(master=interfaz)
    frame_mensajes.configure(bg='black')
    frame_mensajes.grid(row=0, column=0, columnspan=3, sticky="nsew")
    container = tk.Frame(master=interfaz, background="#808080")
    interfaz.config(bg='black')
    interfaz.rowconfigure(0,minsize=400, weight=1)
    interfaz.rowconfigure(1, minsize=50, weight=0)
    interfaz.columnconfigure(0, minsize=400, weight=1)
    interfaz.columnconfigure(1, minsize=100, weight=0)
    interfaz.columnconfigure(2, minsize=100, weight=0)
    lista_mensajes = tk.Listbox(master=frame_mensajes, bg='black', fg='green')
    lista_mensajes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    client.messages = lista_mensajes
    receive.message = lista_mensajes
    text_input = tk.Entry(master=container)
    text_input.pack(fill=tk.BOTH, expand=True)
    text_input.bind("<Return>", lambda x: client.send(text_input))
    text_input.insert(0, "")
    btn_send = tk.Button(
        master=interfaz,
        text='Send',
        command=lambda: client.send(text_input),
        bg='green'
    )
    def clearListBox():
        lista_mensajes.delete('0','end')

    clear = tk.Button(
        master=interfaz,
        text='Clear',
        bg='green',
        command = clearListBox
    )

    container.grid(row=1, column=0, padx=10, sticky="ew")
    btn_send.grid(row=1, column=1, pady=10, sticky="nsew")
    clear.grid(row=1, column=2, pady=10, sticky="nsew")
    interfaz.mainloop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chatroom Server')
    parser.add_argument('host', help='Interfaz de escucha')
    args = parser.parse_args()
    main(args.host, 1234)		




				
