from tokenize import String
from typing import Any


class SendedObject(object):
    def __init__(self, type: String, hash: String, element: Any):
        """
           Block
        """
        self._type = type
        self._element = element
        self._hash = hash

    def hash(self):
        return self._hash
    
    def element(self):
        return self._element
    
    def type(self):
        return self._type
    
