from genericpath import isdir
from PIL import Image
import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__,'../../..')))
from my_mod.my_lib import file_exists, read_xlsx, multiReplace
import copy
import pandas
from os.path import isdir
import multiprocessing
from datetime import datetime
import requests
import time

diskWithPrint = 'F'
diskForTMP = 'E'
pathToMaskFolder = r'{}:\ForPrints\mask'.format(diskForTMP)
pathToPrintAll = r'{}:\Картинки китай\Под натяжку общее\Все'.format(diskWithPrint)
pathToPrintWithOutBack = r'{}:\Картинки китай\Под натяжку общее\Без фона'.format(diskWithPrint)
pathToDonePrints = r'{}:\ForPrints\printsPy'.format(diskForTMP)
lightPath = os.path.abspath(os.path.join(__file__,'..','light.png'))
pathToCategoryList = os.path.abspath(os.path.join(__file__,'..','cat.xlsx'))
reductionDict = {'закрытой камерой': 'зак.кам.',
                 'открытой камерой': 'отк.кам.',
                 'матовый': 'мат.',
                 'прозрачный': 'проз.',
                 'с силиконовым основанием': 'с сил. вставкой',
                 'противоударный': 'противоуд.',
                 'переливающиеся блестки': 'жидк. блестки',
                 'с усиленными углами': 'с усил.угл.',
                 'Чехол для': 'Чехол'}
reductionDict2 = {'Чехол для': 'Чехол'}
siliconCaseColorDict = {'белый': 'WHT',
                        'бирюзовый': 'TRQ',
                        'бледно-розовый': 'L-PNK',
                        'бордовый': 'VNS',
                        'голубой': 'SKB',
                        'желтый': 'YLW',
                        'зеленый': 'GRN',
                        'красный': 'RED',
                        'пудра': 'PWD',
                        'розовый': 'PNK',
                        'салатовый': 'L-GRN',
                        'светло-зеленый': 'L-GRN',
                        'светло-розовый': 'L-PNK',
                        'светло-фиолетовый': 'L-PPL',
                        'серый': 'GRY',
                        'синий': 'BLU',
                        'темно-синий': 'D-BLU',
                        'темно-сиреневый': 'D-LLC',
                        'фиолетовый': 'PPL',
                        'хаки': 'HCK',
                        'черный': 'BLC',
                        'прозрачный': 'CLR'
                        }
bookCaseColorDict = {'бордовый': 'VNS',
                     'бронзовый': 'BNZ',
                     'голубой': 'SKB',
                     'зеленый': 'GRN',
                     'золотой': 'GLD',
                     'красный': 'RED',
                     'розовое золото': 'P-GLD',
                     'серый': 'GRY',
                     'синий': 'BLU',
                     'черный': 'BLC'
                     }


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


def getBarcodForPrintMain(donePrint):
    if not file_exists(os.path.join(
            pathToDonePrints, donePrint + '.xlsx') if '.xlsx'not in donePrint else os.path.join(
            pathToDonePrints, donePrint)):
        excelWithPrint = []
        pathToPrint = os.path.join('D:\printsPy', donePrint)
        listPrint = os.listdir(pathToPrint)
        listBarcodes = generate_bar_WB(len(listPrint))
        for i, Print in enumerate(listPrint):
            data = {
                'Баркод': listBarcodes[i],
                'Группа': 'Чехол производство (принт)',
                'Основная характеристика': Print[0:-4],
                'Название 1С': multiReplace(donePrint, reductionDict),
                'Название полное': multiReplace(donePrint, reductionDict2),
                'Название полное с принтом': multiReplace(donePrint, reductionDict2) + ' ' + Print[0:-4],
                'Размер печать': ''
            }
            excelWithPrint.append(data)
        excelWithPrintpd = pandas.DataFrame(excelWithPrint)
        excelWithPrintpd.to_excel(os.path.join(
            pathToDonePrints, donePrint + '.xlsx'), index=False)


def genArtColor(nameCase, listNamePrint):
    listCase = []
    # узнаём тип чехла
    if 'книга' in nameCase:
        colorList = bookCaseColorDict
        artColor_1 = 'BK'
    else:
        colorList = siliconCaseColorDict
        artColor_1 = 'BP'
    # узнаём цвет чехла
    for color, codeColor in colorList.items():
        if color in nameCase:
            artColor_2 = codeColor
            break
        else:
            artColor_2 = 'UNKNOW_COLOR'
    if 'открытой камерой' in nameCase:
        artColor_3 = 'OCM'
    elif 'закрытой камерой' in nameCase:
        artColor_3 = 'CCM'
    else:
        artColor_3 = 'UCM'
    # узнаём в какие категории входит принт
    categoryList = read_xlsx(pathToCategoryList)
    for namePrint in listNamePrint:
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


def getBarcodForPrintWithCatMain(donePrint, reductionDict, reductionDict2):
    if not file_exists(os.path.join(
            pathToDonePrints, donePrint + '.xlsx') if '.xlsx'not in donePrint else os.path.join(
            pathToDonePrints, donePrint)):
        excelWithPrint = []
        pathToPrint = os.path.join(pathToDonePrints, donePrint)
        listPrint = genArtColor(donePrint, os.listdir(pathToPrint))
        listBarcodes = generate_bar_WB(len(listPrint))
        for i, Print in enumerate(listPrint):
            data = {
                'Баркод': listBarcodes[i],
                'Группа': 'Чехол производство (принт)',
                'Основная характеристика': Print['Принт'],
                'Название 1С': multiReplace(donePrint, reductionDict),
                'Название полное': multiReplace(donePrint, reductionDict2),
                'Название полное с принтом': multiReplace(donePrint, reductionDict2) + ' ' + Print['Принт'],
                'Размер печать': '',
                'Категория': Print['Категория'],
                'Код категории': Print['Код категории'],
                'Код цвета': Print['Код цвета'],
                'Артикул цвета': Print['Артикул цвета'],
                'Код камеры':Print['Код камеры'],
                'Рисунок':Print['Рисунок'],
                'Любимые герои': Print['Любимые герои']
            }
            excelWithPrint.append(data)
        excelWithPrintpd = pandas.DataFrame(excelWithPrint)
        excelWithPrintpd.to_excel(os.path.join(
            pathToDonePrints, donePrint + '.xlsx'), index=False)


def getBarcodForPrint(pathToDonePrints):
    pool = multiprocessing.Pool(6)
    for donePrint in os.listdir(pathToDonePrints):
        pool.apply_async(getBarcodForPrintWithCatMain,
                         args=(donePrint, reductionDict, reductionDict2,))
    pool.close()
    pool.join()


def getSizeAndPos(pathToMask):
    image = Image.open(pathToMask).convert("RGBA")
    size = image.size
    for xLeft in range(50, size[0]):

        rgba = image.getpixel((xLeft, 1700))
        if rgba[3] != 255:
            break
        xLeft += 1
    for xRight in reversed(range(size[0]-20)):
        rgba = image.getpixel((xRight, 1700))
        if rgba[3] != 255:
            break
        xRight += 1
    line = int((xRight - xLeft)/2) + xLeft
    for yTop in range(50, size[1]):
        rgba = image.getpixel((line, yTop))
        if rgba[3] != 255:
            break
        yTop += 1
    for yBott in reversed(range(size[1]-20)):
        rgba = image.getpixel((line, yBott))
        if rgba[3] != 255:
            break
        yBott += 1

    return (xLeft, xRight, yTop, yBott, size)


def isPrintWithoutBack(pathToPrint):
    if file_exists(pathToPrint.replace('PrintWithBack', 'PrintWithOutBack')):
        return False
    else:
        return True


def Rename_print(pathToPrint):
    listPrint = os.listdir(pathToPrint)
    for Print in listPrint:
        if "_" in Print:
            PrintN = Print.replace('print_', '(Принт ')[
                0:-4] + ')' if Print[-5] != ')' else Print.replace('print_', '(Принт ')[
                0:-4] + ''
        else:
            PrintN = Print.replace('print ', '(Принт ')[
                0:-4] + ')' if Print[-5] != ')' else Print.replace('print_', '(Принт ')[
                0:-4] + ''
        os.rename(os.path.join(pathToPrint, Print),
                  os.path.join(pathToPrint, PrintN+'.jpg'))


def makePrintMain(maskFolder, printList, light, pathToPrintFolder):
    lightNew = copy.copy(light)
    print(maskFolder)
    pathToBackground = os.path.join(
        pathToMaskFolder, maskFolder, r'fon.png')
    BackgroundImageOld = Image.open(pathToBackground)
    pathToMask = os.path.join(
        pathToMaskFolder, maskFolder, r'mask.png')
    maskImageOld = Image.open(pathToMask).convert("RGBA")
    maskImage = copy.copy(maskImageOld)
    maskImageOld.close()
    BackgroundImage = copy.copy(BackgroundImageOld)
    xLeft, xRight, yTop, yBott, size = getSizeAndPos(pathToMask)
    printsize = (xRight-xLeft, yBott-yTop)
    lighSize = (xRight-xLeft, yBott-yTop)
    printPaste = (xLeft, yTop)
    lighPaste = (xLeft, yTop)
    lightNew = lightNew.resize(lighSize)
    if not file_exists(os.path.join(pathToDonePrints, maskFolder)):
        os.makedirs(os.path.join(pathToDonePrints, maskFolder))
    for printPath in printList:
        BackgroundImage = copy.copy(BackgroundImageOld)
        pathToPrint = os.path.join(pathToPrintFolder, printPath)
        back = isPrintWithoutBack(pathToPrint)
        printImage = Image.open(pathToPrint).resize(printsize)
        BackgroundImage.paste(printImage, (printPaste), printImage)
        if back:
            BackgroundImage.paste(lightNew, (lighPaste), lightNew)
        printImage.close()
        BackgroundImage.paste(maskImage, (0, 0), maskImage)
        printDone = os.path.join(
            pathToDonePrints, maskFolder, printPath.replace('png', 'jpg'))
        BackgroundImage = BackgroundImage.convert('RGB')
        BackgroundImage = BackgroundImage.resize(
            (size[0]//3, size[1]//3))
        BackgroundImage.save(printDone,
                             quality=70)


def makePrint():
    maskFoldersList = os.listdir(pathToMaskFolder)
    pool = multiprocessing.Pool(6)
    light = Image.open(lightPath).convert("RGBA")
    for maskFolder in maskFoldersList:
        if "прозрачный" in maskFolder:
            pathToPrintFolder = pathToPrintAll
        else:
            pathToPrintFolder = pathToPrintWithOutBack
        printList = os.listdir(pathToPrintFolder)
        pool.apply_async(makePrintMain, args=(
            maskFolder, printList, light, pathToPrintFolder,))
    pool.close()
    pool.join()


def createAllCaseXLSX():
    allCaseList = []
    for file in os.listdir(pathToDonePrints):
        if '.xlsx' in file:
            allCaseList.extend(read_xlsx(os.path.join(
                pathToDonePrints, file), title='Yes'))
    allCaseListpd = pandas.DataFrame(allCaseList)
    allCaseListpd.to_excel(os.path.join(
        pathToDonePrints, 'AllCasePrint{}.xlsx'.format(datetime.today()).replace(':', '-')), index=False)


def main():
    #makePrint()
    for dirModel in os.listdir(pathToDonePrints):
        if isdir(os.path.join(pathToDonePrints, dirModel)):
            Rename_print(os.path.join(pathToDonePrints, dirModel))
    getBarcodForPrint(pathToDonePrints)
    createAllCaseXLSX()


if __name__ == '__main__':
    main()
