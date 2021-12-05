import os
import winshell
import shutil

desktop = winshell.desktop()
path = r'C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\'
target = "http://www.google.com/"

with open(path, 'w') as shortcut:

    shortcut.write('[InternetShortcut]\n')
    shortcut.write('URL=%s' % target)
    shortcut.close()
