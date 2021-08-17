from my_lib import read_xlsx
from termcolor import colored
'''
order_data = read_xlsx(
    r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\Архив\Data_order.xlsx')

while True:
    line = ''
    line2 = ''
    line = input('Введите первый штрихкод: ')
    Flag = 0
    Flag2 = 1
    if len(line) < 11:
        for data in order_data:
            if data['wbStickerEncoded'] == line:
                Flag = 1
                print('Штрихкод найден')
                break
        line2 = input('Введите второй штрихкод:')
        for data in order_data:
            if str(data['barcode'])[0:-2] == line2 and data['wbStickerEncoded'] == line:
                print('Все верно!')
                Flag2 = 0
                break
            else:
                continue
        if Flag and Flag2:
            print('ШК найден, но совпадений в 2м ШК нет')
        if not Flag:
            print('Данный штрихкод не найден в файле')
        Flag = 0
    else:
        for data in order_data:
            if str(data['barcode'])[0:-2] == line:
                Flag = 1
                print('Штрихкод найден')
                break
        line2 = input('Введите второй штрихкод:')
        for data in order_data:
            if str(data['wbStickerEncoded']) == line2 and str(data['barcode'])[0:-2] == line:
                print('Все верно!')
                Flag2 = 0
                break
            else:
                continue
        if Flag and Flag2:
            print('ШК найден, но совпадений в 2м ШК нет')
        if not Flag:

            print('Данный штрихкод не найден в файле')
        Flag = 0'''

order_data = read_xlsx(
    r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\data_order.xlsx')

while True:
    line = ''
    line2 = ''
    line = input('Введите первый штрихкод: ')
    Flag = 0
    Flag2 = 1
    if len(line) < 11:
        for data in order_data:
            if data['wbStickerEncoded'] == line:
                Flag = 1
                print('Штрихкод найден')
                break
        line2 = input('Введите второй штрихкод:')
        for data in order_data:
            if str(data['barcode'])[0:-2] == line2 and data['wbStickerEncoded'] == line:
                print('Все верно!')
                Flag2 = 0
                break
            else:
                continue
        if Flag and Flag2:
            print('ШК найден, но совпадений в 2м ШК нет')
        if not Flag:
            print('Данный штрихкод не найден в файле')
        Flag = 0
    else:
        for data in order_data:
            if str(data['barcode'])[0:-2] == line:
                Flag = 1
                print('Штрихкод найден')
                break
        line2 = input('Введите второй штрихкод:')
        for data in order_data:
            if str(data['numer'])[0:-2] == line2 and str(data['barcode'])[0:-2] == line:
                print('Все верно!')
                Flag2 = 0
                break
            else:
                continue
        if Flag and Flag2:
            print('ШК найден, но совпадений в 2м ШК нет')
        if not Flag:

            print('Данный штрихкод не найден в файле')
        Flag = 0
