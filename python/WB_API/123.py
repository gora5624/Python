from ntpath import join
import sys
import os
import base64
import barcode
from barcode.writer import ImageWriter
import fpdf
from fpdf import FPDF
import requests
import json
import pandas
from datetime import datetime, timedelta
from my_lib import file_exists
from os.path import join as joinpath
from os import makedirs, remove
from os.path import join
import PyPDF2
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from pdfrw import PdfReader, PdfWriter
import xlrd
import multiprocessing


pathToOrders = r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\Новые'
WBOrdersDataFileName = r'Data_orders.xlsx'
WBOrdersJsonDataFileName = r'Order.json'
main_path = r'C:\Users\Public\Documents\WBHelpTools\MakeWBStikersWithName'
WBOrdersData = joinpath(
    main_path, r'WBOrdersData')
TMPDir = r'D:\\'
Token_path = joinpath(
    main_path, r'Token.txt')
fpdf.set_global("SYSTEM_TTFONTS", os.path.join(
    os.path.dirname(__file__), r'C:\Windows\Fonts'))
Name1CStiker = '1c_{}.pdf'
NameWBStikerTMP = 'WBTMP_{}.pdf'
NameWBStiker = 'WB_{}.pdf'
NameSVG = 'WB_{}.pdf'
NameTitle1CStiker = 'Name{}.pdf'
NameEAN13PNG = 'ean13_{}.png'
NameTable = 'TBL_{}.pdf'


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


def create_WB_barcod():
    Base64 = bytes('JVBERi0xLjMKMyAwIG9iago8PC9UeXBlIC9QYWdlCi9QYXJlbnQgMSAwIFIKL01lZGlhQm94IFswIDAgMTY1LjMwIDExNC40MF0KL1Jlc291cmNlcyAyIDAgUgovQ29udGVudHMgNCAwIFI+PgplbmRvYmoKNCAwIG9iago8PC9GaWx0ZXIgL0ZsYXRlRGVjb2RlIC9MZW5ndGggNDQ5Pj4Kc3RyZWFtCngBfJQxj9swDIV3/wqO7ZBXUpQoaQ1wPbRbAQOdm7N9wG3t0r9/cC7RySacKUAIvsf3ySTTz4HpbWCkTP8HBjPT8+33dZACzSRcUY0EVemUE5LRv5mWIQhCvlcZsWyrCivH1YyU7tWAGDa9yqvXzdcpq6LoveqmUkNoyoyat8oV1npdNQq4zeyUY0J80JtRmq8gpo1vYnyycnlThDRl55usY+VmTnXDapfXFBo+We2msgxpeZ1yvn4VR6+QA7gp+97YsXKJsnWsHI0iCHzoWwKscfa9Bm4kAypvXqHU9Z+WaMeqKkKj4ZSrdaxcolpg3cw7ZWFGamM5WMKC2pwVut0k4Yz8oCwBdvwSIhHclth7i62be8REpKzLeSs7oBLCI2YSEqzz3p0ICaXbN0dcVFDbUzvkorG7Tj6YZuSue/fpS5SH1KJ2S+fWWWLeYNndL0mM0n0O+9wpdDfKiZ+uWcLH0bUKyXSK62n+OLvnkb59n7hoTovF+VKLyYvNf+Y4LS/LdJk0MS+X6TKrziQGZhoXehqHvyTXA/9K55HkqigRkWmc6Mvv8+n5xynmGkqWrzS+0dNIv4b3AAAA///IDUNNCmVuZHN0cmVhbQplbmRvYmoKMSAwIG9iago8PC9UeXBlIC9QYWdlcwovS2lkcyBbMyAwIFIgXQovQ291bnQgMQovTWVkaWFCb3ggWzAgMCA1OTUuMjggODQxLjg5XQo+PgplbmRvYmoKNSAwIG9iago8PC9UeXBlIC9Gb250Ci9CYXNlRm9udCAvVGltZXMtUm9tYW4KL1N1YnR5cGUgL1R5cGUxCi9FbmNvZGluZyAvV2luQW5zaUVuY29kaW5nCj4+CmVuZG9iagoyIDAgb2JqCjw8Ci9Qcm9jU2V0IFsvUERGIC9UZXh0IC9JbWFnZUIgL0ltYWdlQyAvSW1hZ2VJXQovRm9udCA8PAovRmQwODM3NWY2NGViOTg2MWM2ZWFlNGRmY2ZkYmQzNTAwZmJkYmUzM2UgNSAwIFIKPj4KL1hPYmplY3QgPDwKPj4KL0NvbG9yU3BhY2UgPDwKPj4KPj4KZW5kb2JqCjYgMCBvYmoKPDwKL1Byb2R1Y2VyICj+/wBGAFAARABGACAAMQAuADcpCi9DcmVhdGlvbkRhdGUgKEQ6MjAyMTEyMDkxMjI1NTcpCi9Nb2REYXRlIChEOjIwMjExMjA5MTIyNTU3KQo+PgplbmRvYmoKNyAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMSAwIFIKL05hbWVzIDw8Ci9FbWJlZGRlZEZpbGVzIDw8IC9OYW1lcyBbCiAgCl0gPj4KPj4KPj4KZW5kb2JqCnhyZWYKMCA4CjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDYzNiAwMDAwMCBuIAowMDAwMDAwODIxIDAwMDAwIG4gCjAwMDAwMDAwMDkgMDAwMDAgbiAKMDAwMDAwMDExNyAwMDAwMCBuIAowMDAwMDAwNzIzIDAwMDAwIG4gCjAwMDAwMDA5ODIgMDAwMDAgbiAKMDAwMDAwMTA5NSAwMDAwMCBuIAp0cmFpbGVyCjw8Ci9TaXplIDgKL1Jvb3QgNyAwIFIKL0luZm8gNiAwIFIKPj4Kc3RhcnR4cmVmCjExOTIKJSVFT0YK', 'utf-8')
    pdf_writer = PyPDF2.PdfFileWriter()
    png_recovered = base64.decodestring(Base64)
    f = open(joinpath(TMPDir, 'postavka1'), "wb")
    f.write(png_recovered)
    f.close()
    # drawing = svg2rlg(joinpath(TMPDir, NameSVG.format(procNum)))
    # renderPDF.drawToFile(drawing, joinpath(
    #     TMPDir, NameWBStikerTMP.format(procNum)))
    # pdf_file = PyPDF2.PdfFileReader(
    #     open(joinpath(TMPDir, NameWBStikerTMP.format(procNum)), 'rb'))
    # page = pdf_file.getPage(0)
    # # page.mediaBox.upperRight = (370, 280)
    # # page.mediaBox.upperLeft = (20, 280)
    # # page.mediaBox.lowerRight = (370, 15)
    # page.scaleBy(3)
    # pdf_writer.addPage(page)
    # with open(joinpath(TMPDir, NameWBStiker.format(procNum)), 'wb') as out_file:
    #     pdf_writer.write(out_file)
    # return joinpath(TMPDir, NameWBStiker.format(procNum))


create_WB_barcod()
