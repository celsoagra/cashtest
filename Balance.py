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
    """
        Deve conter lógica do merkletree, garantindo a lista principal e as demais candidatas
    """
    wallet = Wallet()

    # NAO OBTEM A MESMA BLOCKCHAIN. PRECISA SE COMUNICAR POR OUTRO CAMINHO
    blockchain = Blockchain.getInstance()
    
    print("balance: {}".format(blockchain.balance(wallet)))

if __name__ == "__main__":
    main()
