import os
import pandas
import shutil

listPrint = pandas.read_excel(r'F:\top100.xlsx')['Принт'].values.tolist()
# for i, file in enumerate(os.listdir(r'F:\Принты со светом все\Все')):
#     if a:=file.replace('print', '(Принт').replace('.png', ')') in listPrint:
#         shutil.copy(os.path.join(r'F:\Принты со светом все\Все',file), os.path.join(r'F:\100','top_{}'.format(str(i))))
for i, file in enumerate(listPrint):
    fileName = file.replace('(Принт','print').replace(')','.png')
    shutil.copy(os.path.join(r'F:\Принты со светом все\Все',fileName), os.path.join(r'F:\100','top_{}.png'.format(str(i))))