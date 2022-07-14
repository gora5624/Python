import os


import os 
import pandas


tmpList = []
for dir in os.listdir(r'E:\новый китай по категориям'):
    if not os.path.isdir(os.path.join(r'E:\новый китай по категориям',dir)):
        continue
    for file in os.listdir(os.path.join(r'E:\новый китай по категориям',dir)):
            tmpList.append({
            'Категория':dir, 
            'Принт': file.replace('print','(Принт').replace('.jpg',')')
            })
tmpListpd = pandas.DataFrame(tmpList)
tmpListpd.to_excel(r'E:\\tmp.xlsx', index=False)