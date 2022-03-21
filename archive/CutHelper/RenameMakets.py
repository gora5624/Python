import sys
from os.path import join as joinPath
from os import listdir, rename
sys.path.insert(1, joinPath(__file__, '../../..'))
from my_mod.my_lib import read_xlsx

pathToMakets = r'E:\Макеты'
pathToExcelWithKodAndBarcod = r'E:\rename.xlsx'

for line in read_xlsx(pathToExcelWithKodAndBarcod):
    for file in listdir(pathToMakets):
        if line['Код'] in file:
            barcod = str(line['ШК'])[0:-2]
            rename(joinPath(pathToMakets, file),joinPath(pathToMakets, file.replace(line['Код'], barcod)))
