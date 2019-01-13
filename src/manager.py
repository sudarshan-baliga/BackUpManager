import os
import ctypes, sys
from  backupFolder import Backupfolder

def is_admin():
    '''to check if admin privilage is give'''
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

#check if admin permission is given
admin = False
if is_admin():
    admin = True
else:
    # Re-run the program with admin rights
    res = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    if res >= 32:
       admin = True

if admin:
    bc = Backupfolder()
    dirname = os.path.dirname(__file__)
    bc.backup('backupthis')
else:
    print("Please provide admin privilage in order to create symbolic links(shortcuts)")
