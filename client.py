import threading
import socket
import argparse
import sys
import os
import tkinter as tk


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
			message = self.sock.recv(1024)
			if message: 
				if self.message:
					self.message.insert(tk.END, message)					
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
		print('Conexion Exitosa a {}:{}'.format(self.host, self.port))
		print('Ingresa tu nombre....')
		self.name = input('Nombre: ')
		print('Hola {}!!'.format(self.name))
		send = Send(self.sock, self.name)
		receive = Receive(self.sock, self.name)
		send.start()
		receive.start()

		self.sock.sendall('Server: {} se ha unido al chat!'.format(self.name).encode('utf-8'))
		print("Para salir escriba quit()")
		print('{}: '.format(self.name), end = '')

		return receive
	def send(self, text_input):
		message = text_input.get()
		text_input.delete(0, tk.END)
		self.messages.insert(tk.END, '{}: {}'.format(self.name, message))
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
	principal_frame = tk.Tk()
	principal_frame.iconbitmap('/python.png')
	principal_frame.title('Crypto Chat!!!!')
	
	second_frame = tk.Frame(master = principal_frame, bg="black", fg="green")
	scroll = tk.Scrollbar(master = second_frame )
	messages = tk.Listbox(master=second_frame, yscrollcommand=scroll.set)
	messages.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
	scroll.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
	client.messages = messages
	receive.message = messages
	second_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
	frm_entry = tk.Frame(master=principal_frame)
	text_input = tk.Entry(master=frm_entry)
	text_input.pack(fill=tk.BOTH, expand=True)
	text_input.bind("<Return>", lambda x: client.send(text_input))
	text_input.insert(0, "")
	btn_send = tk.Button(
        master=principal_frame,
        text='Send',
        command=lambda: client.send(text_input)
    )
    # This button was create to clear the chat, create a method in the client class that clean the messages list
    btn_clear = tk.Buttin(
    	master=principal_frame,
    	text='Clear')
	frm_entry.grid(row=1, column=0, padx=10, sticky="ew")
	btn_send.grid(row=1, column=1, pady=10, sticky="ew")
	principal_frame.rowconfigure(0, minsize=500, weight=1)
	principal_frame.rowconfigure(1, minsize=50, weight=0)
	principal_frame.columnconfigure(0, minsize=500, weight=1)
	principal_frame.columnconfigure(1, minsize=200, weight=0)
	principal_frame.mainloop()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Chatroom Server')
	parser.add_argument('host', help='Interfaz de escucha')
	args = parser.parse_args()
	if(len(args)==1){
		main(args.host, 1234)		
	}
	else{
		print("Como usar Chatroom >:v")
		print("[*] python/python3 client.py IP")
		print("[*] Si es a nivel local, entonces =>")
		print("                                    [*] python3 client.py localhost")
	}




				
