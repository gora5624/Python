import os
import base64
import fpdf
import requests
from os.path import join as joinpath
import PyPDF2


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
    Base64 = bytes('PD94bWwgdmVyc2lvbj0iMS4wIj8+CjwhLS0gR2VuZXJhdGVkIGJ5IFNWR28gLS0+Cjxzdmcgd2lkdGg9IjQwMCIgaGVpZ2h0PSIzMDAiCiAgICAgdmlld0JveD0iMjAgMjAgMzUwIDI2MCIKICAgICB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciCiAgICAgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiPgo8cmVjdCB4PSIwIiB5PSIwIiB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgc3R5bGU9ImZpbGw6d2hpdGUiIC8+CjxyZWN0IHg9IjYwIiB5PSIyMCIgd2lkdGg9IjUiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iNjciIHk9IjIwIiB3aWR0aD0iMyIgaGVpZ2h0PSIxNzAiIHN0eWxlPSJmaWxsOmJsYWNrIiAvPgo8cmVjdCB4PSI3NCIgeT0iMjAiIHdpZHRoPSIyIiBoZWlnaHQ9IjE3MCIgc3R5bGU9ImZpbGw6YmxhY2siIC8+CjxyZWN0IHg9Ijg2IiB5PSIyMCIgd2lkdGg9IjQiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iOTUiIHk9IjIwIiB3aWR0aD0iMiIgaGVpZ2h0PSIxNzAiIHN0eWxlPSJmaWxsOmJsYWNrIiAvPgo8cmVjdCB4PSIxMDQiIHk9IjIwIiB3aWR0aD0iMiIgaGVpZ2h0PSIxNzAiIHN0eWxlPSJmaWxsOmJsYWNrIiAvPgo8cmVjdCB4PSIxMTEiIHk9IjIwIiB3aWR0aD0iNCIgaGVpZ2h0PSIxNzAiIHN0eWxlPSJmaWxsOmJsYWNrIiAvPgo8cmVjdCB4PSIxMTciIHk9IjIwIiB3aWR0aD0iNyIgaGVpZ2h0PSIxNzAiIHN0eWxlPSJmaWxsOmJsYWNrIiAvPgo8cmVjdCB4PSIxMjciIHk9IjIwIiB3aWR0aD0iMiIgaGVpZ2h0PSIxNzAiIHN0eWxlPSJmaWxsOmJsYWNrIiAvPgo8cmVjdCB4PSIxMzYiIHk9IjIwIiB3aWR0aD0iMiIgaGVpZ2h0PSIxNzAiIHN0eWxlPSJmaWxsOmJsYWNrIiAvPgo8cmVjdCB4PSIxNDAiIHk9IjIwIiB3aWR0aD0iNyIgaGVpZ2h0PSIxNzAiIHN0eWxlPSJmaWxsOmJsYWNrIiAvPgo8cmVjdCB4PSIxNDkiIHk9IjIwIiB3aWR0aD0iNSIgaGVpZ2h0PSIxNzAiIHN0eWxlPSJmaWxsOmJsYWNrIiAvPgo8cmVjdCB4PSIxNjEiIHk9IjIwIiB3aWR0aD0iMiIgaGVpZ2h0PSIxNzAiIHN0eWxlPSJmaWxsOmJsYWNrIiAvPgo8cmVjdCB4PSIxNjciIHk9IjIwIiB3aWR0aD0iMTAiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iMTc5IiB5PSIyMCIgd2lkdGg9IjIiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iMTg2IiB5PSIyMCIgd2lkdGg9IjIiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iMTkwIiB5PSIyMCIgd2lkdGg9IjMiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iMTk3IiB5PSIyMCIgd2lkdGg9IjkiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iMjExIiB5PSIyMCIgd2lkdGg9IjIiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iMjE4IiB5PSIyMCIgd2lkdGg9IjIiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iMjIyIiB5PSIyMCIgd2lkdGg9IjUiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iMjM2IiB5PSIyMCIgd2lkdGg9IjIiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iMjQzIiB5PSIyMCIgd2lkdGg9IjQiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iMjQ5IiB5PSIyMCIgd2lkdGg9IjMiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iMjYxIiB5PSIyMCIgd2lkdGg9IjIiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iMjcwIiB5PSIyMCIgd2lkdGg9IjQiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iMjgxIiB5PSIyMCIgd2lkdGg9IjMiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iMjg2IiB5PSIyMCIgd2lkdGg9IjIiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iMjkwIiB5PSIyMCIgd2lkdGg9IjUiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iMzAwIiB5PSIyMCIgd2lkdGg9IjYiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iMzExIiB5PSIyMCIgd2lkdGg9IjQiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iMzIyIiB5PSIyMCIgd2lkdGg9IjciIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iMzMxIiB5PSIyMCIgd2lkdGg9IjMiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iMzM2IiB5PSIyMCIgd2lkdGg9IjQiIGhlaWdodD0iMTcwIiBzdHlsZT0iZmlsbDpibGFjayIgLz4KPHJlY3QgeD0iMjAiIHk9IjIwMCIgd2lkdGg9IjM1MCIgaGVpZ2h0PSI5MCIgc3R5bGU9ImZpbGw6YmxhY2siIC8+Cjx0ZXh0IHg9IjMwIiB5PSIyNDAiIHN0eWxlPSJmaWxsOndoaXRlO2ZvbnQtc2l6ZTozMHB0O3RleHQtYW5jaG9yOnN0YXJ0IiA+NDg4NTE2PC90ZXh0Pgo8dGV4dCB4PSIzNTAiIHk9IjI3MCIgc3R5bGU9ImZpbGw6d2hpdGU7Zm9udC1zaXplOjUwcHQ7dGV4dC1hbmNob3I6ZW5kIiA+MTM4NDwvdGV4dD4KPC9zdmc+Cg==', 'utf-8')
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
