from numpy import nan
import pandas as pd
import os
import shutil

lst = pd.read_excel(r"F:\Downloads\antitopprints.xlsx").to_dict('records')
for i, line in enumerate(lst):
    line = dict(line)
    for dir_ in list(line.items()):
        if not os.path.exists(a:=os.path.join(printDirNew:=r'F:\Downloads\Новая папка2', dir_[0])):
            os.mkdir(a)

        if not dir_[1] is nan:
            if os.path.exists(printpath:=os.path.join(printDir:=r'\\192.168.0.111\shared\_Общие документы_\Каталог принтов', dir_[1])):
                shutil.copy(printpath, printpath.replace(printDir,printDirNew+'\\'+dir_[0]).replace(dir_[1],str(i)+'_'+dir_[1]))
            else:
                open(printpath.replace(printDir,printDirNew+'\\'+dir_[0]).replace(dir_[1],str(i)+'_'+dir_[1]), 'w').close()

        
