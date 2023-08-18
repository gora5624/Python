import os
import pandas
import shutil

# mainPath = r'F:\Принты со светом все'
# srcPath = r'F:\топ 300'
# listPrint = pandas.DataFrame(pandas.read_excel(r'E:\топ 300 принтов.xlsx'))['Принт'].values.tolist()
# for dir in os.listdir(mainPath):
#     for file in os.listdir(os.path.join(mainPath, dir)):
#         name = file.replace('print', '(Принт').replace('.png', ')')
#         if name in listPrint:
#             shutil.copy(os.path.join(mainPath, dir,file), os.path.join(srcPath, dir,file))
pathToExcel = r"F:\Downloads\Принты книги 11082023.xlsx"
column = r'Общий итог'
topNum = 45
listPrint = pandas.DataFrame(pandas.read_excel(pathToExcel))['Названия строк'].values.tolist()[0:topNum]#.sort_values(by=[column], inplace=False, ascending=False)
# for file in os.listdir(r'\\rab\Диск для принтов сервак Егор\Принты со светом все\Все'):

    #if name not in listPrint:
    # print(name)
for i,j in enumerate(listPrint):
    name = j.replace('(Принт', 'print').replace(')','.png')
    # shutil.copy(os.path.join(r'\\192.168.0.111\shared\Отдел производство\макеты для принтера\Макеты для 6090\Оригиналы', name), os.path.join(r'D:\topBook', name))
    try:
        if '.png' not in name:
            name = name + '.png'
        shutil.copy(os.path.join(r'\\rab\Диск для принтов сервак Егор\Принты со светом все\Все', name), os.path.join(r'D:\topBook', name))
        # shutil.copy(os.path.join(r'\\rab\Диск для принтов сервак Егор\Принты со светом все\Все', name), os.path.join(r'D:\topBook', str(i+1)+'.png'))
    except:
        pass