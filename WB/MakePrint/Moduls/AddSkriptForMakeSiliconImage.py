from os import listdir
from os.path import join as joinPath, abspath, exists
import re
import shutil
import sys
sys.path.append(abspath(joinPath(__file__,'../..')))
from my_mod.my_lib import  read_xlsx, multiReplace
import requests
import time
import pandas
import multiprocessing
from Folders import pathToDoneSiliconImageSilicon, pathToUploadWeb
from Class.MyClassForMakeImage import ModelWithAddin
from shutil import copytree, ignore_patterns
from Class.ChekPhotoClass import ImageCheker
from Folders import pathToCategoryList, pathToUploadFolderLocal, pathToUploadSecondWeb, pathToUploadFolderLocal, pathToSecondImagesFolderSilicon, pathToSecondImageUploadFolder, pathToDoneSiliconImageSilicon, pathToUploadWeb

TokenKar = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
TokenArb = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
markerForAllModel = 'Применить для всех'
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


def genArtColor(modelClass, colorCase, pathToImage):
    listImage = listdir(pathToImage)
    listCase = []
    artColor_1 = 'BP'
    # узнаём цвет чехла
    for color, codeColor in siliconCaseColorDict.items():
        if color == colorCase.lower():
            artColor_2 = codeColor
            break
        else:
            artColor_2 = 'UNKNOW_COLOR'
    if modelClass.cameraType == 'с закрытой камерой':
        artColor_3 = 'OCM'
    elif modelClass.cameraType == 'с открытой камерой':
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
                           'Любимые герои': category['Любимые герои'],
                           'Путь к картинке': joinPath(pathToImage,namePrint)}
                listCase.append(dataTMP)
    return listCase


def generate_bar_WB(count):
    listBarcode = []
    countTry = 0
    url = "https://suppliers-api.wildberries.ru/card/getBarcodes"
    headers = {'Authorization': TokenKar,
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


def CreateExcelForFolder(modelClass=ModelWithAddin, color=str):
    listColor = []
    model = modelClass.model
    listArt = genArtColor(modelClass, color, joinPath(pathToDoneSiliconImageSilicon, model, color))
    listBarcodes = generate_bar_WB(len(listArt))
    cameraType = modelClass.cameraType
    colorCase = color if color == 'прозрачный' else color + ' матовый'
    nameFor1C = 'Чехол {} силикон {} {}'.format(model, cameraType, colorCase)
    for i, art in enumerate(listArt):
        imageList = [art['Путь к картинке'].replace(pathToDoneSiliconImageSilicon, pathToUploadWeb + '/Силикон').replace('\\','/')]
        if exists(joinPath(pathToSecondImagesFolderSilicon, model, color, '2.jpg')):
            imageList.append(joinPath(pathToSecondImagesFolderSilicon, model, color, '2.jpg').replace(pathToSecondImagesFolderSilicon, pathToUploadSecondWeb + '/Силикон').replace('\\','/'))
        data = {'Баркод': listBarcodes[i],
                'Бренд': modelClass.brand,
                'Наименование': modelClass.name,
                'Розничная цена': modelClass.price,
                'Артикул поставщика': '_'.join([model.replace(' ','_'),'PRNT',art['Код цвета'], art['Код камеры'],art['Код категории']]),
                'Артикул цвета': art['Артикул цвета'],
                'Описание': modelClass.description,
                'Тнвэд': modelClass.TNVED,
                'Комплектация': modelClass.equipment,
                'Повод': modelClass.reason,
                'Особенности чехла': modelClass.special,
                'Вид застежки': modelClass.lock,
                'Рисунок': art['Рисунок'],
                'Любимые герои': art['Любимые герои'],
                'Совместимость': modelClass.compatibility,
                'Тип чехлов': modelClass.type,
                'Модель':modelClass.model,
                'Основная характеристика': art['Принт'],
                'Название 1С': multiReplace(nameFor1C, reductionDict),
                'Название полное': nameFor1C,
                'Название полное с принтом': nameFor1C + ' ' + art['Принт'],
                'Размер печать': '',
                'Путь к файлу': '#'.join(imageList)}
        if art['Артикул цвета']=='BP_SKB_TXT_PRNT_0010':
            print(art['Артикул цвета'])
        listColor.append(data)
    listColorpd = pandas.DataFrame(listColor)
    listColorpd.to_excel(joinPath(pathToDoneSiliconImageSilicon, model + ' ' + color)+'.xlsx', index=False)


def copyImage():
    copytree(pathToDoneSiliconImageSilicon, pathToUploadFolderLocal + r'\\Силикон', dirs_exist_ok=True, ignore=ignore_patterns('*.xlsx'))
    copytree(pathToSecondImagesFolderSilicon, pathToSecondImageUploadFolder + r'\\Силикон', dirs_exist_ok=True, ignore=ignore_patterns('*.xlsx'))



def createExcelSilicon(modelList):
    listImageAll = []
    pool = multiprocessing.Pool(6)
    for model in modelList:
        for color in model.colorList:
            pool.apply_async(CreateExcelForFolder, args=(model,color,))
    pool.close()
    pool.join()
    for folder in listdir(pathToDoneSiliconImageSilicon):
        if '.xlsx' in folder and '~' not in folder:
            listModel = read_xlsx(joinPath(pathToDoneSiliconImageSilicon, folder))
            listImageAll.extend(listModel)
    listImageAllpd = pandas.DataFrame(listImageAll)
    listImageAllpd.to_excel(pathToDoneSiliconImageSilicon + '.xlsx', index=False)


def chekImage(fileName, supplier):
    pathToFileForUpload = joinPath(pathToDoneSiliconImageSilicon, fileName)
    listCase = read_xlsx(pathToFileForUpload)
    a = ImageCheker(listCase, supplier)
    a.setImageForCards()
    a.updateCardsStart()
    return a.status


if __name__ == '__main__':
    listImageAll = []
    pathToDoneSiliconImageSilicon = r'F:\Для загрузки\Готовые принты\Силикон'
    for folder in listdir(pathToDoneSiliconImageSilicon):
        if '.xlsx' in folder and '~' not in folder:
            listModel = read_xlsx(joinPath(pathToDoneSiliconImageSilicon, folder))
            listImageAll.extend(listModel)
    listImageAllpd = pandas.DataFrame(listImageAll)
    listImageAllpd.to_excel(pathToDoneSiliconImageSilicon + '.xlsx', index=False)