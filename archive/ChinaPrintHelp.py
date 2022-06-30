import pandas


import pandas
import os

tmpList = []
for folder in os.listdir(r'E:\новый китай по категориям'):
    if os.path.isdir(os.path.join(r'E:\новый китай по категориям',folder)):
        tmpList.extend(os.listdir(os.path.join(r'E:\новый китай по категориям',folder)))

# tmpListpd = pandas.DataFrame(tmpList)
# tmpListpd.to_excel(r'E:\новый китай по категориям\tmp1.xlsx', index=False)



for file in os.listdir(r'E:\Новая папка'):
    a = file[0:-4] + '.jpg'
    a
    if (a not in tmpList) and ('.ai' not in file):
        os.remove(os.path.join(r'E:\Новая папка',file))


pandas.DataFrame(os.listdir(r'E:\Новая папка')).to_excel(r'E:\новый китай по категориям\tmp2.xlsx', index=False)
