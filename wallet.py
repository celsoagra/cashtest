import hashlib,binascii,codecs,base58,ecdsa
import socket,pickle
import threading
from SendedObject import SendedObject

from Transaction import Transaction

class Wallet(object):
    def __init__(self):
        """
            private key
            public key
            address
            https://github.com/burakcanekici/BitcoinAddressGenerator
            https://medium.com/coinmonks/bitcoin-address-generation-on-python-e267df5ff3a3
        """
        self._address = self._generateAddress()

    def _readPEMFile(self, filename):
        dataPem = "";
        with open(filename, 'r') as file:
            dataPem = file.read()
        return dataPem
    
    def _generateAddress(self):
        dataPem = self._readPEMFile('walletkey.pem')
        self._privateKey = ecdsa.SigningKey.from_pem(dataPem)
        self._ecdsaPublicKey = '04' +  self._privateKey.get_verifying_key().to_string().hex()
        
        hash256FromECDSAPublicKey = hashlib.sha256(binascii.unhexlify(self._ecdsaPublicKey)).hexdigest()
        ridemp160FromHash256 = hashlib.new('ripemd160', binascii.unhexlify(hash256FromECDSAPublicKey))
        prependNetworkByte = '00' + ridemp160FromHash256.hexdigest()
        hash = prependNetworkByte
        for x in range(1,3):
            hash = hashlib.sha256(binascii.unhexlify(hash)).hexdigest()
        cheksum = hash[:8]
        appendChecksum = prependNetworkByte + cheksum
        return base58.b58encode(binascii.unhexlify(appendChecksum))

    def _initSocket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def send(self, transaction):
        sendedObject = SendedObject("tx", transaction.hash(), transaction)
        pickledTransaction = codecs.encode(pickle.dumps(sendedObject), "base64").decode()

        self._initSocket()
        self.sock.connect(("localhost", 20000))
        self.sock.send(pickledTransaction.encode())

    def _balance(self):
        """
            show balances
        """
        
        raise AttributeError("Não implementado")

    def address(self):
        """
            show address
        """
        return self._address.decode('utf8')
    
    def pubKey(self):
        """
            show public Key
        """
        return self._privateKey.get_verifying_key().to_string().hex()
    
    def signature(self, hash):
        return self._privateKey.sign(bytes(hash, "utf-8"))


