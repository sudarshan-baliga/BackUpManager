import os
import ctypes
import sys
import subprocess
from backupFolder import Backupfolder


def is_admin():
    '''To check if admin(sudo) privilage is given.'''
    if sys.platform == "linux":
        try:
            return os.getuid() == 0
        except:
            return False
    else:
        # for windows
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

def request_admin():
    if sys.platform == "linux":
        res = subprocess.call(["/usr/bin/sudo", "/usr/bin/id"])
    else:
        res = ctypes.windll.shell32.ShellExecuteW( None, "runas", sys.executable, __file__, None, 1)
        if res >= 32:
            exit(0)
        else:
            res = False
    return res

# check if admin permission is given
admin = False
if is_admin():
    admin = True
else:
    # Re-run the program with admin rights
    admin = request_admin()

if admin:
    bc = Backupfolder()
    dirname = os.path.dirname(__file__)
    bc.backup('backupthis')
else:
    print("Please provide admin privilage in order to create symbolic links(shortcuts)")
