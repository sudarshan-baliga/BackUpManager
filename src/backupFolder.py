from hasher import Hasher
import os
import shutil
import sqlite3
import logging


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
        except Exception as e:
            print("could not copy {} into backup folder".format(filepath))
            logging.error(e)
        return False

    def createsymlink(self, src, dest):
        """create symlink of src pointing to dest."""
        print(src, dest)
        try:
            path, file = os.path.split(dest)
            os.makedirs(path, exist_ok=True)
            # src should be absolute path
            os.symlink(src, dest)
        except Exception as e:
            logging.error(e)


    def cleardb(self):
        """Drop the hashes table from sqlite3 db."""
        try:
            db = sqlite3.connect("backup.db")
            cursor = db.cursor()
            query = "DROP table hashes"
            cursor.execute(query)
        except Exception as e:
            print("coulld not drop table hashes")
            logging.error(e)

    def backup(self, fullpath):
        """Backup everthing present in the path."""
        self.cleardb()
        hasher = Hasher()
        try:
            db = sqlite3.connect('backup.db')
            cursor = db.cursor()
            createtable = "CREATE TABLE IF NOT EXISTS hashes(hash TEXT PRIMART KEY NOT NULL, dir TEXT NOT NULL)"
            cursor.execute(createtable)
            db.commit()
        except Exception as e: 
            db.rollback()
            print("Could not create or connect to the database")
            logging.error(e)
        self.listnesteddir(fullpath)
        for file in self.files:
            hash = hasher.findhash(file)
            query = "SELECT * FROM hashes WHERE hash = \'{}\';".format(hash)
            try:
                cursor.execute(query)
            except Exception as e:
                print("not able to query database to check the hashes", e.__doc__)
            identicalrow = cursor.fetchall()
            if len(identicalrow) == 0:
                res = self.copyfile(file)
                if res:
                    try:
                        destpath = os.path.join(os.path.abspath("backup"), file)
                        query = "INSERT into hashes values(\'{}\',\'{}\')".format(hash, destpath)
                        cursor.execute(query)
                        db.commit()
                    except Exception as ee:
                        db.rollback()
                        print("could no insert {} into data base".format(file))
                        logging.error(e)
            else:
                if os.path.exists(os.path.join("backup", file)):
                    print("no changes made for", file)
                else:
                    src = identicalrow[0][1]
                    dest = os.path.join("backup", file)
                    self.createsymlink(src, dest)
