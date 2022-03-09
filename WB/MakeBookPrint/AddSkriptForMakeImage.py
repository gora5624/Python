from os.path import abspath, join as joinPath
from os import listdir, rename
import sys
sys.path.append(abspath(joinPath(__file__,'../../..')))
from my_mod.my_lib import  read_xlsx, multiReplace
import requests
import time

pathToCategoryList = abspath(joinPath(__file__, '..', 'cat.xlsx'))

bookCaseColorDict = {'бордовый': 'VNS',
                     'бронзовый': 'BNZ',
                     'голубой': 'SKB',
                     'зеленый': 'GRN',
                     'золотой': 'GLD',
                     'красный': 'RED',
                     'розовое золото': 'P-GLD',
                     'серый': 'GRY',
                     'синий': 'BLU',
                     'черный': 'BLC'}


reductionDict = {'закрытой камерой': 'зак.кам.',
                 'открытой камерой': 'отк.кам.',
                 'матовый': 'мат.',
                 'прозрачный': 'проз.',
                 'с силиконовым основанием': 'с сил. вставкой',
                 'с силиконовый вставкой': 'с сил. вставкой',
                 'противоударный': 'противоуд.',
                 'переливающиеся блестки': 'жидк. блестки',
                 'с усиленными углами': 'с усил.угл.',
                 'Чехол для': 'Чехол'}
reductionDict2 = {'Чехол для': 'Чехол'}


def RenameImage(pathToPrint):
    listPrint = listdir(pathToPrint)
    for Print in listPrint:
        if "_" in Print:
            PrintN = Print.replace('print_', '(Принт ')[
                0:-4] + ')' if Print[-5] != ')' else Print.replace('print_', '(Принт ')[
                0:-4] + ''
        else:
            PrintN = Print.replace('print ', '(Принт ')[
                0:-4] + ')' if Print[-5] != ')' else Print.replace('print_', '(Принт ')[
                0:-4] + ''
        rename(joinPath(pathToPrint, Print),
                  joinPath(pathToPrint, PrintN+'.jpg'))


def genArtColor(colorBook, listImage):
    listCase = []
    colorBook = colorBook.lower()
    artColor_1 = 'BK'
    # узнаём цвет чехла
    for color, codeColor in bookCaseColorDict.items():
        if color == colorBook:
            artColor_2 = codeColor
            break
        else:
            artColor_2 = 'UNKNOW_COLOR'
    categoryList = read_xlsx(pathToCategoryList)
    for namePrint in listImage:
        for category in categoryList:
            if category['Принт'] == namePrint[0:-4]:
                printNum = namePrint[0:-4].split(' ')[1][0:-1]
                printNum = '0'*(4-len(printNum)) + printNum
                artColor = [artColor_1, artColor_2,
                            category['Код категории'], 'PRNT', printNum]
                dataTMP = {'Принт': namePrint[0:-4],
                           'Категория': category['Категория'],
                           'Код категории': category['Код категории'],
                           'Артикул цвета': ('_').join(artColor),
                           'Код товара': artColor_1,
                           'Код цвета': artColor_2}
                listCase.append(dataTMP)
    return listCase




def generate_bar_WB(count):
    listBarcode = []
    countTry = 0
    url = "https://suppliers-api.wildberries.ru/card/getBarcodes"
    headers = {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjgyYTU2OGZlLTgyNTctNGQ2Yi05ZTg1LTJkYTgxMTgxYWI3MSJ9.ROCdF7eOfTZA-atpsLGTAi15yDzHk2UMes05vwjZwn4',
               'Content-Type': 'application/json',
               'accept': 'application/json'}

    while count > 5000:
        count -= 5000
        while True and countTry < 10:
            data = "{\"id\":1,\"jsonrpc\":\"2.0\",\"params\":{\"quantity\":5000,\"supplierID\":\"3fa85f64-5717-4562-b3fc-2c963f66afa6\"}}"
            try:
                r = requests.post(url, data=str(data), headers=headers)
                listBarcode.extend(r.json()['result']['barcodes'])
                if 'err barcode service' not in r.text:
                    break
            except:
                print(
                    'Ошибка получения ШК. count = {}, пытаюсь повторно получить.'.format(count))
                countTry += 1
                time.sleep(10)
                continue
    while True and countTry < 10:
        data = '(\"id\":1,\"jsonrpc\":\"2.0\",\"params\":(\"quantity\":{},\"supplierID\":\"3fa85f64-5717-4562-b3fc-2c963f66afa6\"))'
        try:
            r = requests.post(url, data=data.format(
                str(count)).replace('(', '{').replace(')', '}'), headers=headers)
            listBarcode.extend(r.json()['result']['barcodes'])
            if 'err barcode service' not in r.text:
                break
        except:
            print(
                'Ошибка получения ШК. count = {}, пытаюсь повторно получить.'.format(count))
            countTry += 1
            time.sleep(10)
            continue

    return listBarcode