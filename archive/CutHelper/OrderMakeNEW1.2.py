import os
import sys
from my_lib import read_xlsx, file_exists, read_csv
import xlwt
from collections import Counter

order_path = sys.argv[1]
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
                            datatmp2[2], datatmp2[4], '1', num_tab])
            dataFromCorelNEW.append(datatmp)

list_tmp_for_counter = []
for data_0 in dataFromCorelNEW:
    list_tmp_for_counter.append(','.join(str(e) for e in data_0))
c = Counter(list_tmp_for_counter)

for data in c.keys():
    data_new = data.split(',')
    try:
        ws = wb.add_sheet("Стол {}".format(data_new[5]))
        i = 0
    except:
        pass
    data_new = data.split(',')
    data_new[4] = c[data]
    data_new[2] = data_new[2].replace('.0', '')
    for j, el in enumerate(data_new[0: 5]):
        ws.write(i, j, el)
    wb.save(r'C:\Users\Public\Documents\CutHelp\Cut_table.xls')
    i = i+1
