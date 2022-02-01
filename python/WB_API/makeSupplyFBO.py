import os
import pandas
from my_lib import read_xlsx


pathToPackings = r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\Реестры ФБО'
listBox = []
listBoxNew = []
reestr = []
for file in os.listdir(pathToPackings):
    if 'ФБО коробка' in file and '.xlsx' in file:
        listBox.append(file)

barcodeLsit = read_xlsx(os.path.join(
    pathToPackings, r'barcodes.xlsx'), title='No')
if len(barcodeLsit) < len(listBox):
    print('Штрихкодов меньше чем коробок')
else:
    for j, pathBox in enumerate(listBox):
        num = str(pathBox.split('№ ')[1].split('.')[0])
        box = read_xlsx(os.path.join(pathToPackings, pathBox))
        barcodeBox = barcodeLsit[j]
        name = 'Уникальный ШК короба/Палеты'
        for line in box:
            line.update({'Уникальный ШК короба/Палеты': barcodeBox[0]})
        box
        data = {'ШК единицы товара': barcodeBox[0],
                'Номер коробки': num}
        reestr.append(data)
        listBoxNew.extend(box)
reestrpd = pandas.DataFrame(reestr)
reestrpd.to_excel(os.path.join(
    pathToPackings, 'реестр.xlsx'), index=False)
listBoxNewpd = pandas.DataFrame(listBoxNew)
listBoxNewpd.to_excel(os.path.join(
    pathToPackings, 'поставка.xlsx'), index=False)
