from my_lib import read_xlsx
import os

list_ = read_xlsx(r'D:\Под натяжку.xlsx', title='No')
for a in list_:
    os.mkdir(os.path.join(r'D:\mask', a[0]))
