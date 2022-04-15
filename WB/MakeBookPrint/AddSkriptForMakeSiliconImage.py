

from os import listdir
from os.path import join as joinPath, abspath
import sys
sys.path.append(abspath(joinPath(__file__,'../../..')))
from my_mod.my_lib import  read_xlsx, multiReplace
import requests
import time
import pandas
import multiprocessing
from makeImageSilicon import pathToDoneSiliconImage


pathToCategoryList = abspath(joinPath(__file__, '..', 'cat.xlsx'))
siliconCaseColorDict = {'белый': 'WHT',
                        'светло-зеленый': 'L-GRN',
                        'светло-розовый': 'L-PNK',
                        'светло-фиолетовый': 'L-PPL',
                        'бледно-розовый': 'L-PNK',
                        'темно-синий': 'D-BLU',
                        'темно-сиреневый': 'D-LLC',
                        'бирюзовый': 'TRQ',
                        'бордовый': 'VNS',
                        'голубой': 'SKB',
                        'желтый': 'YLW',
                        'зеленый': 'GRN',
                        'красный': 'RED',
                        'пудра': 'PWD',
                        'розовый': 'PNK',
                        'салатовый': 'L-GRN',
                        'серый': 'GRY',
                        'синий': 'BLU',
                        'фиолетовый': 'PPL',
                        'хаки': 'HCK',
                        'черный': 'BLC',
                        'прозрачный': 'CLR',
                        'проз': 'CLR'
                        }
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


def genArtColor(folder, listImage):
    listCase = []
    artColor_1 = 'BP'
    # узнаём цвет чехла
    for color, codeColor in siliconCaseColorDict.items():
        if color in folder:
            artColor_2 = codeColor
            break
        else:
            artColor_2 = 'UNKNOW_COLOR'
    if 'открытой камерой' in folder or 'отк.кам.' in folder:
        artColor_3 = 'OCM'
    elif 'закрытой камерой' in folder or 'зак.кам.' in folder:
        artColor_3 = 'CCM'
    else:
        artColor_3 = 'UCM'
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
                           'Код цвета': artColor_2,
                           'Код камеры': artColor_3,
                           'Рисунок':category['Рисунок'],
                           'Любимые герои': category['Любимые герои']}
                listCase.append(dataTMP)
    return listCase


def generate_bar_WB(count):
    listBarcode = []
    countTry = 0
    url = "https://suppliers-api.wildberries.ru/card/getBarcodes"
    headers = {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w',
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
                print(r.rext)
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


def CreateExcelForFolder(pathToDoneSiliconImage,folder):
    modelForExcel = folder.replace('&','/')
    listColor = []
    listArt = genArtColor(folder, listdir(joinPath(pathToDoneSiliconImage, folder)))
    listBarcodes = generate_bar_WB(len(listArt))
    for i, art in enumerate(listArt):
        data = {'Баркод': listBarcodes[i],
                'Группа': 'Чехол производство (принт)',
                'Основная характеристика': art['Принт'],
                'Название 1С': multiReplace(folder, reductionDict),
                'Название полное': folder,
                'Название полное с принтом': folder + ' ' + art['Принт'],
                'Размер печать': '',
                'Категория': art['Категория'],
                'Код категории': art['Код категории'],
                'Код цвета': art['Код цвета'],
                'Артикул цвета': art['Артикул цвета'],
                'Код камеры':art['Код камеры'],
                'Рисунок':art['Рисунок'],
                'Любимые герои': art['Любимые герои'],
                'Модель': modelForExcel,
                'Путь к файлу': joinPath(pathToDoneSiliconImage, folder,art['Принт']+'.jpg')}
        listColor.append(data)
    listColorpd = pandas.DataFrame(listColor)
    listColorpd.to_excel(joinPath(pathToDoneSiliconImage,folder)+'.xlsx', index=False)
    print(joinPath(pathToDoneSiliconImage,folder)+'.xlsx')


def createExcelSilicon():
    listImageAll = []
    pool = multiprocessing.Pool(6)
    for model in listdir(pathToDoneSiliconImage):
        if '.xlsx' in model:
            continue
        pool.apply_async(CreateExcelForFolder, args=(pathToDoneSiliconImage,model,))
    pool.close()
    pool.join()
    print('1')
    for folder in listdir(pathToDoneSiliconImage):
        if '.xlsx' in folder:
            listModel = read_xlsx(joinPath(pathToDoneSiliconImage, folder))
            listImageAll.extend(listModel)
    listImageAllpd = pandas.DataFrame(listImageAll)
    listImageAllpd.to_excel(pathToDoneSiliconImage + '.xlsx', index=False)


def copyImage():
    pass