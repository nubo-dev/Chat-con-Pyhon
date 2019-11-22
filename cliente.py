import socket
import threading
import sys
import pickle
import os

class Cliente():

    """
    [Conectará con el servidor]
    """

    def __init__(self, host="localhost", port=9999):

        # Variable que almacenará el socket.
        # # Parametros=Familia de los sockets, tipo(TCP)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conectar al servidor
        self.sock.connect((str(host), int(port)))

        # Mensajes recibidos
        msg_recv = threading.Thread(target=self.msg_recv)
        msg_recv.daemon = True
        msg_recv.start()

        while True:
            msgs = input("")
            if msgs != 'salir':
                self.send_msg(msgs)
            else:
                self.sock.close()
                sys.exit()

    def msg_recv(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if data:
                    # deserializar el mensaje
                    print("{} dice: {}".format(os.environ.get('USER'),pickle.loads(data)))
            except:
                pass

    def send_msg(self, msg):
        self.sock.send(pickle.dumps(msg))


cliente = Cliente("", 9999)
