import os
import pandas as pd
import shutil


pathToPrint = r'\\192.168.0.111\shared\_Общие документы_\Каталог принтов'
pathToCopy = r'E:\Принты новые'
df = pd.DataFrame(pd.read_excel(r'E:\topPrint.xlsx', sheet_name='Лист4'))
categoryList = df['Группа'].unique().tolist()
printList = []
pull_1 = []
pull_2 = []
pull_3 = []
pullList = [pull_1, pull_2, pull_3]

for category in categoryList:
    printList.append(df[df['Группа'] == category]['Принт'].unique().tolist())
printList
for print_ in printList:
    while len(print_)>0:
        for j, pull in enumerate(pullList):
            for i in range(len(print_)):
                pull.append(print_[i])
                fileName = print_[i].replace('Принт','print') + '.png'
                shutil.copy2(pathToPrint + r'\\' + fileName, pathToCopy + r'\\' +f'pull_{str(j+1)}' + r'\\' +fileName)
                print_.pop(i)
                break
df = pd.DataFrame(pullList)
df = df.transpose()
df.to_excel(r'E:\topPrintNew.xlsx', index=False)


            






