import requests
from os.path import join as joinpath
from GetOrdersInWork import getToken
from datetime import datetime, timedelta

main_path = r'C:\Users\Public\Documents\WBGetOrder'
Token_path = joinpath(main_path, r'Token.txt')
WBOrdersDataFileName = 'ordersForCancel.xlsx'
WBStikersDataFileName = 'stikersForCancel.xlsx'
Debug = 0
Token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjgyYTU2OGZlLTgyNTctNGQ2Yi05ZTg1LTJkYTgxMTgxYWI3MSJ9.ROCdF7eOfTZA-atpsLGTAi15yDzHk2UMes05vwjZwn4'


def get_orders(Token, days=3):
    """Получает заказы за последние 3 дня"""
    print("Идёт получение свежих заказов, ожидайте...")
    Url = 'https://suppliers-api.wildberries.ru/api/v2/orders?date_start={}%2B03%3A00&take=1000&skip={}'

    start_data = (datetime.today() - timedelta(days=int(days))).isoformat('T', 'seconds').replace(
        ':', '%3A').replace('+', '%2B').replace('.', '%2E')
    count_skip = 1
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
    return dataorders


def changeStatus(listOrderForChangeStatus, Token):
    """Изменяет статус заказа на заданный, в данном случае "1" - на сборке"""
    orderListForChange = []
    for order in listOrderForChangeStatus:
        if order['wbWhId'] == 117986:
            if Debug != 1:
                Url = 'https://suppliers-api.wildberries.ru/api/v2/orders'
                status = 2
                datajson = {"orderId": str(order['orderId']),
                            "status": status}
                orderListForChange.append(datajson)
        else:
            pass
    response = requests.put(Url, headers={
        'Authorization': '{}'.format(Token)}, json=orderListForChange)
    print(response)
    print(response.text)


dataorders = get_orders(getToken(), days=5)
while True:
    changeStatus(dataorders, Token)
