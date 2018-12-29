import hasher
import os

hash = hasher.Hasher()
dirname = os.path.dirname(__file__)
print(hash.findhash(os.path.join(dirname, './temp/1.txt')))
