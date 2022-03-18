import os
import requests
import pandas
from datetime import datetime, timedelta

WBOrdersDataFileName = "Заказы полученые {} {}.xlsx"
curData = datetime.today().date().strftime(r"%d.%m.%Y")
curTime = datetime.today().time().strftime(r"%H.%M.%S")
TokenAbr = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
TokenKar = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'


def get_orders(Token, mode, days=3):
    i = 0
    print("Идёт получение свежих заказов, ожидайте...")
    Url = 'https://suppliers-api.wildberries.ru/api/v2/orders?date_start={}%2B03%3A00&take=1000&skip={}'
    tmp = []
    start_data = ((datetime.today() - timedelta(days=int(days)))).isoformat('T', 'seconds').replace(
        ':', '%3A').replace('+', '%2B').replace('.', '%2E')
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
        tmp = response.json()['orders']
        dataorders.extend(tmp)
    dataNew = []
    for line in dataorders:
        date = line['dateCreated'].split('T')[0].split('-')
        date = date[2] + '.' + date[1] + '.' + date[0]
        datatmp = {'Баркод': int(line['barcode']),
                   'Дата': date,
                   'Количество': 1,
                   'Цена': line['totalPrice']/100}
        dataNew.append(datatmp)
    dataNewpd = pandas.DataFrame(dataNew)
    dataNewpd.to_excel((os.path.join(os.path.join(
        os.environ['USERPROFILE']), 'Desktop', WBOrdersDataFileName.format(curData + '_' + curTime, "Караханян" if mode == 1 else "Абраамян"))), index=False)


def getMode():
    return 1 if int(input('Введите режим работы: "1" - Караханян, "2" - Абраамян: ')) == 1 else 2


if __name__ == '__main__':
    while True:
        mode = getMode()
        if mode == 1:
            token = TokenKar
        elif mode == 2:
            token = TokenAbr
        else:
            print("Введён некорректный режим, установлен режим Караханян")
            token = TokenKar
        days = int(input("Введите количество дней (по умолчанию 3 дня): "))
        get_orders(token, mode, days=days)
        input('Готово, нажмите Enter')
