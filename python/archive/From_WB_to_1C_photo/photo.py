import os
from my_lib import read_xlsx, file_exists

data = read_xlsx(
    r'\\192.168.0.33\shared\Отдел производство\Wildberries\Анализ\Номенклатура\Список номенклатуры 1c 26.04.21.xlsx')

file_list = os.listdir(r'D:\доделать')


for kod in data:
    for file in file_list:
        if kod['Штрихкод'] in file:
            if file_exists(os.path.join(r'D:\доделать', 'new', kod['Код'])):
                try:
                    os.remove(os.path.join(r'D:\доделать', 'new', kod['Код']))
                except:
                    pass
            try:
                os.rename(os.path.join(r'D:\доделать', file),
                          os.path.join(r'D:\доделать', 'new', kod['Код']))
            except:
                pass

file_list = os.listdir(r'D:\доделать')


print()
