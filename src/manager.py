import os
from  backupFolder import Backupfolder

bc = Backupfolder()
dirname = os.path.dirname(__file__)
bc.backup('backupthis')
