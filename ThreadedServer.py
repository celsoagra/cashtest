import codecs, pickle
import socket
import threading

from Blockchain import Blockchain

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient, args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 2048
        while True:
            try:
                data = client.recv(size)
                if data:
                    transaction = pickle.loads(codecs.decode(data, "base64"))
                    print("received transaction - {}".format(transaction.hash()))
                    Blockchain.getInstance().addTransaction(transaction)
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False