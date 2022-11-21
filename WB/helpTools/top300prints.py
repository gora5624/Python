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

listPrint = pandas.DataFrame(pandas.read_excel(r'E:\топ 300 принтов.xlsx'))['Принт'].values.tolist()
for file in os.listdir(r'F:\топ 300\Все'):
    name = file.replace('print', '(Принт').replace('.png', ')')
    #if name not in listPrint:
    print(name)
