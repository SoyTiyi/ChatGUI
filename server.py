import threading
import socket
import argparse
import os
import math

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
            print('Conexion aceptada desde {} para {}'.format(sc.getpeername(), sc.getsockname()))
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

            print ("INFORMACION----> "+message)
            if (': ' in message):
                print('{} dice {!r}'.format(self.sockname, message))
                message1=message.split(': ')
                m2=str(message1[1].strip())
                self.server.broadcast(m2, self.sockname)
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
    #parser = argparse.ArgumentParser(description='Chatroom Server')
    #parser.add_argument('host', help='Interface the server listensat')
    #parser.add_argument('-p', metavar='PORT', type=int, default=1234,help='TCP port (default 1234)')
    #args = parser.parse_args()
    server = Server('127.0.0.1', 1234)
    server.start()
    exit = threading.Thread(target = exit, args = (server,))
    exit.start()


