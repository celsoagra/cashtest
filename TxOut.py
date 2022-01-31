
class TxOut(object):
    def __init__(self, value, pubKeyHash):
        """
            Transaction Output
        """
        self._value = value
        self._pubKeyHash = pubKeyHash
        self._scriptPubkey = "OP_DUP OP_HASH160 {} OP_EQUALVERIFY OP_CHECKSIG".format(pubKeyHash)
    
    def value(self):
        return self._value
    
    def pubKeyHash(self):
        return self._pubKeyHash
    
    def print(self):
        print("Output {")
        print("    value: {}".format(self._value) )
        print("    pubKeyHash: {}".format(self._pubKeyHash) )
        print("    scriptPubkey: {}".format(self._scriptPubkey) )
        print("}")
