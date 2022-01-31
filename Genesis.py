from Blockchain import Blockchain
from Transaction import Transaction
from wallet import Wallet

def main():
    wallet = Wallet()
    blockchain = Blockchain.getInstance()
    transaction: Transaction = blockchain.createCoinbaseTransaction(wallet, 200)
    wallet.send(transaction)

if __name__ == "__main__":
    main()
