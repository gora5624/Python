import os
import shutil

path = r"F:\новые принты"

for fld in os.listdir(path):
    if os.path.isdir(os.path.join(path,fld)):
        for file in os.listdir(os.path.join(path,fld)):
            if '.pdf' in file:
                shutil.copy(os.path.join(path,fld,file),os.path.join(r'F:\test',fld+"_"+file))
            # print('a')
# for file in os.listdir(r'F:\новые принты\0'):
#     os.rename(os.path.join(r'F:\новые принты\0', file),os.path.join(r'F:\новые принты\0', file.replace("new ",'')))