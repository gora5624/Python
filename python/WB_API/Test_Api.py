import os
import requests
import pandas
from datetime import datetime, timedelta
import multiprocessing

WBOrdersDataFileName = "Заказы полученые {}".format(
    datetime.today().isoformat('T', 'seconds')).replace(':', '.') + '.xlsx'


# def getOrdersMain(Token, start_data, Url, tmp1, count_skip, flag):

#     return response


def get_orders():
    Token = 'Mjc4YzZhY2YtOTlhMS00NDlkLTgwMTctZmFkMDk2YjQzNWEx'
    print("Идёт получение свежих заказов, ожидайте...")
    #Url = 'https://suppliers-api.wildberries.ru/api/v2/orders?date_start={}%2B03%3A00&take=1000&skip={}'
    Url = ' https://suppliers-stats.wildberries.ru/api/v1/supplier/stocks?dateFrom={}Z&key={}'
    #Url = 'https://suppliers-stats.wildberries.ru/api/v1/supplier/orders?dateFrom={}Z&flag=1&key={}'
    start_data = ((datetime.today() - timedelta(hours=int(12)))).isoformat('T', 'seconds').replace(
        ':', '%3A').replace('+', '%2B').replace('.', '%2E')
    tmp = []
    CountTry = 0
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
    for line in response.json():
        tmp.append(line)
    all_data = pandas.DataFrame(tmp)
    all_data.to_excel((os.path.join(os.path.join(
        os.environ['USERPROFILE']), 'Desktop', WBOrdersDataFileName)), index=False)


#days = input('Введите количество дней: ')
get_orders()
input('Готово, нажмите Enter')
