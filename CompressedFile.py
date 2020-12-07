from enum import Enum

class CompressedFile:
    """
    Basic compressed file structure
    """
    def __init__(self, header, data):
        self.header = header
        self.data = data

class Type(Enum):
    DCT = 1
    MDCT = 2