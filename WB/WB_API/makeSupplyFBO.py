import os
import pandas
from my_lib import read_xlsx
import copy


pathToPackings = r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\Реестры ФБО'
listBox = []
listBoxNew = []
reestr = []
order = []
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
        boxtm = copy.deepcopy(box)
        order.extend(boxtm)
        boxNew = []
        for line in box:
            lineNew = {'ШК единицы товара': line['Баркод'],
                       'Кол-во товаров': line['Количество'],
                       'Уникальный ШК короба/Палеты': barcodeBox[0],
                       'срок годности': '',
                       'Если товар с Кизом, заполните – Да': ''}
            boxNew.append(lineNew)
        data = {'ШК единицы товара': barcodeBox[0],
                'Номер коробки': num}
        reestr.append(data)
        listBoxNew.extend(boxNew)
reestrpd = pandas.DataFrame(reestr)
reestrpd.to_excel(os.path.join(
    pathToPackings, 'реестр.xlsx'), index=False)
listBoxNewpd = pandas.DataFrame(listBoxNew)
listBoxNewpd.to_excel(os.path.join(
    pathToPackings, 'поставка.xlsx'), index=False)
orderpd = pandas.DataFrame(order)
orderpd.to_excel(os.path.join(
    pathToPackings, 'Заказ.xlsx'), index=False)
