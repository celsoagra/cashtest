import hashlib,binascii,codecs,base58,ecdsa
import hashlib
from TxIn import TxIn
from TxOut import TxOut
from block import Block
from Transaction import Transaction
from wallet import Wallet
import os
import time
import pickle

class Blockchain:
    __instance = None

    @staticmethod 
    def getInstance():
        if Blockchain.__instance == None:
            Blockchain()
        return Blockchain.__instance

    def __init__(self):
        if Blockchain.__instance == None:
            self._transactionPool = {} # memory pool
            Blockchain.__instance = self
    
    def addTransaction(self, transaction : Transaction):
        transaction.print()
        self._transactionPool[transaction.hash()] = transaction
    
    #
    # PRECISA OBTER QUAIS SÃO MEUS HASHES / TX QUE PERTENCEM A MINHA CARTEIRA
    # DEPOIS JUNTAR TUDO E CRIAR NOVAS POSICOES DE UXTO
    # VER ALG DE BALANCE
    #
    def createTransaction(self, wallet : Wallet, value, address) -> Transaction:
        chain = self.getChain()
        lastBlock: Block = chain[-1]

        listTxIn = lastBlock.createTxInFromWallet(wallet, value)
        listTxOut = lastBlock.listUtxos()
        
        filtered = []
        for txin in listTxIn:
            txout = next((tx for tx in listTxOut if tx['txHash'] == txin.getPreviousTxOutput() and tx['index'] == txin.getOutputIndex()), None)
            if (txout != None):
                filtered.append(txout['output'].value())

        leftOver = sum( filtered )
        leftOver = leftOver - value
        txout = TxOut(value, address)
        txoutLeftOver = TxOut(leftOver, wallet.address())

        # 2. prepara o hash e assina o hash
        id = "{}_{}_{} {}".format(address, txout.value(), txout.pubKeyHash(), int(time.time()))
        hash = hashlib.sha256(id.encode('utf-8')).hexdigest()
        
        # cria a transação
        return Transaction(hash, listTxIn, [txout, txoutLeftOver])

    def createCoinbaseTransaction(self, wallet: Wallet, value) -> Transaction:
        # 1. envio de 50 coins da carteira
        txout = TxOut(value, wallet.address())

        # 2. prepara o hash e assina o hash
        id = "{}_{}_{} {}".format(wallet.address(), txout.value(), txout.pubKeyHash(), int(time.time()))
        hash = hashlib.sha256(id.encode('utf-8')).hexdigest()
            
        # prepara a parte a ser desbloqueada
        txin = TxIn("0", 0, 0)
        txin.setSignature(wallet.signature(hash))
        txin.setPubKey(wallet.pubKey())
        
        # cria a transação
        return Transaction(hash, [txin], [txout])


    def balance(self, wallet: Wallet):
        chain = self.getChain()
        lastBlock: Block = chain[-1]
        return lastBlock.balance(wallet)
    
    def createBlock(self):
        chain = self.getChain()
        if (len(self._transactionPool.keys()) == 0):
            return

        previousHash = "0" #genesis
        hashes = [tx.hash() for tx in self._transactionPool.values()]
        transactions = []
        for hash in hashes:
            transactions.append(self._transactionPool.pop(hash)) 

        blockChanged = False
        oldTransactions = []
        if (len(chain) > 0):
            lastBlock: Block = chain[-1]
            previousHash = lastBlock.hash()
            oldTransactions = lastBlock.transactions()
            
            # PERCORRER A LISTA DE TRANSACOES
            # VOU PEGAR O TXIN
            # REMOVER O TXOUT REFERENTE A ESTE TXIN E ADD O NOVO TXOUT
            
            for transaction in transactions: # TRANSACOES PROVENIENTES DA MEMORY POOL
                skipTransaction = False

                for txin in transaction.listTxInput(): # obtem a lista de entrada / desbloqueantes


                    # obtem a entrada referente ao hash da antiga transacao
                    txFounded = next((tx for tx in oldTransactions if tx.hash().__eq__(txin.getPreviousTxOutput()) ), None)

                    # Se for None, desconsidera. Significa que esta transação é invalida
                    listTxOutput = None if txFounded is None else txFounded.listTxOutput()
                    if (listTxOutput is None or listTxOutput[ txin.getOutputIndex() ] is None or self.isOperationValid(txin, listTxOutput[ txin.getOutputIndex() ]) is False):
                        skipTransaction = True
                        break
                    
                    txFounded.listTxOutput()[txin.getOutputIndex()] = None                
                if (skipTransaction is False): # pula a transacao se ela for errada
                    oldTransactions.append(transaction)
                    blockChanged = True
                
        else:
            for transaction in transactions: # ADDED GENESIS
                oldTransactions.append(transaction)
            blockChanged = True

        if (not blockChanged): return

        # Add coinbase
        wallet = Wallet()
        oldTransactions.append( self.createCoinbaseTransaction(wallet, 50) )

        block = Block(previousHash, oldTransactions)
        block.print()
        self.saveOnChain(block)
        #self._chain.append(block) # COMPARTILHAR VIA ARQUIVO DAT / PICKLE

    # VALIDAR GENESIS BLOCK, VALIDAR SE POSSUI RECURSOS,
    # O SOMATORIO DO TXIN/TXOUT PRECISA SER VALIDADE PRA QUE A PESSOA POSSUA DINHEIRO
    def isOperationValid(self, txIn: TxIn, txOut: TxOut):
        txInAddress = self.genAddress(txIn.getPubKey()).decode('utf8')
        if (txInAddress != txOut.pubKeyHash()):
            return False
        

    def genAddress(self, pubKey):
        ecdsaPublicKey = '04' + pubKey
        hash256FromECDSAPublicKey = hashlib.sha256(binascii.unhexlify(ecdsaPublicKey)).hexdigest()
        ridemp160FromHash256 = hashlib.new('ripemd160', binascii.unhexlify(hash256FromECDSAPublicKey))
        prependNetworkByte = '00' + ridemp160FromHash256.hexdigest()
        hash = prependNetworkByte
        for x in range(1,3):
            hash = hashlib.sha256(binascii.unhexlify(hash)).hexdigest()
        cheksum = hash[:8]
        appendChecksum = prependNetworkByte + cheksum
        return base58.b58encode(binascii.unhexlify(appendChecksum))

    def getChain(self):
        chain = []
        if (os.path.exists("./chain.dat")):
            fp = open("chain.dat", 'rb')
            chain = pickle.load(fp)
            fp.close()
        return chain
    
    def saveOnChain(self, block):
        chain = self.getChain()
        chain.append(block)
        fp = open("./chain.dat","wb+")
        pickle.dump(chain, fp)
        fp.close()