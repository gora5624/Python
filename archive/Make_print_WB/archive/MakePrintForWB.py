from genericpath import isdir
from PIL import Image
import os
from my_lib import file_exists, read_xlsx, generate_bar_WB
import copy
import pandas
from os.path import isdir
import multiprocessing
from datetime import datetime


Mode = 'All'
# Mode = 'WithOtBack'

pathToMaskFolder = r'D:\mask'
pathToPrintFolder = r'F:\китай png готово' if Mode == 'All' else r'D:\tmp\my_prod\Python\python\Make_print_WB\PrintWithOutBack'
pathToDonePrints = r'D:\printsPy'
lightPath = r'D:\tmp\my_prod\Python\python\Make_print_WB\light.png'


def getBarcodForPrintMain(donePrint):
    if not file_exists(os.path.join(
            pathToDonePrints, donePrint + '.xlsx') if '.xlsx'not in donePrint else os.path.join(
            pathToDonePrints, donePrint)):

        excelWithPrint = []
        # for case in listCase:
        #     if case['Наименование'].replace('\xa0', ' ') == donePrint:
        #         code1C = case['Код 1С']
        #         break
        #     else:
        code1C = None
        pathToPrint = os.path.join('D:\printsPy', donePrint)
        listPrint = os.listdir(pathToPrint)
        for Print in listPrint:
            data = {
                'Баркод': generate_bar_WB(),
                'Название 1С': donePrint + ' ' + Print[0:-4],
                'Код 1С': code1C,
                'Название принта': Print[0:-4]
            }
            excelWithPrint.append(data)
        excelWithPrintpd = pandas.DataFrame(excelWithPrint)
        excelWithPrintpd.to_excel(os.path.join(
            pathToDonePrints, donePrint + '.xlsx'), index=False, header=False)


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
    for xLeft in range(20, size[0]):

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
    for yTop in range(20, size[1]):
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
    # return (1200, 2200, 400, 2660, size)


def isPrintWithoutBack(pathToPrint):
    if file_exists(pathToPrint.replace('PrintWithBack', 'PrintWithOutBack')):
        return False
    else:
        return True


def Rename_print(pathToPrint):
    list_print_name = os.listdir(
        r'\\192.168.0.33\shared\Отдел производство\Wildberries\оригиналы принтов')
    listPrint = os.listdir(pathToPrint)
    for Print in listPrint:
        for name in list_print_name:
            PrintN = Print.replace('print', 'Принт')[0:-4]
            nameN = name[name.find('(')+1:name.find(')')]
            if PrintN == nameN:
                os.rename(os.path.join(pathToPrint, Print),
                          os.path.join(pathToPrint, name+'.jpg'))


def makePrintMain(maskFolder, printList, light):
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
    printList = os.listdir(pathToPrintFolder)
    pool = multiprocessing.Pool()
    light = Image.open(lightPath).convert("RGBA")
    for maskFolder in maskFoldersList:
        pool.apply_async(makePrintMain, args=(
            maskFolder, printList, light))
    pool.close()
    pool.join()


def createAllCaseXLSX():
    allCaseList = []
    for file in os.listdir(pathToDonePrints):
        if '.xlsx' in file:
            allCaseList.extend(read_xlsx(os.path.join(
                pathToDonePrints, file), title='No'))
    allCaseListpd = pandas.DataFrame(allCaseList)
    allCaseListpd.to_excel(os.path.join(
        pathToDonePrints, 'AllCasePrint{}.xlsx'.format(datetime.today()).replace(':', '-')), index=False, header=False)


def main():
    makePrint()
    for dirModel in os.listdir(pathToDonePrints):
        if isdir(os.path.join(pathToDonePrints, dirModel)):
            Rename_print(os.path.join(pathToDonePrints, dirModel))
    getBarcodForPrint(pathToDonePrints)
    createAllCaseXLSX()


# if __name__ == '__main__':
#     main()


def createAllCaseXLSX1():
    allCaseList = []
    pathToDonePrints = r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\Реестры ФБО'
    for file in os.listdir(pathToDonePrints):
        if '.xlsx' in file:
            allCaseList.extend(read_xlsx(os.path.join(
                pathToDonePrints, file), title='Yes'))
    allCaseListpd = pandas.DataFrame(allCaseList)
    allCaseListpd.to_excel(os.path.join(
        pathToDonePrints, 'AllCasePrint{}.xlsx'.format(datetime.today()).replace(':', '-')), index=False, header=False)


createAllCaseXLSX1()
