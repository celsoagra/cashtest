import hashlib

class Transaction(object):
    def __init__(self, hash, vin, vout):
        """
            Transaction
        """
        self._version = "0.0.1"
        self._lockTime = 0
        self._listTxIn = vin
        self._listTxOut = vout
        self._hash = hash
    
    def hash (self):
        return self._hash
    
    def listTxOutput(self):
        return self._listTxOut
    
    def listTxInput(self):
        return self._listTxIn
    
    def print(self):
        print("Transaction {")
        print("    hash: {}".format(self._hash) )
        print("    version: {}".format(self._version) )
        print("    lockTime: {}".format(self._lockTime) )
        print("    list txin: [" )
        if self._listTxIn is not None : [txin.print() for txin in self._listTxIn if txin is not None]
        print("    ]")
        print("    list txout: [" )
        if self._listTxOut is not None : [txout.print() for txout in self._listTxOut if txout is not None]
        print("    ]")
        print("}")
