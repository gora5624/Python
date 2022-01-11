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


def get_orders(Token, days=10):
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


def changeStatus(stikerList, Token, stikerInput):
    """Изменяет статус заказа на заданный, в данном случае "3" - отменён"""
    Url = 'https://suppliers-api.wildberries.ru/api/v2/orders'
    try:
        stikerInput = int(stikerInput)
    except:
        stikerInput = stikerInput
    for stiker in stikerList:
        if type(stikerInput) == int:
            if stiker['sticker']['wbStickerId'] == stikerInput:
                orderId = str(stiker['orderId'])
                break
            else:
                if stiker['sticker']['wbStickerEncoded'] == stikerInput:
                    orderId = str(stiker['orderId'])
                    break
    status = 3
    datajson = {"orderId": orderId,
                "status": status}
    response = requests.put(Url, headers={
        'Authorization': '{}'.format(Token)}, json=[datajson])
    if response.status_code != 200:
        print('При отмене произошла ошибка.')
    elif response.status_code == 200:
        print(response)
        print('Заказ {} отменён.'.format(str(stikerInput)))


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


dataorders = get_orders(Token, days=10)
stikerList = getStiker(Token, dataorders)
while True:
    stiker = input("Отсканируйте этикетку или введите номер стикера: ")
    changeStatus(stikerList, Token, stiker)
