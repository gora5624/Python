import requests
from datetime import timedelta, datetime
import base64
from os.path import join as joinpath
import pandas
import os


Token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjgyYTU2OGZlLTgyNTctNGQ2Yi05ZTg1LTJkYTgxMTgxYWI3MSJ9.ROCdF7eOfTZA-atpsLGTAi15yDzHk2UMes05vwjZwn4'
suppDir = r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\ШК поставки'
# Режим отладки 1 - да, 0 - боевой режим
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


def getStiker(Token, dataorders):
    stikers = []
    tmpOrders = []
    UrlStiker = 'https://suppliers-api.wildberries.ru/api/v2/orders/stickers'
    for line in dataorders:
        if line['status'] == 0 or line['status'] == 1:
            tmpOrders.append(int(line['orderId']))
        if len(tmpOrders) > 999:
            OrderNumJson = {"orderIds": tmpOrders}
            response = requests.post(UrlStiker, headers={
                'Authorization': '{}'.format(Token)}, json=OrderNumJson)
            stikers.extend(response.json()['data'])
            tmpOrders = []
    OrderNumJson = {"orderIds": tmpOrders}
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
        try:
            with open(joinpath(suppDir, 'postavka.txt'), 'a', encoding='utf-8') as file:
                file.writelines(response.json()['supplyId'] + ' ' + str(
                    datetime.today().date())+'\n')
                file.close()
        except FileNotFoundError:
            print('Поставка создана, но не записана в файл.')
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
                    if str(stiker['orderId']) not in orderIdList:
                        orderIdList.append(str(stiker['orderId']))
                        Flag = True
                        break
                    else:
                        print("Уже добавлен")
            elif type(stikerInput) == str:
                if stiker['sticker']['wbStickerEncoded'] == stikerInput:
                    if str(stiker['orderId']) not in orderIdList:
                        orderIdList.append(str(stiker['orderId']))
                        Flag = True
                        break
                    else:
                        print("Уже добавлен")

        if not Flag:
            print('Заказ {}, не добавлен.'.format(stikerInput))
    Url = 'https://suppliers-api.wildberries.ru/api/v2/supplies/{}'
    response = requests.put(Url.format(supplyId), headers={
        'Authorization': '{}'.format(Token)}, json={'orders': orderIdList})
    if response.status_code != 204:
        print((response.status_code, response.text))
    elif response.status_code == 409:
        failedOrdersList = response.json()['data']['failedOrders']
        for order in failedOrdersList:
            try:
                orderIdList.remove(order)
                print(
                    'Заказ {} успешно удалён из поставки, т.к. он отменён.'.format(order))
            except ValueError:
                print('Не удалось удалить лишние заказы из поставки. Попробуйте заного.')
        print('Пробую повторно отправить поставку.')
        response = requests.put(Url.format(supplyId), headers={
            'Authorization': '{}'.format(Token)}, json={'orders': orderIdList})
        if response.status_code == 204:
            print((response.status_code, response.text))
            print('Успешно!')
        else:
            print((response.status_code, response.text))
    else:
        print((response.status_code, response.text))
        if response.status_code == 204:
            changeStatus(orderIdList, Token)


def getBarcodeSupply(supplyId):
    Url = 'https://suppliers-api.wildberries.ru//api/v2/supplies/{}/barcode?type=pdf'
    response = requests.get(Url.format(supplyId), headers={
        'Authorization': '{}'.format(Token)})
    if response.status_code != 200:
        print((response.status_code, response.text))
    else:
        Base64 = bytes(response.json()['file'], 'utf-8')
        png_recovered = base64.decodebytes(Base64)
        f = open(joinpath(suppDir, '{}_от_{}.pdf'.format(supplyId,
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


def changeStatus(listOrderForChangeStatus, Token):
    """Изменяет статус заказа на заданный, в данном случае "1" - на сборке"""
    if Debug != 1:
        orderListForChange = []
        Url = 'https://suppliers-api.wildberries.ru/api/v2/orders'
        if Debug == 1:
            status = 0
        else:
            status = 2
        for orderId in listOrderForChangeStatus:
            if len(orderListForChange) < 1000:
                datajson = []
                datajson = {"orderId": orderId,
                            "status": status}
                orderListForChange.append(datajson)
            else:
                while True:
                    try:
                        response = requests.put(Url, headers={
                            'Authorization': '{}'.format(Token)}, json=orderListForChange)
                        if response.status_code != 200:
                            continue
                        elif response.status_code == 200:
                            break
                    except:
                        continue
                orderListForChange = []
                print(response)
        while True:
            try:
                response = requests.put(Url, headers={
                    'Authorization': '{}'.format(Token)}, json=orderListForChange)
                if response.status_code != 200:
                    continue
                elif response.status_code == 200:
                    print("Количество товара: {}".format(
                        str(len(orderListForChange))))
                    break
            except:
                continue
        print(response)


dataorders = get_orders(Token, days=3)
dataorderspd = pandas.DataFrame(dataorders)
dataorderspd.to_excel(joinpath(os.path.dirname(
    os.path.abspath(__file__)), r'\tmp.xlsx'), index=False)
stikerslist = getStiker(Token, dataorders)
stikerslistdp = pandas.DataFrame(stikerslist)
stikerslistdp.to_excel(joinpath(os.path.dirname(
    os.path.abspath(__file__)), r'\tmp2.xlsx'), index=False)
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
