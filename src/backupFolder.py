from hasher import Hasher
import os


class Backupfolder():
    def __init__(self):
        self.hasher = Hasher()
        self.files = []
        pass

    def listnesteddir(self, fullpath):
        """List all files in directory ans subdirectories."""
        directories = [x[0] for x in os.walk(fullpath)]
        for directory in directories:
            for file in os.listdir(directory):
                absFile = os.path.join(directory , file)
                if os.path.isfile(absFile):
                    self.files.append(absFile)

    def backup(self, fullpath):
        """Backup everthing present in the path."""
        self.listnesteddir(fullpath)
        print(self.files)
