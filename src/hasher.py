import hashlib

class Hasher():
    def __init__(self):
        self.hash = hashlib.sha256()
    def findhash(self,fielename):
        """find the hash of files taking 4094 bytes at a time"""
        with open(fielename, 'rb') as file:
            chunk = 0
            while chunk != b'':
                chunk = file.read(4094)
                self.hash.update(chunk)
        return self.hash.hexdigest()

