import hashlib

class Hasher():
    def __init__(self):
        pass
    def findhash(self,fielename):
        """find the hash of files taking 4094 bytes at a time"""
        hash = hashlib.sha256()
        with open(fielename, 'rb') as file:
            chunk = 0
            while chunk != b'':
                chunk = file.read(4094)
                hash.update(chunk)
        return hash.hexdigest()

