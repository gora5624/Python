import os
import sys
from my_lib import read_xlsx

#pathToPrint = sys.argv[1].replace("_", " ")
pathToPrint = r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\Каталог принтов'



def Rename_print(pathToPrint):
    list_print_name = os.listdir(
        r'\\192.168.0.33\shared\Отдел производство\Wildberries\оригиналы принтов')
    listPrint = os.listdir(pathToPrint)
    for Print in listPrint:
        for name in list_print_name:
            PrintN = Print.replace('print', 'Принт')[0:-4]
            nameN = name[name.find('(')+1:name.find(')')]
            if PrintN == nameN:
                os.rename(os.path.join(pathToPrint, Print),
                          os.path.join(pathToPrint, name+'.png'))

'''for dir in os.listdir(pathToPrint):
    Rename_print(os.path.join(pathToPrint, dir))'''
Rename_print(pathToPrint)

