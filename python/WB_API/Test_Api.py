import os
import requests
import pandas
from datetime import datetime, timedelta
import multiprocessing

WBOrdersDataFileName = "Заказы полученые {}".format(
    datetime.today().isoformat('T', 'seconds')).replace(':', '.') + '.xlsx'


def getOrdersMain(Token, start_data):
    while len(tmp1) > 0 or flag:
        CountTry = 0
        flag = False
        while True:
            CountTry += 1
            try:
                response = requests.get(Url.format(start_data, count_skip), headers={
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
        tmp1 = response.json()['orders']
    return response


def get_orders(days):
    Token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjgyYTU2OGZlLTgyNTctNGQ2Yi05ZTg1LTJkYTgxMTgxYWI3MSJ9.ROCdF7eOfTZA-atpsLGTAi15yDzHk2UMes05vwjZwn4'
    print("Идёт получение свежих заказов, ожидайте...")
    Url = 'https://suppliers-api.wildberries.ru/api/v2/orders?date_start={}%2B03%3A00&take=1000&skip={}'
    start_data = (datetime.today() - timedelta(days=int(days))).isoformat('T', 'seconds').replace(
        ':', '%3A').replace('+', '%2B').replace('.', '%2E')
    count_skip = 0
    tmp = []
    tmp1 = []
    flag = True
    getOrdersMain
    t1 = multiprocessing.Process(
        target=getOrdersMain, args=(Token, start_data,))
    t1.start()
    for line in response.json()['orders']:
        data = {'Дата': line['dateCreated'].split('T')[0],
                'Баркод': line['barcode'],
                'Количество': '1',
                'Цена': str(line['totalPrice'])[0:-2],
                'Стикер': line['sticker']
                }
        tmp.append(data)
    all_data = pandas.DataFrame(tmp)
    all_data.to_excel((os.path.join(os.path.join(
        os.environ['USERPROFILE']), 'Desktop', WBOrdersDataFileName)), index=False)


days = input('Введите количество дней: ')
get_orders(days)
input('Готово, нажмите Enter')
