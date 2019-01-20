import os
import ctypes
import sys
import subprocess
import argparse
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
            print('nonono')
            return False


def request_admin():
    if sys.platform == "linux":
        res = subprocess.call(["/usr/bin/sudo", "/usr/bin/id"])
    else:
        res = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, subprocess.list2cmdline(sys.argv), None, 1)
        if res >= 32:
            exit(0)
        else:
            res = False
    return res


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--source", type=str,
                    help="select the source folder")
parser.add_argument("-d", "--destination", type=str,
                    help="select the destination folder")
args = parser.parse_args()


if(args.source == None):
    print("Please provide source directory\nUse --help arg to see the usage")
    exit(1)
elif not os.path.exists(args.source):
    print("source directory {} does not exist".format(args.source))
    exit(1)
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
    bc.backup(args.source)
else:
    print("Please provide admin privilage in order to create symbolic links(shortcuts)")
