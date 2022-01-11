from io import BytesIO
from re import A
from reportlab.graphics.transform import scale
import requests
from datetime import timedelta, datetime
import base64
from os.path import join as joinpath
import pandas
import os
import fpdf
from fpdf import FPDF
from reportlab.graphics import renderPDF, renderPM
from svglib.svglib import svg2rlg
import io
from PIL import Image


fpdf.set_global("SYSTEM_TTFONTS", os.path.join(
    os.path.dirname(__file__), r'C:\Windows\Fonts'))
Token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjgyYTU2OGZlLTgyNTctNGQ2Yi05ZTg1LTJkYTgxMTgxYWI3MSJ9.ROCdF7eOfTZA-atpsLGTAi15yDzHk2UMes05vwjZwn4'
suppDir = r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\ШК поставки'
# Режим отладки 1 - да, 0 - боевой режим
Debug = 0


def get_orders(Token, days=4):
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
        # if line['status'] == 0 or line['status'] == 1:
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
    count = len(orderIdList)
    print(response.text)
    while response.status_code == 409:
        failedOrdersList = response.json()['data']['failedOrders']
        orderIdListForChange = []
        orderIdListForChange.extend(orderIdList)
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
            changeStatus(orderIdListForChange, orderIdList, Token)
            return count
        else:
            print((response.status_code, response.text))
    #
    # if response.status_code != 204:
    #     print((response.status_code, response.text))

    # else:
    #     print((response.status_code, response.text))
    #     if response.status_code == 204:
    #         changeStatus(orderIdListForChange, orderIdList, Token)
    #         return count


def getBarcodeSupply(supplyId, count):
    Url = 'https://suppliers-api.wildberries.ru//api/v2/supplies/{}/barcode?type=svg'
    response = requests.get(Url.format(supplyId), headers={
        'Authorization': '{}'.format(Token)})
    if response.status_code != 200:
        print((response.status_code, response.text))
    else:
        Base64 = bytes(response.json()['file'], 'utf-8')
        SVG_recovered = base64.decodebytes(Base64)
        fileTMPName = joinpath(suppDir, '{}_от_{}_tmp.pdf'.format(supplyId,
                                                                  datetime.today().date()))

        drawing = svg2rlg(io.BytesIO(SVG_recovered))
        renderPM.drawToFile(
            drawing, fileTMPName.replace('.pdf', '.png'), fmt="PNG")
    img = Image.open(fileTMPName.replace('.pdf', '.png'))
    new_image = img.resize((600, 450))
    new_image.save(fileTMPName.replace('.pdf', '.png'))
    size = (200, 300)
    pdf = FPDF(format=size)
    pdf.add_page()
    pdf.image(fileTMPName.replace('.pdf', '.png'), x=-1, y=0, w=0)
    pdf.add_font(
        'Arial', '', fname="Arial.ttf", uni=True)
    pdf.set_font('Arial', '', 45)
    pdf.multi_cell(180, 150)
    pdf.multi_cell(180, 25, txt="{}".format(
        'ИП Караханян Э.С.'), align='C')
    pdf.multi_cell(180, 25, txt="{}".format(
        'Маркетплейс Оренбург'), align='C')
    day = datetime.today().date().strftime(r"%d.%m.%Y")
    pdf.multi_cell(180, 25, txt="{}".format(
        'От {}').format(day), align='C')
    if count != 0:
        pdf.multi_cell(180, 25, txt="{}".format(
            'Количество {} шт.').format(str(count)), align='C')
    pdf.output(fileTMPName.replace('_tmp', ''))
    try:
        os.remove(fileTMPName.replace('.pdf', '.png'))
    except:
        pass


def closeSupply(supplyId):
    Url = 'https://suppliers-api.wildberries.ru//api/v2/supplies/{}/close'
    response = requests.post(Url.format(supplyId), headers={
        'Authorization': '{}'.format(Token)})
    if response.status_code != 204:
        print((response.status_code, response.text))
    else:
        print('Поставка {} успешно закрыта.'.format(supplyId))


def changeStatus(listOrderForChangeStatus, orderIdList, Token):
    """Изменяет статус заказа на заданный, в данном случае "1" - на сборке"""
    if Debug != 1:
        orderListForChange = []
        orderListForChange_2 = []
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
        for orderId in orderIdList:
            if len(orderListForChange_2) < 1000:
                datajson = []
                datajson = {"orderId": orderId,
                            "status": status}
                orderListForChange_2.append(datajson)
            else:
                while True:
                    try:
                        response = requests.put(Url, headers={
                            'Authorization': '{}'.format(Token)}, json=orderListForChange)
                        if response.status_code != 200:
                            response = requests.put(Url, headers={
                                'Authorization': '{}'.format(Token)}, json=orderListForChange_2)
                            if response.status_code != 200:
                                continue
                            elif response.status_code == 200:
                                break
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


while True:
    dataorders = get_orders(Token, days=5)
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
    count = addOrderInSupply(Token, stikerslist, supplyId)
    getBarcodeSupply(supplyId, count)
    if input('Закрыть поставку {}? 1 - Закрыть, 0 - оставить открытой.: '.format(supplyId)) == '1':
        closeSupply(supplyId)
    else:
        print('Поставка не {} закрыта.'.format(supplyId))
    input('Готово, нажмите Enter')
