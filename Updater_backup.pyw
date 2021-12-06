import os
from os.path import join as joinpath
import shutil
import time

import subprocess
mainPath = os.path.dirname(os.path.abspath(__file__))
upDateDirPath = r'\\192.168.0.33\shared\_Транзит_\updateSoft\{}'
mode = ''
copyList = []
period_min = 30


def applyConfig():
    with open(joinpath(mainPath, 'configUpdate.txt'), 'r', encoding='utf-8') as fileConfig:
        dataConfig = fileConfig.readlines()
        for line in dataConfig:
            if 'role:' in line:
                if line.split(':')[1].lower().strip() == 'master':
                    global mode
                    mode = 'Master'
                elif line.split(':')[1].lower().strip() == 'slave':
                    mode = 'Slave'
            elif 'copyList:' in line:
                global copyList
                copyList = list(line.split(':')[1].strip().split(','))
            elif 'period_min:' in line:
                global period_min
                period_min = int(line.split(':')[1].strip())


def file_exists(file_name):
    return(os.path.exists(file_name))


def copyMaster(path):
    if os.path.isdir(joinpath(mainPath,
                              path)):
        if file_exists(upDateDirPath.format(path)):
            shutil.rmtree(upDateDirPath.format(path))
            shutil.copytree(joinpath(mainPath,
                                     path), upDateDirPath.format(
                path), ignore=shutil.ignore_patterns('ФБС*.xlsx', 'DEBUG*.xlsx', 'ФБС*.pdf', '__pycache__', '.git'))
        else:
            shutil.copytree(joinpath(mainPath,
                                     path), upDateDirPath.format(
                path), ignore=shutil.ignore_patterns('ФБС*.xlsx', 'DEBUG*.xlsx', 'ФБС*.pdf', '__pycache__', '.git'))
    else:
        if file_exists(upDateDirPath.format(path)):
            os.remove(upDateDirPath.format(path))
            shutil.copyfile(joinpath(mainPath,
                                     path), upDateDirPath.format(
                path))
        else:
            shutil.copyfile(joinpath(mainPath,
                                     path), upDateDirPath.format(
                path))


def copySlave(path):
    if os.path.isdir(upDateDirPath.format(
            path)):
        if file_exists(joinpath(mainPath,
                                path)):
            shutil.rmtree(joinpath(mainPath,
                                   path))
            shutil.copytree(upDateDirPath.format(
                path), joinpath(mainPath,
                                path))
        else:
            shutil.copytree(upDateDirPath.format(
                path), joinpath(mainPath,
                                path))
    else:
        if path == 'UpdateUpdater.py':
            shutil.copyfile(upDateDirPath.format(
                path), joinpath(mainPath,
                                path))
        else:
            shutil.copyfile(upDateDirPath.format(
                path), joinpath(mainPath,
                                path.replace('.', '_Update.')))


applyConfig()
if mode == 'Master':
    for file in copyList:
        copyMaster(file.strip())
elif mode == 'Slave':
    while True:
        for file in copyList:
            copySlave(file.strip())
            a = os.path.getmtime(joinpath(mainPath, 'Updater.py'))
            b = os.path.getmtime(
                joinpath(upDateDirPath.format('Updater.py')))
        if a != b:
            subprocess.Popen(
                'python ' + joinpath(mainPath, 'UpdateUpdater.py'))
        time.sleep(period_min)
