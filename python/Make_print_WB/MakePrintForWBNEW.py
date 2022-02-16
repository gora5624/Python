from genericpath import isdir
from PIL import Image
import os
from my_lib import file_exists, read_xlsx, multiReplace
import copy
import pandas
from os.path import isdir
import multiprocessing
from datetime import datetime
import requests
import time


pathToMaskFolder = r'D:\mask'
pathToPrintAll = r'G:\Картинки китай\Под натяжку общее\Все'
pathToPrintWithOutBack = r'G:\Картинки китай\Под натяжку общее\Без фона'
pathToDonePrints = r'D:\printsPy'
lightPath = r'D:\tmp\my_prod\Python\python\Make_print_WB\light.png'


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


def getBarcodForPrint(pathToDonePrints):
    #listCase = read_xlsx(r'D:\Список чехлов под печать.xlsx')
    pool = multiprocessing.Pool()
    for donePrint in os.listdir(pathToDonePrints):
        pool.apply_async(getBarcodForPrintMain,
                         args=(donePrint, ))
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

        PrintN = Print.replace('print_', '(Принт ')[
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
    pool = multiprocessing.Pool()
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
    # makePrint()
    for dirModel in os.listdir(pathToDonePrints):
        if isdir(os.path.join(pathToDonePrints, dirModel)):
            Rename_print(os.path.join(pathToDonePrints, dirModel))
    getBarcodForPrint(pathToDonePrints)
    createAllCaseXLSX()


if __name__ == '__main__':
    main()
