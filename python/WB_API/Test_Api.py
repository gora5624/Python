import os
import requests
import pandas
from datetime import datetime, timedelta
import multiprocessing

WBOrdersDataFileName = "Заказы полученые {}".format(
    datetime.today().isoformat('T', 'seconds')).replace(':', '.') + '.xlsx'


# def getOrdersMain(Token, start_data, Url, tmp1, count_skip, flag):

#     return response


def get_orders(days):
    Token = 'Mjc4YzZhY2YtOTlhMS00NDlkLTgwMTctZmFkMDk2YjQzNWEx'
    print("Идёт получение свежих заказов, ожидайте...")
    # Url = 'https://suppliers-api.wildberries.ru/api/v2/orders?date_start={}%2B03%3A00&take=1000&skip={}'
    Url = ' https://suppliers-stats.wildberries.ru/api/v1/supplier/stocks?dateFrom={}T21%3A00%3A00.000Z&key={}'
    start_data = (datetime.today()).isoformat('T', 'seconds').replace(
        ':', '%3A').replace('+', '%2B').replace('.', '%2E')
    count_skip = 0
    tmp = []
    tmp1 = []
    flag = True
    while len(tmp1) > 0 or flag:
        CountTry = 0
        flag = False
        while True:
            CountTry += 1
            try:
                # response = requests.get(Url.format(start_data, count_skip), headers={
                #     'Authorization': '{}'.format(Token)})
                response = requests.get(Url.format(start_data, Token))
                if response.status_code == 200:
                    break
                elif CountTry > 500:
                    print("Не удалось достучасться до ВБ")
                else:
                    continue
            except:
                continue
        count_skip = count_skip+1000
        tmp1 = response.json()['orders']
        for line in response.json()['orders']:
            data = {'Баркод': int(line['barcode']),
                    'Дата': line['dateCreated'].split('T')[0].split('-')[2]+'.'+line['dateCreated'].split('T')[0].split('-')[1]+'.'+line['dateCreated'].split('T')[0].split('-')[0],
                    'Количество': 1,
                    'Цена': int(str(line['totalPrice'])[0:-2]),
                    'sticker': line['sticker'],
                    'orderId': line['orderId'],
                    'userInfo': line['userInfo'],
                    'officeAddress': line['officeAddress']
                    }
            tmp.append(data)
    all_data = pandas.DataFrame(tmp)
    all_data.to_excel((os.path.join(os.path.join(
        os.environ['USERPROFILE']), 'Desktop', WBOrdersDataFileName)), index=False)


# days = input('Введите количество дней: ')
days = 1
get_orders(days)
input('Готово, нажмите Enter')
