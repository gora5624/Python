import os
from my_lib import write_csv

file_list = os.listdir(r'D:\Done\Antyspy')
for file in file_list:
    data = {'name': file.replace('.jpg', '')}
    write_csv(data, "tmp.csv")
