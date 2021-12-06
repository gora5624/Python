import os
import subprocess
from os.path import join as joinpath
import time

mainPath = os.path.dirname(os.path.abspath(__file__))
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


while True:
    applyConfig()
    try:
        if mode == 'Slave':
            if file_exists(joinpath(mainPath, 'Updater_Update.pyw')):
                if file_exists(joinpath(mainPath, 'Updater_backup.pyw')):
                    os.remove(joinpath(mainPath, 'Updater_backup.pyw'))
                    os.rename(joinpath(mainPath, 'Updater.pyw'),
                              joinpath(mainPath, 'Updater_backup.pyw'))
                    os.rename(joinpath(mainPath, 'Updater_Update.pyw'),
                              joinpath(mainPath, 'Updater.pyw'))
                else:
                    os.rename(joinpath(mainPath, 'Updater.pyw'),
                              joinpath(mainPath, 'Updater_backup.pyw'))
                    os.rename(joinpath(mainPath, 'Updater_Update.pyw'),
                              joinpath(mainPath, 'Updater.pyw'))
                subprocess.Popen(
                    'python ' + joinpath(mainPath, 'Updater.pyw'))
                time.sleep(period_min*60)
    except:
        time.sleep(2*60)
