import os
import re
for file in os.listdir(r'D:\newPrint'):
    if 'print' not in file:
        num = file.split('.')[0]
        num = str(5000+int(re.sub(r'-.*.png','',file)))
        new = os.path.join(r'D:\newPrint', r'print {}.pdf'.format(num))
        os.rename(os.path.join(r'D:\newPrint', file),new)
    else:
        os.rename(os.path.join(r'D:\newPrint', file),os.path.join(r'D:\newPrint', file.replace('pdf','png')))
