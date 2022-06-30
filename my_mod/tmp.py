import re
from my_lib import read_xlsx
import os

data = read_xlsx(r'E:\123.xlsx')
for line in data:
    os.remove(line['Picture Filename'])