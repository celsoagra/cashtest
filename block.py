import hashlib
import time
from itertools import chain
from TxIn import TxIn

from wallet import Wallet

class Block(object):
    def __init__(self, hashPrevBlock, transactions):
        """
           Block
        """
        self._hashPrevBlock = hashPrevBlock
        self._timestamp = int(time.time())
        #self._transactionsOnDisk = transactionsOnDisk # vector<CTransaction> vtx;
        self._transactionsOnMemory = transactions # mutable vector<uint256> vMerkleTree;
        self._hashMerkleRoot = self._merkle([txs.hash() for txs in transactions])
        self._hash = self.calculateHash()

    def transactions(self):
        return self._transactionsOnMemory

    def print(self):
        print("Block {")
        print("    hash: {}".format(self._hash) )
        print("    hashMerkleRoot: {}".format(self._hashMerkleRoot) )
        print("    timestamp: {}".format(self._timestamp) )
        print("    hashPrevBlock: {}".format(self._hashPrevBlock) )
        print("    list transactions ( {} ): [".format(len(self._transactionsOnMemory)) )
        for transaction in self._transactionsOnMemory:
            transaction.print()
        print("    ]")
        print("}")

    def printSimple(self):
        print("block [ hash: {} ; hashMerkleRoot: {}, timestamp: {}, hashPrevBlock: {}, {} transactions]".format(self._hash, self._hashMerkleRoot, self._timestamp, self._hashPrevBlock, len(self._transactionsOnMemory)) )

    def calculateHash(self):
        """ index +_timestamp + nonce + _hashPrevBlock """
        id = "{}{}{}".format(self._timestamp, self._hashPrevBlock, self._hashMerkleRoot)
        return hashlib.sha256(id.encode('utf-8')).hexdigest()
    
    def hash(self):
        return self._hash

    def listUtxos(self):
        mapOutput = {txs.hash() : txs.listTxOutput() for txs in self._transactionsOnMemory}
        listOutput = []
        for key, val in mapOutput.items():
            listOutput.append( [ dict(txHash=key, output=output, index=index) for index, output in enumerate(val) if output != None ] )
        listOutputTotal = list(chain(*listOutput))
        return listOutputTotal
    
    def createTxInFromWallet(self, wallet : Wallet, totalToSpend):
        utxos = self.listUtxos()
        listTxIn = []
        total = 0.0
        for utxo in utxos:
            if(utxo['output'].pubKeyHash() == wallet.address()):
                total += utxo['output'].value()
                txIn = TxIn(previousOutputIndex=utxo['index'], previousTxOutput=utxo['txHash'], sequence=0)
                txIn.setSignature(wallet.signature(txIn.hash()))
                txIn.setPubKey(wallet.pubKey())
                listTxIn.append(txIn)

                if (total > totalToSpend):
                    break
        return listTxIn

    
    def balance(self, wallet: Wallet):
        listUtxos = self.listUtxos()
        total = 0.0
        for utxo in listUtxos:
            if(utxo['output'].pubKeyHash() == wallet.address()):
                total = total + utxo['output'].value()
        return total
    
    def validateBlock(self):
        """ verifica se a geração do hash está correta """

    # https://stackoverflow.com/questions/61738723/code-to-compute-the-merkle-root-for-the-block
    # https://stackoverflow.com/questions/67355203/how-to-improve-the-speed-of-merkle-root-calculation
    def _merkle(self, hashList):
        if len(hashList) == 0:
            return None
        elif len(hashList) == 1:
            return hashList[0]

        newHashList = []
        # Process pairs. For odd length, the last is skipped
        for i in range(0, len(hashList)-1, 2):
            newHashList.append(self._hash2(hashList[i], hashList[i+1]).hex())
        if len(hashList) % 2 == 1: # odd, hash last item twice
            newHashList.append(self._hash2(hashList[-1], hashList[-1]).hex())
        return self._merkle(newHashList)

    def _hash2(self, a, b):
        # Reverse inputs before and after hashing
        # due to big-endian / little-endian nonsense
        a1 = a[::-1]
        b1 = b[::-1]
        
        contcat = a1+b1
                
        h = hashlib.sha256(hashlib.sha256(b"concat").digest()).digest()
        return h

    #def _verifyHash(self, hash):
        

