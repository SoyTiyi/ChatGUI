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

class Send(threading.Thread):
	def __init__(self,sock,name):
		super().__init__()
		self.sock = sock
		self.name = name

	def run(self):
		while True:
			print('{}: '.format(self.name),end='')
			sys.stdout.flush()
			message = sys.stdin.readline()[:-1]
			if message == 'quit()':
				self.sock.sendall('Server: {} ha dejado el chat'.format(self.name).encode('utf-8'))
				break
			else:
				self.sock.sendall('{}:{}'.format(self.name, message).encode('utf-8'))
		print('\nSaliendo....')
		self.sock.close()
		os._exit(0)

class Receive(threading.Thread):
	def __init__(self,sock,name):
		super().__init__()
		self.message = None
		self.sock = sock
		self.name = name

	def run(self):
		while True:
			now = datetime.now()
			message = self.sock.recv(1024)
			if message: 
				if self.message:
					self.message.insert(tk.END, str(now) +' '+ str(message))					
				print('\r{}\n{}:'.format(message.decode('utf-8'), self.name), end = '')
					
			else: 
				print('\n Oh no, perdimos la conexion con el servidor')
				print('\nSaliendo....')
				self.sock.close()
				os._exit(0)

class Client:
	def __init__(self,host,port):
		self.port = port
		self.host = host
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.name = None
		self.messages = None
	def start(self):
		print('Conectandose a {}:{}...'.format(self.host, self.port))
		self.sock.connect((self.host, self.port))
		now = datetime.now()
		print('Conexion Exitosa a {}:{} a las {}'.format(self.host, self.port, now))
		print('Ingresa tu nombre....')
		self.name = input('Nombre: ')
		print('Hola {}!!'.format(self.name))
		send = Send(self.sock, self.name)
		receive = Receive(self.sock, self.name)
		send.start()
		receive.start()

		self.sock.sendall('Server: {} se ha unido al chat!'.format(self.name).encode('utf-8'))
		print("Para salir escriba quit()")
		print('CriptoChat ~ {}: '.format(self.name), end = '')

		return receive
	def send(self, text_input):
		message = text_input.get()
		text_input.delete(0, tk.END)
		now = datetime.now()
		self.messages.insert(tk.END, '{} ~{}: {}'.format(now,self.name, message))
		if message == 'quit()':
			self.sock.sendall('Server: {} se ha ido del chat'.format(self.name).encode('utf-8'))
			print("\nBYe.....")
			self.sock.close()
			os._exit(0)
		else:
			self.sock.sendall('{}: {}'.format(self.name, message).encode('utf-8'))
		
def main(host,port):

	client = Client(host,port)
	receive = client.start()
	interfaz = tk.Tk()
	interfaz.iconphoto(False, tk.PhotoImage(file='/home/soytiyi/Escritorio/Universidad/chat/python.png'))
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
	#scroll = tk.Scrollbar(master=frame_mensajes,bg='green')
	#scroll.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
	#yscrollcommand=scroll.set
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
	print("Como usar Chatroom >:v")
	print("[*] python/python3 client.py IP")
	print("[*] Si es a nivel local, entonces =>")
	print("                                    [*] python3 client.py localhost")
	main(args.host, 1234)		




				
