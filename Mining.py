from Blockchain import Blockchain
from ThreadedServer import ThreadedServer
from Transaction import Transaction
from TxIn import TxIn
from TxOut import TxOut
from block import Block
from wallet import Wallet
import hashlib
import threading
import time

def main():
    wallet = Wallet()

    print("start server")
    threading.Thread(target = _initServer, args = ('localhost', 20000)).start()
    threading.Thread(target = _initMiner).start()
    
    time.sleep(5)
    blockchain = Blockchain.getInstance()
    
def _initServer(host, port):
    ThreadedServer(host, port).listen()

def _initMiner():
    blockchain = Blockchain.getInstance()
    timestamp = int(time.time())
    nextTimestamp = timestamp + 10
    print("{} - next: {}".format(timestamp, nextTimestamp))
    blockchain.createBlock()
    while True:
        timestamp = int(time.time())
        if (timestamp >= nextTimestamp):
            blockchain.createBlock()
            nextTimestamp = timestamp + 10
            print("{} - next: {}".format(timestamp, nextTimestamp))


if __name__ == "__main__":
    main()
