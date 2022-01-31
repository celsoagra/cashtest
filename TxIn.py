
import hashlib


class TxIn(object):

    def __init__(self, previousTxOutput, previousOutputIndex, sequence):
        """
            Transaction Input
        """
        self._previousTxOutput = previousTxOutput
        self._outputIndex = int(previousOutputIndex)
        self._sequence = sequence

    def hash(self, ):
        id = "{}{}{}".format(self._previousTxOutput, self._outputIndex, self._sequence)
        return hashlib.sha256(id.encode('utf-8')).hexdigest()

    def setSignature(self, signature):
        self._signature = signature # hash signed by privK + pubK
    
    def getSignature(self):
        return self._signature
    
    def setPubKey(self, pubKey):
        self._pubKey = pubKey
    
    def getPubKey(self):
        return self._pubKey
    
    def getOutputIndex(self) -> int:
        return self._outputIndex
    
    def getPreviousTxOutput(self):
        return self._previousTxOutput
    
    def print(self):
        print("Input {")
        print("    previousTxOutput: {}".format(self._previousTxOutput) )
        print("    outputIndex: {}".format(self._outputIndex) )
        print("    sequence: {}".format(self._sequence) )
        print("    signature: {}".format(str(self._signature)) )
        print("    pubKey: {}".format(str(self._pubKey)) )
        print("}")