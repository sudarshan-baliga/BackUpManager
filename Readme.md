# BackUpManager
This program allows the user to backup his files.
<br>How To run:
<br> &nbsp; Linux: <code> python3 /src/manager.py </code>
&nbsp; windows: <code> python /src/manager.py </code>
<br> The files in the "backupthis" folder is backed up in "backup" folder. Also symbolic links of identical files are created.(check the size of the backup and backupthis folder)
<br>Features:
1) Only creates a backup of the modified files (using SHA256 hash).
2) Hashes are stored in sqlite3 database to speed up the process.
3) Creates symbolic links when the similar file already exists in backup

<br> Issues:
1) When a file changes and it is backed up once again all the symbolic link pointing to it will be pointing to the new file even though they are not changed.