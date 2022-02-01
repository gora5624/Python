import sys
import os
import base64
import barcode
from barcode.writer import ImageWriter
import fpdf
from fpdf import FPDF
import requests
from os.path import join as joinpath
from os import makedirs, remove
import PyPDF2
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from pdfrw import PdfReader, PdfWriter
import xlrd
import multiprocessing

pathToOrders = r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\Новые'
WBOrdersDataFileName = r'Data_orders.xlsx'
WBOrdersJsonDataFileName = r'Order.json'
main_path = os.path.dirname(os.path.abspath(__file__))
WBOrdersData = joinpath(
    main_path, r'WBOrdersData')
TMPDir = joinpath(
    main_path, r'TMPDirStiker')
Token_path = joinpath(
    main_path, r'Token.txt')
fpdf.set_global("SYSTEM_TTFONTS", os.path.join(
    os.path.dirname(__file__), r'C:\Windows\Fonts'))
Name1CStiker = '1c_{}.pdf'
NameWBStikerTMP = 'WBTMP_{}.pdf'
NameWBStiker = 'WB_{}.pdf'
NameSVG = 'WB_{}.svg'
NameTitle1CStiker = 'Name{}.pdf'
NameEAN13PNG = 'ean13_{}.png'


OrderNum = 188484496


def getStiker(OrderNum):
    OrderNum = OrderNum if type(OrderNum) != float else int(OrderNum)[0:-2]
    Token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjgyYTU2OGZlLTgyNTctNGQ2Yi05ZTg1LTJkYTgxMTgxYWI3MSJ9.ROCdF7eOfTZA-atpsLGTAi15yDzHk2UMes05vwjZwn4'
    UrlStiker = 'https://suppliers-api.wildberries.ru/api/v2/orders/stickers'
    trying = 0
    OrderNumJson = {"orderIds": [int(OrderNum)],
                    "type": 'qr'}
    while True:
        trying += 1
        try:
            response = requests.post(UrlStiker, headers={
                'Authorization': '{}'.format(Token)}, json=OrderNumJson)
            if response.status_code == 200:
                break
            elif trying > 500:
                print("Не удолось достучаться до сервера ВБ")
                sys.stdout.flush()
                return 1
            else:
                continue
        except:
            continue

    a = response.json()['data'][0]['sticker']['wbStickerSvgBase64']
    a


getStiker(OrderNum)
