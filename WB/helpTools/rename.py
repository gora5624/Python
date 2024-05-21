import os
import shutil

for f in os.listdir(r'F:\выбрано'):
    shutil.copy(os.path.join(r'F:\Все какие нашёл png', f),os.path.join(r'F:\выбрано2', f))
    print(f)