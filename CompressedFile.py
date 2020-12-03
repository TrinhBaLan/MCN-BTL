class CompressedFile:
    """
    Basic compressed file structure
    """
    def __init__(self, header, data):
        self.header = header
        self.data = data


