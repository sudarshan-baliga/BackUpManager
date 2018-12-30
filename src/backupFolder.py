from hasher import Hasher
import os
import shutil
import pymysql


class Backupfolder():
    def __init__(self):
        self.files = []

    def listnesteddir(self, fullpath):
        """List all files in directory ans subdirectories."""
        directories = [x[0] for x in os.walk(fullpath)]
        for directory in directories:
            for file in os.listdir(directory):
                absFile = os.path.join(directory, file)
                if os.path.isfile(absFile):
                    self.files.append(absFile)

    def copyfile(self, filepath):
        try:
            path, file = os.path.split(filepath)
            os.makedirs(os.path.join("backup", path), exist_ok=True)
            shutil.copy2(filepath, os.path.join("backup", filepath))
            return True
        except:
            print("could not copy {} into backup folder".format(filepath))
        return False

    def createsymlink(self, src, dest):
        """create symlink of src pointing to dest."""
        print(src, dest)
        try:
            path, file = os.path.split(dest)
            os.makedirs(path, exist_ok=True)
            # src should be absolute path
            print(file)
            os.symlink(src, dest)
        except Exception as e:
            print("could not create symlink", dest)
            print(e.__doc__)

    def backup(self, fullpath):
        """Backup everthing present in the path."""
        hasher = Hasher()
        try:
            db = pymysql.connect("localhost", "sudarshan", "12345", "backup")
            cursor = db.cursor() 
        except:
            print("Could not connect to the database")
        self.listnesteddir(fullpath)
        for file in self.files:
            hash = hasher.findhash(file)
            query = "SELECT * FROM hashes WHERE hash = \'{}\';".format(hash)
            try:
                cursor.execute(query)
            except:
                print("not able to query database to check the hashes")
            if cursor.rowcount == 0:
                res = self.copyfile(file)
                if res:
                    try:
                        destpath = os.path.join(os.path.abspath("backup"), file)
                        query = "INSERT into hashes values(\'{}\',\'{}\')".format(hash, destpath)
                        cursor.execute(query)
                        db.commit()                   
                    except:
                        db.rollback()
                        print("could no insert {} into data base".format(file))
            else:
                if os.path.exists(os.path.join("backup", file)):
                    print("no changes made for", file)
                else:
                    srcdata = cursor.fetchone()
                    src = srcdata[1]
                    dest = os.path.join("backup", file)
                    self.createsymlink(src, dest)
