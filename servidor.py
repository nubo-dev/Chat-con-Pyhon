#!/usr/bin/env python3
import socket
import threading
import sys

'''
Un socket (enchufe), es un método para la comunicación entre un programa del cliente y un programa del servidor en una red, se define, por tanto, como el punto final en una conexión.

Un socket queda definido por un par de direcciones IP local y remota, un protocolo de transporte y un par de números de puerto local y remoto.
'''

class Servidor():

    """
    [Servidor]
    """
    host = "localhost"  # 127.0.0.1
    port = 9999

    def __init__(self, host=host, port=port):
    
    	# ------- Configuración del socket ---------------
        self.clients = [] # cantidad de clientes
        '''
        Bien, dentro de la librería, hay una clase llamada socket. En ella, nosotros seleccionaremos los parametros para crear un socket bajo el protocolo TCP/IP.
        '''
        # variable que servirá como socket.
        # socket.AF_INET es el domino del conector. En este caso, un conector IPv4
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Asignación del puerto y la ip
        self.sock.bind((str(host), int(port)))
        
        # Cantidad de entidades a escuchar
        self.sock.listen(10)
        
        # Interacción entre clientes.
        self.sock.setblocking(False)

        # Hilos
        accept = threading.Thread(target=self.accept_connection)
        proccess = threading.Thread(target=self.proccess_connection)

        accept.daemon = True
        accept.start()
        proccess.daemon = True
        proccess.start()

        print("Servidor escuchando en el puerto: {}.".format(port))

	# mantiene vivo el hilo principal
        while True:
            msg = input('Escriba [salir], para parar el servidor.\n\n')
            if msg == 'salir':
                self.sock.close()
                sys.exit()
            else:
                pass # No hará nada, mantendrá el hilo vivo

    #Manejará el envío de mensajes a los demás clientes conectados, recorre los clientes, por cada clientes se validará que no envíe el mismo mensaje al mismo cliente
    def msg_to_all(self, msg, cliente):
        for i in self.clients:
            try:
                if i != cliente:
                    i.send(msg)
            except:
                self.clients.remove(i) # remueve el ciente si la conexión esta rota

    def accept_connection(self):
        while True:
            try:
              # conn: cabecera de la conexión del cliente
              # addr: ip y puerto
                conn, addr = self.sock.accept() # que acepte la conexión
                print("Cliente conectado, datos: {}:{}.".format(addr[0], addr[1]))
                conn.setblocking(False) # le decimos que no se bloque
                self.clients.append(conn) # agregar al arreglo de clientes, pasamos coneción
            except:
                pass # si pasa un error, pues que no dé nada

    # Hacer conexiones
    def proccess_connection(self):
        while True:
            if len(self.clients) > 0:
                for i in self.clients:
                    try:
                        data = i.recv(1024)
                        if data:
                            self.msg_to_all(data, i) # mandar a los demás clientes, válidar los mensajes y reenviar
                    except:
                        pass

server = Servidor('', 9999)
