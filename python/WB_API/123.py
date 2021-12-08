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
    Base64 = bytes('JVBERi0xLjMKMyAwIG9iago8PC9UeXBlIC9QYWdlCi9QYXJlbnQgMSAwIFIKL01lZGlhQm94IFswIDAgMTY1LjMwIDExNC40MF0KL1Jlc291cmNlcyAyIDAgUgovQ29udGVudHMgNCAwIFI+PgplbmRvYmoKNCAwIG9iago8PC9GaWx0ZXIgL0ZsYXRlRGVjb2RlIC9MZW5ndGggNDUxPj4Kc3RyZWFtCngBfJQxj9swDIV3/wqO7ZBXUpQoaQ1wPbRbAQOdm7N9wG3t0r9fOJfoZLPOFCAEH/k+0Y/p+8D0NjBSpr8Dg5np+fb7OkiBZhKuqEaCqnTKCcnoz0zLEAQh36uMWLZVhZXjakZK92pADJte5XXWba5TVkXRe9VtpYbQlBk1b5UrrPW6ahRw29kpx4T4oDejtLmCmDZzE+ODlfObIqQpu7nJOlZu51Q3rHZ+TaHhg9VuK8uQ5tcp5+tVHL1CDuCm7Htjx8o5ytaxcjSKIPDh3BJgjbPvNXAjGVB58wqlrv80RztWVREaDadcrWPlHNUC63beKQsLapN2zcIGbVu7exfOyK3boV7thNbt9hZRpNbtDlPE1i93Fan2H3Ep68d5KzugEsIjZhISrAuQ3flJqODjtxQNqMcnJhq7dPJY1KDdk+ziSbQgN3FvLGr30XlqMW+w7PJLEqM8mJ1Cl1FO/HT1Et5D1yok0ymu0fweu+eRvnyduGhOi8X5UovJi82/5jgtL8t0mTQxL5fpMqvOJAZmGhd6GoffJNeAf6XzSHJVlIjINE706ef59PztFLMWSeEzjW/0NNKP4V8AAAD//7DkQzcKZW5kc3RyZWFtCmVuZG9iagoxIDAgb2JqCjw8L1R5cGUgL1BhZ2VzCi9LaWRzIFszIDAgUiBdCi9Db3VudCAxCi9NZWRpYUJveCBbMCAwIDU5NS4yOCA4NDEuODldCj4+CmVuZG9iago1IDAgb2JqCjw8L1R5cGUgL0ZvbnQKL0Jhc2VGb250IC9UaW1lcy1Sb21hbgovU3VidHlwZSAvVHlwZTEKL0VuY29kaW5nIC9XaW5BbnNpRW5jb2RpbmcKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1Byb2NTZXQgWy9QREYgL1RleHQgL0ltYWdlQiAvSW1hZ2VDIC9JbWFnZUldCi9Gb250IDw8Ci9GZDA4Mzc1ZjY0ZWI5ODYxYzZlYWU0ZGZjZmRiZDM1MDBmYmRiZTMzZSA1IDAgUgo+PgovWE9iamVjdCA8PAo+PgovQ29sb3JTcGFjZSA8PAo+Pgo+PgplbmRvYmoKNiAwIG9iago8PAovUHJvZHVjZXIgKP7/AEYAUABEAEYAIAAxAC4ANykKL0NyZWF0aW9uRGF0ZSAoRDoyMDIxMTIwODExMzg1OCkKL01vZERhdGUgKEQ6MjAyMTEyMDgxMTM4NTgpCj4+CmVuZG9iago3IDAgb2JqCjw8Ci9UeXBlIC9DYXRhbG9nCi9QYWdlcyAxIDAgUgovTmFtZXMgPDwKL0VtYmVkZGVkRmlsZXMgPDwgL05hbWVzIFsKICAKXSA+Pgo+Pgo+PgplbmRvYmoKeHJlZgowIDgKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwNjM4IDAwMDAwIG4gCjAwMDAwMDA4MjMgMDAwMDAgbiAKMDAwMDAwMDAwOSAwMDAwMCBuIAowMDAwMDAwMTE3IDAwMDAwIG4gCjAwMDAwMDA3MjUgMDAwMDAgbiAKMDAwMDAwMDk4NCAwMDAwMCBuIAowMDAwMDAxMDk3IDAwMDAwIG4gCnRyYWlsZXIKPDwKL1NpemUgOAovUm9vdCA3IDAgUgovSW5mbyA2IDAgUgo+PgpzdGFydHhyZWYKMTE5NAolJUVPRgo=', 'utf-8')
    pdf_writer = PyPDF2.PdfFileWriter()
    png_recovered = base64.decodestring(Base64)
    f = open(joinpath(TMPDir, 'postavka'), "wb")
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
