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
    print(Inventory.getInstance.getBlockHashes())
    print(Inventory.getInstance.getTxHashes())

if __name__ == "__main__":
    main()
