from backupFolder import Backupfolder

def backup(src):
    print(src)
    bc = Backupfolder()
    # dirname = os.path.dirname(__file__)
    bc.backup('backupthis')
