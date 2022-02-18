# Inventory
# A data type identifier and a hash; used to identify transactions and blocks available for download through the Bitcoin P2P network.

# Criação de um map com hash + tipo

from Transaction import Transaction
from block import Block
import pickle
import os

# precisa carregar do chain.dat
class Inventory(object):

    __instance = None

    @staticmethod 
    def getInstance():
        if Inventory.__instance == None:
            Inventory()
        return Inventory.__instance

    def __init__(self):
        if Inventory.__instance == None:
            self._invBlocks = {}
            self._invTx = {}
            self.loadData()
            Inventory.__instance = self
    
    def loadData(self):
        chain = self.getChain()
        lastBlock: Block = chain[-1]
        for block in chain: self.addBlock(block)
        for transaction in lastBlock.transactions(): self.addTx(transaction)

    def getChain(self):
        chain = []
        if (os.path.exists("./chain.dat")):
            fp = open("chain.dat", 'rb')
            chain = pickle.load(fp)
            fp.close()
        return chain

    def addBlock(self, block: Block):
        self._invBlocks[block.hash()] = block
    
    def addTx(self, tx: Transaction):
        self._invTx[tx.hash()] = tx

    def delTx(self, tx: Transaction):
        del self._invTx[tx.hash()]
    
    def delBlock(self, block: Block):
        del self._invBlocks[block.hash()]
    
    def getBlock(self, hash):
        return self._invBlocks[hash]
    
    def getBlockHashes(self):
        return self._invBlocks.keys()
    
    def getTxHashes(self):
        return self._invTx.keys()
    
    def getTx(self, hash):
        return self._invTx[hash]
    
