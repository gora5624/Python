import shutil
import os
from pandas import DataFrame
import pandas as pd

# mainPath = r'F:\Принты_05032024_выбрано'
# i = 7000
# list_ = []
# # for dir_ in os.listdir(mainPath):
# for file_ in os.listdir(os.path.join(mainPath)):
#     if '.db' not in file_ and '.png' in file_:
#         os.rename(os.path.join(mainPath,file_), os.path.join(mainPath, 'print ' + str(i) + '.png'))
#         list_.append({"oldName":os.path.join(mainPath,file_), 'newName':os.path.join(mainPath, 'print ' + str(i) + '.png')})
#         i+=1
# DataFrame(list_).to_excel(os.path.join(mainPath, 'name 2.xlsx'), index=False)



# mainPathToXLSX = r"F:\Принты_05032024_выбрано\name.xlsx"
# mainDF = pd.read_excel(mainPathToXLSX).to_dict('records')
# for line in mainDF:
#     if os.path.exists(os.path.join(r'F:\Принты_05032024_выбрано\выбрано 600', line['Новое имя'])):
#         os.rename(os.path.join(r'F:\Принты_05032024_выбрано\выбрано 600', line['Новое имя']), os.path.join(r'F:\Принты_05032024_выбрано\выбрано 600', line['Принт']))

for file in os.listdir(r'\\rab\Диск для принтов сервак Егор\книжки новые3 — копия\Черный'):
    if not os.path.exists(os.path.join(r'F:\Принты_05032024_выбрано\выбрано 600', file)) and 'Thumbs' not in file:
        os.remove(os.path.join(r'\\rab\Диск для принтов сервак Егор\книжки новые3 — копия\Черный', file))