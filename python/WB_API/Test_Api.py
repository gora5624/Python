import requests
from my_lib import write_csv
import datetime
import os

delta = datetime.timedelta(hours=0, minutes=0)
now = datetime.datetime.now(datetime.timezone.utc) + delta
url = 'https://suppliers-stats.wildberries.ru/api/v1/supplier/stocks?dateFrom={}6:00:00.000Z&key=MThlZmZjODAtZGU0Yi00NGEwLWIwN2EtZWUzNjVlNGRjY2Uz'.format(now.isoformat()[0:-14][
    0:-7])
print(url)
responce = requests.get(url)

print(responce)

if responce.status_code == 429:
    print('Слишком много запросов, повторите через пару минут.')
    input('Нажмите Enter')
else:
    a = os.getcwd() + '\\' + 'остатки.csv'
    for line in responce.json():
        write_csv(line, os.getcwd() + '\\' + 'остатки.csv')

    print("Файл сохранён в {}".format(a))
    input('Нажмите Enter')
