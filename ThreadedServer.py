import codecs, pickle
import socket
import threading

from Blockchain import Blockchain
from SendedObject import SendedObject

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
                    sendedObject : SendedObject = pickle.loads(codecs.decode(data, "base64"))
                    
                    # Must have a version message before anything else
                    if(sendedObject.type() == "version"):
                        """Primeira mensagem de todas"""
                    if(sendedObject.type() == "tx"):
                        Blockchain.getInstance().addTransaction(sendedObject.element())
                    if(sendedObject.type() == "GetBlocks"):
                        """recebe uma lista de hashes de blocos"""
                    if(sendedObject.type() == "block"):
                        """recebe um bloco minerado"""
                    if(sendedObject.type() == "getData"):
                        """recebe uma solicitacao p enviar algum elemento"""
                    if(sendedObject.type() == "inv"):
                        """recebe um inventario, com blocos e tx"""
                    else:
                        print("descartando pacotes")
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

# Mensagens
# 
# The “block” message transmits a single serialized block
# - Quem recebe a mensagem, envia o bloco
# 
# The “getblocks” message requests an “inv” message that 
# provides block header hashes starting from a particular point in the block chain.
# - Recebe a mensagem de onde até onde deve enviar. Essa mensagem acaba realizando
#   request para mensagem "inv"
# 
# 
# 
# 
# 
# 
# 