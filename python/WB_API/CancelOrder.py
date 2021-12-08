from my_lib import read_xlsx
import requests
from os.path import join as joinpath
from os import listdir
import xlrd
from GetOrdersInWork import getToken
import pandas
from datetime import datetime, timedelta

main_path = r'C:\Users\Public\Documents\WBGetOrder'
Token_path = joinpath(main_path, r'Token.txt')
WBOrdersDataFileName = 'ordersForCancel.xlsx'
WBStikersDataFileName = 'stikersForCancel.xlsx'
Debug = 0


def get_orders(Token, days=3):
    """Получает заказы за последние 3 дня"""
    print("Идёт получение свежих заказов, ожидайте...")
    Url = 'https://suppliers-api.wildberries.ru/api/v2/orders?date_start={}%2B03%3A00&take=1000&skip={}'

    start_data = (datetime.today() - timedelta(days=int(days))).isoformat('T', 'seconds').replace(
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
    return dataorders


def getStiker(OrderNum):
    OrderNum = OrderNum if type(OrderNum) != float else int(OrderNum)[0:-2]
    with open(Token_path, 'r', encoding='UTF-8') as file:
        Token = file.read()
        file.close()
    UrlStiker = 'https://suppliers-api.wildberries.ru/api/v2/orders/stickers'
    trying = 0
    OrderNumJson = {"orderIds": [int(OrderNum)]}
    while True:
        trying += 1
        try:
            response = requests.post(UrlStiker, headers={
                'Authorization': '{}'.format(Token)}, json=OrderNumJson)
            if response.status_code == 200:
                break
            elif trying > 500:
                print("Не удолось достучаться до сервера ВБ")
                return 1
            else:
                continue
        except:
            continue

    return response.json()['data'][0]['sticker']['wbStickerSvgBase64']


def getStiker(Token, dataorders):
    stikers = []
    tmpOrders = []
    UrlStiker = 'https://suppliers-api.wildberries.ru/api/v2/orders/stickers'
    for line in dataorders:
        if line['status'] == 1:
            tmpOrders.append(int(line['orderId']))
        if len(tmpOrders) > 999:
            OrderNumJson = {"orderIds": tmpOrders}
            response = requests.post(UrlStiker, headers={
                'Authorization': '{}'.format(Token)}, json=OrderNumJson)
            stikers.extend(response.json()['data'])
            tmpOrders = []
    OrderNumJson = {"orderIds": [tmpOrders]}
    response = requests.post(UrlStiker, headers={
        'Authorization': '{}'.format(Token)}, json=OrderNumJson)
    stikers.extend(response.json()['data'])
    return stikers


def changeStatus(listOrderForChangeStatus, Token):
    """Изменяет статус заказа на заданный, в данном случае "1" - на сборке"""
    if Debug != 1:
        orderListForChange = []
        Url = 'https://suppliers-api.wildberries.ru/api/v2/orders'
        status = 1
        orderId = listOrderForChangeStatus
        datajson = {"orderId": str(orderId),
                    "status": status}
        orderListForChange.append(datajson)
        # response = requests.put(Url, headers={
        #     'Authorization': '{}'.format(Token)}, json=orderListForChange)
        print(orderId)
        # print(response)
        # print(response.text)


def cancelOrder(stikeriD, stikerslist):
    for line in stikerslist:
        if str(line['sticker']['wbStickerId']) == stikeriD:
            listOrderForChangeStatus = line['orderId']
            changeStatus(listOrderForChangeStatus, getToken())
           # print('{} отменен.'.format(stikeriD))
            return 0


dataorders = get_orders(getToken(), days=5)
stikerslist = getStiker(getToken(), dataorders)
while True:
    stikeriD = str(input('Введи нормер стикера: '))
    cancelOrder(stikeriD, stikerslist)
