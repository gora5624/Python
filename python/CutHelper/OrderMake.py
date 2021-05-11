import os
import sys
from my_lib import read_xlsx, file_exists, read_csv
import xlwt

order_path = r"C:\Users\Public\Documents\CutHelp\Заказ_на_резку_мат_02.05.21.xlsx"
with open(r'C:\Users\Public\Documents\CutHelp\orderNEW.txt', 'r', encoding='ansi') as file:
    dataFromCorel = []
    for line in file:
        dataFromCorel.append(line.strip().strip('"').split(';'))

wb = xlwt.Workbook()
i = 0
dataOrdet = read_xlsx(order_path, title="No")

dataFromCorelNEW = []
for datatmp in dataFromCorel:
    for datatmp2 in dataOrdet:
        if datatmp[1] == datatmp2[1]:
            num_tab = datatmp[2]
            datatmp = []
            datatmp.extend([datatmp2[0], datatmp2[1],
                            datatmp2[2], datatmp2[4], num_tab])
            dataFromCorelNEW.append(datatmp)

for data in dataFromCorelNEW:
    try:
        ws = wb.add_sheet("Стол {}".format(data[4]))
        i = 0
    except:
        pass
    for j, el in enumerate(data[0: 4]):
        ws.write(i, j, el)
    wb.save(r'C:\Users\Public\Documents\CutHelp\Cut_table.xls')
    i = i+1
