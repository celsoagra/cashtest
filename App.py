from Blockchain import Blockchain
from Inventory import Inventory
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
    """
        Deve conter lógica do merkletree, garantindo a lista principal e as demais candidatas
    """
    wallet = Wallet()
    #print(wallet.address())
    #print(wallet.pubKey())

    print("start server")
    threading.Thread(target = _initServer, args = ('localhost', 20000)).start()
    threading.Thread(target = _initMiner).start()
    
    time.sleep(5)
    blockchain = Blockchain.getInstance()
    
    transaction: Transaction = blockchain.createCoinbaseTransaction(wallet, 200)
    print("send transaction - {}".format(transaction.hash()))
    wallet.send(transaction)

    time.sleep(20)
    print("balance: {}".format(blockchain.balance(wallet)))

    transaction: Transaction = blockchain.createTransaction(wallet, 30, "0x000000")
    print("send transaction - {}".format(transaction.hash()))
    wallet.send(transaction)

    transaction: Transaction = blockchain.createTransaction(wallet, 40, "0x000000")
    print("send transaction - {}".format(transaction.hash()))
    wallet.send(transaction)

    time.sleep(20)
    print("balance: {}".format(blockchain.balance(wallet)))
    print(Inventory.getInstance().getBlockHashes())
    print(Inventory.getInstance().getTxHashes())
    
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
