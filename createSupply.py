import requests
from datetime import timedelta, datetime
import base64
from os.path import join as joinpath
import pandas
import os


Token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjgyYTU2OGZlLTgyNTctNGQ2Yi05ZTg1LTJkYTgxMTgxYWI3MSJ9.ROCdF7eOfTZA-atpsLGTAi15yDzHk2UMes05vwjZwn4'
suppDir = r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\ШК поставки Оренбург'


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


def getStiker(OrderNum, Token):
    OrderNum = OrderNum if type(OrderNum) != float else int(OrderNum)[0:-2]
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


def crateSupply(Token):
    Url = 'https://suppliers-api.wildberries.ru/api/v2/supplies'

    response = requests.post(Url, headers={
        'Authorization': '{}'.format(Token)})
    if response.status_code != 201:
        print((response.status_code, response.text))
    else:
        print(response.json()['supplyId'])
        with open(joinpath(suppDir, 'postavkaOren.txt'), 'a', encoding='utf-8') as file:
            file.writelines(response.json()['supplyId'] + ' ' + str(
                datetime.today().date()))
            file.close()
        return response.json()['supplyId']


def addOrderInSupply(Token, stikerslist, supplyId):
    orderIdList = []
    stikerInput = 0
    while True:
        Flag = False
        tmp = input('Введите стикер, 0 - выйти: ')
        if tmp == '0':
            break
        try:
            stikerInput = int(tmp)
        except:
            stikerInput = tmp
        for stiker in stikerslist:
            if type(stikerInput) == int:
                if stiker['sticker']['wbStickerId'] == stikerInput:
                    orderIdList.append(str(stiker['orderId']))
                    Flag = True
                    break
            elif type(stikerInput) == str:
                if stiker['sticker']['wbStickerEncoded'] == stikerInput:
                    orderIdList.append(str(stiker['orderId']))
                    Flag = True
                    break

        if not Flag:
            print('Заказ {}, не добавлен.'.format(stikerInput))
    Url = 'https://suppliers-api.wildberries.ru/api/v2/supplies/{}'
    response = requests.put(Url.format(supplyId), headers={
        'Authorization': '{}'.format(Token)}, json={'orders': orderIdList})
    if response.status_code != 204:
        print((response.status_code, response.text))
    else:
        print((response.status_code, response.text))


def getBarcodeSupply(supplyId):
    Url = 'https://suppliers-api.wildberries.ru//api/v2/supplies/{}/barcode?type=pdf'
    response = requests.get(Url.format(supplyId), headers={
        'Authorization': '{}'.format(Token)})
    if response.status_code != 200:
        print((response.status_code, response.text))
    else:
        Base64 = bytes(response.json()['file'], 'utf-8')
        png_recovered = base64.decodestring(Base64)
        f = open(joinpath(suppDir, 'postavkaOren_{}.pdf'.format(
            datetime.today().date())), "wb")
        f.write(png_recovered)
        f.close()


def closeSupply(supplyId):
    Url = 'https://suppliers-api.wildberries.ru//api/v2/supplies/{}/close'
    response = requests.post(Url.format(supplyId), headers={
        'Authorization': '{}'.format(Token)})
    if response.status_code != 204:
        print((response.status_code, response.text))
    else:
        print('Поставка {} успешно закрыта.'.format(supplyId))


dataorders = get_orders(Token, days=2)
dataorderspd = pandas.DataFrame(dataorders)
dataorderspd.to_excel(joinpath(os.path.dirname(
    os.path.abspath(__file__)), r'\tmp.xlsx'), index=False)
stikerslist = getStiker(Token, dataorders)
stikerslistdp = pandas.DataFrame(stikerslist)
stikerslistdp.to_excel(joinpath(os.path.dirname(
    os.path.abspath(__file__)), r'\tmp.xlsx'), index=False)
if input('Создать поставку? 1-Да, 2-Нет: ') == '1':
    supplyId = crateSupply(Token)
else:
    supplyId = input('Введите номер поставки: ')
addOrderInSupply(Token, stikerslist, supplyId)
getBarcodeSupply(supplyId)
if input('Закрыть поставку {}? 1 - Закрыть, 0 - оставить открытой.: '.format(supplyId)) == '1':
    closeSupply(supplyId)
else:
    print('Поставка не {} закрыта.'.format(supplyId))
input('Готово, нажмите Enter')
