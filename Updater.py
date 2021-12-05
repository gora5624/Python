import os
import winshell
import shutil


path = r'{}'.format(
    os.path.expanduser('~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'))
target = os.path.abspath(__file__)
os.symlink(target, r'D:\tmp')
