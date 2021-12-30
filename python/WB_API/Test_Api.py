import os
import requests
import pandas
from datetime import datetime, timedelta
import multiprocessing
import time

WBOrdersDataFileName = "Заказы полученые {}".format(
    datetime.today().isoformat('T', 'seconds')).replace(':', '.') + '.xlsx'


def get_orders():
    i = 0
    Token = 'Mjc4YzZhY2YtOTlhMS00NDlkLTgwMTctZmFkMDk2YjQzNWEx'
    print("Идёт получение свежих заказов, ожидайте...")
    #Url = 'https://suppliers-api.wildberries.ru/api/v2/orders?date_start={}%2B03%3A00&take=1000&skip={}'
    Url = ' https://suppliers-stats.wildberries.ru/api/v1/supplier/stocks?dateFrom={}Z&key={}'
    #Url = 'https://suppliers-stats.wildberries.ru/api/v1/supplier/orders?dateFrom={}Z&flag=1&key={}'
    tmp = []
    all_data = []
    a = 0
    while a == 0:
        start_data = ((datetime.today() - timedelta(days=int(30)))).isoformat('T', 'seconds').replace(
            ':', '%3A').replace('+', '%2B').replace('.', '%2E')
        try:
            response = requests.get(Url.format(start_data, Token))
            i += 1
            a = len(response.json())
            if response.status_code == 429:
                time.sleep(10)

        except:
            continue
    for line in response.json():
        tmp.append(line)
    all_data = pandas.DataFrame(tmp)
    all_data.to_excel((os.path.join(os.path.join(
        os.environ['USERPROFILE']), 'Desktop', WBOrdersDataFileName)), index=False)


#days = input('Введите количество дней: ')
if __name__ == '__main__':
    get_orders()
    #input('Готово, нажмите Enter')
