import threading 
import socket
import argparse
import os 


class Server(threading.Thread):
	
	def __init__(self, host, port):
			super().__init__()
			self.connections = []
			self.host = host
			self.port = port

	def run(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.bind((self.host, self.port))
		sock.listen(1)
		print('Escuchando en', sock.getsockname())
	
		while True:
			sc, sockname = sock.accept()
			print('Coneccion aceptada desde {} para {}'.format(sc.getpeername(), sc.getsockname()))
			server_socket = ServerSocket(sc, sockname, self)
			server_socket.start()
			self.connections.append(server_socket)
			print('Listo para recibir mensajes desde', sc.getpeername())
	def broadcast(self, message, source):
		for connection in self.connections:
			if connection.sockname != source:
				connection.send(message)
	def remove_connection(self, connection):
		self.connections.remove(connection)

class ServerSocket(threading.Thread):
	def __init__(self, sc, sockname, server):
		super().__init__()
		self.sc = sc
		self.sockname = sockname
		self.server = server
	def run(self):
		while True:
			message = self.sc.recv(1024).decode('utf-8')
			if message:
				print('{} dice {!r}'.format(self.sockname, message))
				self.server.broadcast(message, self.sockname)
			else: 
				print('{} cerró la conección'.format(self.sockname))
				self.sc.close()
				self.server.remove_connection(self)
				return 
	def send(self, message):
		self.sc.sendall(message.encode('utf-8'))
	
	def exit(server):
		while True: 
			inputToFinish = input('')
			if inputToFinish == 'quit()':
				print('Cerrando las conexion ')
				for connection in server.connections:
					connection.sc.close()
				print('Cerrando el programa brox')
				os._exit(0)

	if __name__ == '__main__':
		parser = argparse.ArgumentParser(description='Chatroom Server')
		parser.add_argument('host', help='Interface the server listensat')
		parser.add_argument('-p', metavar='PORT', type=int, default=1234,help='TCP port (default 1234)')
		args = parser.parse_args()
		server = Server(args.host, args.p)
		server.start()
		exit = threading.Thread(target = exit, args = (server,))
		exit.start()






