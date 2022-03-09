import os
import pandas
import requests
from pandas import DataFrame
from datetime import datetime, timedelta

WBOrdersDataFileName = "Заказы ФБО полученые {}".format(
    datetime.today().isoformat('T', 'seconds')).replace(':', '.') + '.xlsx'


def get_orders(days):
    Token = 'Mjc4YzZhY2YtOTlhMS00NDlkLTgwMTctZmFkMDk2YjQzNWEx'
    print("Идёт получение заказов, ожидайте...")
    Url = 'https://suppliers-stats.wildberries.ru/api/v1/supplier/orders?dateFrom={}Z&flag=1&key={}'
    start_data = ((datetime.today() - timedelta(days=int(days)))).isoformat('T', 'seconds').replace(
        ':', '%3A').replace('+', '%2B').replace('.', '%2E')
    tmp = []
    tmp1 = []
    CountTry = 0
    while True:
        CountTry += 1
        try:
            response = requests.get(Url.format(start_data, Token))
            if response.status_code == 200:
                break
            elif CountTry > 500:
                print("Не удалось достучасться до ВБ")
            else:
                continue
        except:
            continue
    for line in response.json():
        if line['incomeID'] == 0:
            orderType = 'ФБС'
        else:
            orderType = 'ФБО'
        #Date = line['date'].split('T')[0]
        data = {'Баркод': int(line['barcode']),
                'Дата': line['date'],
                'Количество': 1,
                'Цена': int(line['totalPrice']),
                'Тип заказа': orderType}
        # tmp.append(line)
        tmp.append(data)
    all_data = DataFrame(tmp)
    for line in tmp:
        a = datetime.strptime(line['Дата'], "%Y-%m-%dT%H:%M:%S")
        line['Дата'] = a.date()
        tmp1.append(line)
    all_data1 = DataFrame(tmp1)
    all_data1.to_excel((os.path.join(os.path.join(
        os.environ['USERPROFILE']), 'Desktop', WBOrdersDataFileName)), index=False)


days = input('Введите количество дней: ')
get_orders(days)
input('Готово, нажмите Enter')
