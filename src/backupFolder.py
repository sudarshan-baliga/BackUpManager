from hasher import Hasher
import os
import pymysql

class Backupfolder():
    def __init__(self):
        self.files = []

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
        db = pymysql.connect("localhost", "sudarshan", "12345", "backup")
        cursor = db.cursor() 
        self.listnesteddir(fullpath)
        for file in self.files:
            # hasher will append the hashes so we need to create
            # new object for every file
            hasher = Hasher()
            hash = hasher.findhash(file)
            query = "SELECT * FROM hashes WHERE hash = \'{}\';".format(hash)
            try:
                cursor.execute(query)
            except:
                print("not able to query database to check the hashes")
            if cursor.rowcount == 0:
                try:
                    query = "INSERT into hashes values(\'{}\',\'{}\')".format(hash, file)
                    cursor.execute(query)
                    db.commit()
                except:
                    db.rollback()
            else:
                print(file , " already exists create symlink")
