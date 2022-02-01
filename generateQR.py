from ast import While
import PyPDF2
import requests
import base64
from os.path import join as joinpath
import fpdf
import os
import pandas
import requests
from datetime import timedelta, datetime
import base64
import pandas
import os
import fpdf
from fpdf import FPDF
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
from PIL import Image
from reportlab.graphics import renderPDF

fpdf.set_global("SYSTEM_TTFONTS", os.path.join(
    os.path.dirname(__file__), r'C:\Windows\Fonts'))
Token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjgyYTU2OGZlLTgyNTctNGQ2Yi05ZTg1LTJkYTgxMTgxYWI3MSJ9.ROCdF7eOfTZA-atpsLGTAi15yDzHk2UMes05vwjZwn4'


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


def getStikers(Token, dataorders):
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
    count = 0
    while response.json()['data'] == None and count < 100:
        response = requests.post(UrlStiker, headers={
            'Authorization': '{}'.format(Token)}, json=OrderNumJson)
        count += 1
    a = response.json()['data']
    if response.json()['data'] != None:
        stikers.extend(response.json()['data'])
    return stikers


def getStiker(OrderNum):
    OrderNum = OrderNum if type(OrderNum) != float else int(OrderNum)[0:-2]
    Token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjgyYTU2OGZlLTgyNTctNGQ2Yi05ZTg1LTJkYTgxMTgxYWI3MSJ9.ROCdF7eOfTZA-atpsLGTAi15yDzHk2UMes05vwjZwn4'
    UrlStiker = 'https://suppliers-api.wildberries.ru/api/v2/orders/stickers'
    trying = 0
    OrderNumJson = {"orderIds": [int(OrderNum)],
                    "type": "qr"}
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


def addOrderInSupply(stikerslist):
    stikerInput = 0
    while True:
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
                    return int(stiker['orderId']), str(stikerInput)


dataorders = get_orders(Token, days=5)
dataorderspd = pandas.DataFrame(dataorders)
dataorderspd.to_excel(joinpath(os.path.dirname(
    os.path.abspath(__file__)), r'\tmpQR.xlsx'), index=False)
stikerslist = getStikers(Token, dataorders)
stikerslistdp = pandas.DataFrame(stikerslist)
stikerslistdp.to_excel(joinpath(os.path.dirname(
    os.path.abspath(__file__)), r'\tmpQR2.xlsx'), index=False)
while True:
    OrderNum, stikerInput = addOrderInSupply(stikerslist)
    Base64 = bytes(getStiker(OrderNum), 'utf-8')
    pdf_writer = PyPDF2.PdfFileWriter()
    png_recovered = base64.decodestring(Base64)
    f = open(joinpath(r'D:\\', str(stikerInput)+'.svg'), "wb")
    f.write(png_recovered)
    f.close()
    drawing = svg2rlg(joinpath(r'D:\\', str(stikerInput)+'.svg'))
    renderPDF.drawToFile(drawing, joinpath(r'D:\\', str(stikerInput)+'.pdf'))
