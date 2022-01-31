from Blockchain import Blockchain
from Transaction import Transaction
from wallet import Wallet

def main():
    wallet = Wallet()
    blockchain = Blockchain.getInstance()
    transaction: Transaction = blockchain.createTransaction(wallet, 40.0, "0x0000")
    wallet.send(transaction)
    
    print("send transaction - {}".format(transaction.hash()))

if __name__ == "__main__":
    main()
