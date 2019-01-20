from backupFolder import Backupfolder

def backup():
    bc = Backupfolder()
    # dirname = os.path.dirname(__file__)
    bc.backup('backupthis')
