import os
import shutil


with open(r'F:\printspdf.txt', 'r', encoding='utf-8') as file:
  listFile = file.readlines()
  for i, line in enumerate(listFile):
    listFile[i] = line[0:-1]
  listFile
for file in listFile:
  try:
    if os.path.join(r'\\192.168.0.33\shared\_Общие документы_\Егор\Все принты\Принты под пластины PDF\полные', file) not in os.listdir(r'\\192.168.0.33\shared\_Общие документы_\Егор\Все принты\Принты под пластины PDF'):
      shutil.copy(os.path.join(r'\\192.168.0.111\shared\Отдел производство\макеты для принтера\Макеты для 6090\XXL',file),os.path.join(r'\\192.168.0.33\shared\_Общие документы_\Егор\Все принты\Принты под пластины PDF\полные', file) )
  except:
    pass
  try:
    if os.path.join(r'\\192.168.0.33\shared\_Общие документы_\Егор\Все принты\Принты под пластины PDF\полные', file.replace('pdf','cdr')) not in os.listdir(r'\\192.168.0.33\shared\_Общие документы_\Егор\Все принты\Принты под пластины PDF'):
      shutil.copy(os.path.join(r'\\192.168.0.111\shared\Отдел производство\макеты для принтера\Макеты для 6090\XXL',file.replace('pdf','cdr')),os.path.join(r'\\192.168.0.33\shared\_Общие документы_\Егор\Все принты\Принты под пластины PDF\полные', file.replace('pdf','cdr')) )
  except:
    pass



