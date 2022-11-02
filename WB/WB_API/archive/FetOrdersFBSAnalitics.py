import os
import requests
import pandas
from datetime import datetime, timedelta

WBOrdersDataFileName = "Заказы полученые {} {}.xlsx"
curData = datetime.today().date().strftime(r"%d.%m.%Y")
curTime = datetime.today().time().strftime(r"%H.%M.%S")
TokenAbr = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
TokenKar = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
TokenSam = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'


def get_orders(Token, mode, days=3):
    i = 0
    print("Идёт получение свежих заказов, ожидайте...")
    # Url = 'https://suppliers-api.wildberries.ru/api/v2/orders?date_start={}%2B03%3A00&take=1000&skip={}'
    if '.' not in days:
        days = int(days)
        Url = 'https://suppliers-api.wildberries.ru/api/v2/orders?date_start={}%2B03%3A00&take=1000&skip={}'
        start_data = ((datetime.today() - timedelta(days=int(days)))).isoformat('T', 'seconds').replace(
        ':', '%3A').replace('+', '%2B').replace('.', '%2E')
        end_data = ((datetime.today() - timedelta(days=int(days)))).isoformat('T', 'seconds').replace(
        ':', '%3A').replace('+', '%2B').replace('.', '%2E')
    else:
        Url = 'https://suppliers-api.wildberries.ru/api/v2/orders?date_start={}%2B00%3A00&take=1000&skip={}&date_end={}%2B00%3A00'
        start_data = datetime.strptime(days, '%d.%m.%Y').isoformat('T', 'seconds').replace(
        ':', '%3A').replace('+', '%2B').replace('.', '%2E')
        end_data = (datetime.strptime(days, '%d.%m.%Y') + timedelta(days=1)).isoformat('T', 'seconds').replace(
        ':', '%3A').replace('+', '%2B').replace('.', '%2E')
    tmp = []
    #start_data = ((datetime.today() - timedelta(days=int(days)))).isoformat('T', 'seconds').replace(
        #':', '%3A').replace('+', '%2B').replace('.', '%2E')
    count_skip = 0
    tmp = []
    dataorders = []
    flag = True
    while len(tmp) > 0 or flag:
        CountTry = 0
        flag = False
        while True:
            CountTry += 1
            try:
                if type(days) == int:
                    response = requests.get(Url.format(start_data, count_skip), headers={
                    'Authorization': '{}'.format(Token)})
                else:
                    response = requests.get(Url.format(start_data, count_skip, end_data), headers={
                    'Authorization': '{}'.format(Token)})
                if response.status_code == 200:
                    break
                elif CountTry > 500:
                    print("Не удалось достучасться до ВБ")
                else:
                    continue
            except:
                continue
        count_skip = count_skip+1000
        tmp = response.json()['orders']
        dataorders.extend(tmp)
    dataNew = []
    dfdataorders = pandas.DataFrame(dataorders)
    dfdataorders['barcode'] = dfdataorders['barcode'].astype(str)
    dfBarcodes = pandas.DataFrame(pandas.read_table(r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\ШК.txt'))
    dfBarcodes['Штрихкод'] = dfBarcodes['Штрихкод'].astype(str)
    dfdataordersMerge = pandas.merge(dfdataorders, dfBarcodes, how='left',left_on='barcode',right_on='Штрихкод')
    for line in dfdataordersMerge.to_dict('recodrs'):
        date = line['dateCreated'].split('T')[0].split('-')
        time = ':'.join(line['dateCreated'].split('T')[1].split(':')[0:2])
        date = date[2] + '.' + date[1] + '.' + date[0]
        #barcod = int(line['barcode']) if line['barcode'] != '' else ''
        if line['storeId'] == 10237:
            ip = 'Караханян'
        elif line['storeId'] == 141069:
            ip = 'Манвел'
        elif line['storeId'] == 278784:
            ip = 'Самвел'
        else:
            ip = 'хз'

        datatmp = {
            'Номенклатура': line['Номенклатура'],
            # 'Баркод': int(line['barcode']) if line['barcode'] != '' else '',
            'Дата': date,
            'Время': time,
            'Количество': 1,
            'Цена': line['convertedPrice']/100,
            'Номер заказа':line['orderId'],
            'ИП': ip}
        dataNew.append(datatmp)
        #dataNew.append(line)
    dataNewpd = pandas.DataFrame(dataNew)
    dataNewpd.to_excel((os.path.join(os.path.join(
        os.environ['USERPROFILE']), 'Desktop', WBOrdersDataFileName.format(curData + '_' + curTime, 'все ИП'))), index=False)


def get_ordersAll(days=3):
    i = 0
    print("Идёт получение свежих заказов, ожидайте...")
    if '.' not in days:
        days = int(days)
        Url = 'https://suppliers-api.wildberries.ru/api/v2/orders?date_start={}%2B03%3A00&take=1000&skip={}'
        start_data = ((datetime.today() - timedelta(days=int(days)))).isoformat('T', 'seconds').replace(
        ':', '%3A').replace('+', '%2B').replace('.', '%2E')
        end_data = ((datetime.today() - timedelta(days=int(days)))).isoformat('T', 'seconds').replace(
        ':', '%3A').replace('+', '%2B').replace('.', '%2E')
    else:
        Url = 'https://suppliers-api.wildberries.ru/api/v2/orders?date_start={}%2B00%3A00&take=1000&skip={}&date_end={}%2B00%3A00'
        start_data = datetime.strptime(days, '%d.%m.%Y').isoformat('T', 'seconds').replace(
        ':', '%3A').replace('+', '%2B').replace('.', '%2E')
        end_data = (datetime.strptime(days, '%d.%m.%Y') + timedelta(days=1)).isoformat('T', 'seconds').replace(
        ':', '%3A').replace('+', '%2B').replace('.', '%2E')
    dataNew = []
    dataorders = []
    tmp = []
    for Token in [TokenKar, TokenAbr, TokenSam]:
        flag = True
        count_skip = 0
        while len(tmp) > 0 or flag:
            CountTry = 0
            flag = False
            while True:
                CountTry += 1
                try:
                    if type(days) == int:
                        response = requests.get(Url.format(start_data, count_skip), headers={
                        'Authorization': '{}'.format(Token)})
                    else:
                        response = requests.get(Url.format(start_data, count_skip, end_data), headers={
                        'Authorization': '{}'.format(Token)})
                    if response.status_code == 200:
                        break
                    elif CountTry > 500:
                        print("Не удалось достучасться до ВБ")
                    else:
                        continue
                except:
                    continue
            count_skip = count_skip+1000
            tmp = response.json()['orders']
            dataorders.extend(tmp)
    dfdataorders = pandas.DataFrame(dataorders)
    dfdataorders['barcode'] = dfdataorders['barcode'].astype(str)
    dfBarcodes = pandas.DataFrame(pandas.read_table(r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\ШК.txt'))
    dfBarcodes['Штрихкод'] = dfBarcodes['Штрихкод'].astype(str)
    dfdataordersMerge = pandas.merge(dfdataorders, dfBarcodes, how='left',left_on='barcode',right_on='Штрихкод')
    for line in dfdataordersMerge.to_dict('records'):
        date = line['dateCreated'].split('T')[0].split('-')
        time = ':'.join(line['dateCreated'].split('T')[1].split(':')[0:2])
        date = date[2] + '.' + date[1] + '.' + date[0]
        #barcod = int(line['barcode']) if line['barcode'] != '' else ''
        if line['storeId'] == 10237:
            ip = 'Караханян'
        elif line['storeId'] == 141069:
            ip = 'Манвел'
        elif line['storeId'] == 278784:
            ip = 'Самвел'
        else:
            ip = 'хз'

        datatmp = {
            'Номенклатура': line['Номенклатура'],
            # 'Баркод': int(line['barcode']) if line['barcode'] != '' else '',
            'Дата': date,
            'Время': time,
            'Количество': 1,
            'Цена': line['convertedPrice']/100,
            'Номер заказа':line['orderId'],
            'ИП': ip}
        dataNew.append(datatmp)
        #dataNew.append(line)
    dataNewpd = pandas.DataFrame(dataNew)
    dataNewpd.to_excel((os.path.join(os.path.join(
        os.environ['USERPROFILE']), 'Desktop', WBOrdersDataFileName.format(curData + '_' + curTime, 'все ИП'))), index=False)


def getMode():
    try:
        a = int(input('Введите режим работы: "0" по всем ИП, "1" - Караханян, "2" - Абраамян: , "3" - Самвел: '))
    except ValueError:
        print('По умолчанию 0.')
        a = 0
    if a == 1:
        return 1
    elif a == 2:
        return 2
    elif a == 3:
        return 3
    elif a == 0:
        return 0
    else:
        print('По умолчанию Караханян.')
        return 1


if __name__ == '__main__':
    while True:
        mode = getMode()
        if mode == 1:
            token = TokenKar
        elif mode == 2:
            token = TokenAbr
        elif mode == 3:
            token = TokenSam
        elif mode == 0:
            token = [TokenKar, TokenAbr, TokenSam]
        else:
            print("Введён некорректный режим, установлен режим Караханян")
            token = TokenKar
        try:
            days = input("Введите количество дней (по умолчанию 3 дня) или дату в фомате ДД.ММ.ГГГГ: ")
        except ValueError:
            days = 3
        if type(token) == list:
            get_ordersAll(days=days)
        else:
            get_orders(token, mode, days=days)
        input('Готово, нажмите Enter')
