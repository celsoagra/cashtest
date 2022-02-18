from tokenize import String
from typing import Any

class SendedObject(object):
    def __init__(self, type: String, element: Any):
        """
           Block
        """
        self._type = type
        self._element = element
    
    def element(self):
        return self._element
    
    def type(self):
        return self._type
    
