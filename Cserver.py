import socket
import threading
import sys
import pickle
import os

class Servidor():
	 	##Pide introducir puerto
	def __init__(self, host=socket.gethostname(), port=input('\nEscriba el puerto \n')):
		self.clientes = []
		self.sock = socket.socket()
		self.sock.bind((str(host), int(port)))
		self.sock.listen(20)
		self.sock.setblocking(False)
		ipB = socket.gethostbyname(host)
		print('Su IP es: ', ipB)

		aceptar = threading.Thread(target=self.aceptarC)
		procesar = threading.Thread(target=self.procesarC)
		
		aceptar.daemon = True
		aceptar.start()

		procesar.daemon = True
		procesar.start()

		while True:
			msg = input('SALIR = Q\n')
			if msg == 'Q':
				print("**** TALOGOOO *****")
				self.sock.close()
				sys.exit()
			else:
				pass

	def broadcast(self, msg, cliente):
		for c in self.clientes:
			try:
				if c != cliente:
					c.send(msg)
			except:
				self.clientes.remove(c)

	def aceptarC(self):
		while True:
			try:
				conn, addr = self.sock.accept()
				print(f"\nConexion aceptada via {adrr}\n") ##Saca Ip de la conexion aceptada
				conn.setblocking(False)
				self.clientes.append(conn)
			except:
				pass

	def procesarC(self):
		print("Procesamiento de mensajes iniciado")
		while True:
			if len(self.clientes) > 0:
				for c in self.clientes:
					try:
						print('Clientes conectados: ', len(self.clientes))
						data = c.recv(32)
						if data:
							self.broadcast(data,c)
					except:
						pass

s = Servidor()