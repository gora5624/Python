from os import listdir
from os.path import join as joinPath, abspath, exists
import re
import shutil
import sys
sys.path.append(abspath(joinPath(__file__,'../..')))
sys.path.append(abspath(joinPath(__file__,'..')))
from my_mod.my_lib import  read_xlsx, multiReplace
from pandas import read_excel
import requests
import time
import pandas
import multiprocessing
from Folders import pathToDoneSiliconImageSilicon, pathToUploadWeb
from Class.MyClassForMakeImage import ModelWithAddin
from Class.ChekPhotoClass import ImageCheker
from shutil import copytree, ignore_patterns
# from Main import mameBookPrint
from Folders import pathToCategoryList, pathToUploadFolderLocal, pathToUploadSecondWeb, pathToUploadFolderLocal, pathToSecondImagesFolderSilicon, pathToSecondImageUploadFolder, pathToDoneSiliconImageSilicon, pathToUploadWeb, pathToDoneBookImageWithName, pathToTopPrint

TokenKar = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
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


def generateVendorCode(modelClass, colorCase, pathToImage):
    listImage = listdir(pathToImage)
    listCase = []
    if modelClass.caseType == 'Силикон':
        vendorCode1 = modelClass.model.replace(' ','_') + '_BP'
        if modelClass.cameraType == 'с закрытой камерой':
            vendorCode2 = 'CCM'
        elif modelClass.cameraType == 'с открытой камерой':
            vendorCode2 = 'OCM'
        else:
            vendorCode2 = 'UCM'
        for color, codeColor in siliconCaseColorDict.items():
            if color == colorCase.lower():
                vendorCode3 = codeColor
                break
        else:
            vendorCode3 = 'UNKNOW_COLOR'
        categoryList = read_xlsx(pathToCategoryList)
        for namePrint in listImage:
            for category in categoryList:
                if category['Принт'] == namePrint[0:-4]:
                    printNum = namePrint[0:-4].split(' ')[1][0:-1]
                    printNum = '0'*(4-len(printNum)) + printNum
                    vendorCode = [vendorCode1, vendorCode2, vendorCode3,
                                category['Код категории'], 'PRNT', printNum]
                    dataTMP = {'Принт': namePrint[0:-4],
                            'Категория': category['Категория'],
                            'Код категории': category['Код категории'],
                            'Артикул поставщика': '_'.join(vendorCode),
                            'Рисунок':category['Рисунок'],
                            'Любимые герои': category['Любимые герои'],
                            'Путь к картинке': joinPath(pathToImage,namePrint)}
                    listCase.append(dataTMP)
    elif modelClass.caseType == 'Книжки':
        vendorCode1 = modelClass.model.replace(' ','_') + '_BK'
        vendorCode2 = 'NTU'
        for color, codeColor in bookCaseColorDict.items():
            if color == colorCase.lower():
                vendorCode3 = codeColor
                break
        else:
            vendorCode3 = 'UNKNOW_COLOR'        
        categoryList = read_xlsx(pathToCategoryList)
        for namePrint in listImage:
            for category in categoryList:
                if category['Принт'] == namePrint[0:-4]:
                    printNum = namePrint[0:-4].split(' ')[1][0:-1]
                    printNum = '0'*(4-len(printNum)) + printNum
                    vendorCode = [vendorCode1, vendorCode2, vendorCode3,
                                category['Код категории'], 'PRNT', printNum]
                    dataTMP = {'Принт': namePrint[0:-4],
                            'Категория': category['Категория'],
                            'Код категории': category['Код категории'],
                            'Артикул поставщика': vendorCode,
                            'Рисунок':category['Рисунок'],
                            'Любимые герои': category['Любимые герои'],
                            'Путь к картинке': joinPath(pathToImage,namePrint)}
                    listCase.append(dataTMP)
    return listCase


def generate_bar_WB(count):
    listBarcode = []
    countTry = 0
    url = "https://suppliers-api.wildberries.ru/content/v1/barcodes"
    headers = {'Authorization': TokenArb}

    while count > 5000:
        count -= 5000
        while True and countTry < 10:
            json = {
                    "count": count
                    }
            try:
                r = requests.post(url, json=json, headers=headers)
                listBarcode.extend(r.json()['data'])
                if not r.json()['error']:
                    break
            except:
                print(
                    'Ошибка получения ШК. count = {}, пытаюсь повторно получить.'.format(count))
                print(r.rext)
                countTry += 1
                time.sleep(10)
                continue
    while True and countTry < 10:
        json = {
                    "count": count
                    }
        try:
            r = requests.post(url, json=json, headers=headers)
            listBarcode.extend(r.json()['data'])
            if not r.json()['error']:
                break
        except:
            print(
                'Ошибка получения ШК. count = {}, пытаюсь повторно получить.'.format(count))
            countTry += 1
            time.sleep(10)
            continue

    return listBarcode


def CreateExcelForFolder(modelClass=ModelWithAddin, topPrint=''):
    listColorpd = pandas.DataFrame(modelClass.data)
    if type(topPrint) == str:
        # a=len(listColorpd['Принт'])
        topPrint = pandas.DataFrame(pandas.read_excel(pathToTopPrint))[0:len(listColorpd['Принт'])]
    listColorpd = pandas.merge(listColorpd, topPrint, how='left', left_on='Принт', right_on='Принт')
    listColorpd.sort_values(by=['Позиция'], inplace=True)
    listColorpd.to_excel(joinPath(pathToDoneSiliconImageSilicon, modelClass.maskFolderName)+'.xlsx', index=False)


def CreateExcelForFolderNew(modelClass=ModelWithAddin, color=str, addImage=str):
    listColor = []
    model = modelClass.model
    pathToDone = pathToDoneSiliconImageSilicon if modelClass.caseType == 'Силикон' else pathToDoneBookImageWithName
    listVendorCode = generateVendorCode(modelClass, color, joinPath(pathToDone, model, color))
    listBarcodes = generate_bar_WB(len(listVendorCode))
    colorCase = color if color == 'прозрачный' else color + ' матовый'
    nameFor1C = 'Чехол {} силикон {} {}'.format(model, modelClass.cameraType, colorCase)
    for i, VendorCode in enumerate(listVendorCode):
        imageList = [VendorCode['Путь к картинке'].replace(pathToDone, pathToUploadWeb + '/Силикон').replace('\\','/')]
        if exists(joinPath(pathToSecondImagesFolderSilicon, model, color, '2.jpg')):
            imageList.append(joinPath(pathToSecondImagesFolderSilicon, model, color, '2.jpg').replace(pathToSecondImagesFolderSilicon, pathToUploadSecondWeb + '/Силикон').replace('\\','/'))
        elif exists(joinPath(pathToSecondImagesFolderSilicon, model, color, '3.jpg')):
            imageList.append(joinPath(pathToSecondImagesFolderSilicon, model, color, '3.jpg').replace(pathToSecondImagesFolderSilicon, pathToUploadSecondWeb + '/Силикон').replace('\\','/'))    
            # data = {
            #     'Номер карточки': cardNumber,
            #     'Категория': categoryCase,
            #     'Цвет': colorCase,
            #     'Баркод товара': barcodeCase,
            #     'Бренд': brandCase,
            #     'Наименование': nameCaseCase,
            #     'Цена': priceCase,
            #     'Артикул товара': articleCase,
            #     'Описание': descriptionCase,
            #     'Производитель телефона': madeByCase,
            #     'Назначение подарка': destenitionGiftCase,
            #     'Комплектация': equipmentCase,
            #     'Особенности чехла': specialCase,
            #     'Вид застежки': claspCase,
            #     'Рисунок': pictureCase,
            #     'Любимые герои': heroesCase,
            #     'Совместимость': compatibilityCase,
            #     'Тип чехлов': typeCase,
            #     'Модель': modelCase,
            #     'Повод': occasinCase,
            #     'Страна производства': countryManufactureCase,
            #     'Декоративные элементы': decorationCase,
            #     'Материал изделия': materialsCase,
            #     'Медиафайлы': pictureURLCase
            # }
        data = {'Баркод': listBarcodes[i],
                'Бренд': modelClass.brand,
                'Наименование': modelClass.name,
                'Розничная цена': modelClass.price,
                'Артикул поставщика': VendorCode['Артикул поставщика'],
                'Описание': modelClass.description,
                'Тнвэд': modelClass.TNVED,
                'Комплектация': modelClass.equipment,
                'Повод': modelClass.reason,
                'Особенности чехла': modelClass.special,
                'Вид застежки': modelClass.lock,
                'Рисунок': VendorCode['Рисунок'],
                'Любимые герои': VendorCode['Любимые герои'],
                'Совместимость': modelClass.compatibility,
                'Тип чехлов': modelClass.type,
                'Модель':modelClass.model,
                'Основная характеристика': VendorCode['Принт'],
                'Название 1С': multiReplace(nameFor1C, reductionDict),
                'Название полное': nameFor1C,
                'Название полное с принтом': nameFor1C + ' ' + VendorCode['Принт'],
                'Размер печать': '',
                'Путь к файлу': '#'.join(imageList)}
        listColor.append(data)
    listColorpd = pandas.DataFrame(listColor)
    listColorpd.to_excel(joinPath(pathToDone, model + ' ' + color)+'.xlsx', index=False)


def copyImage():
    copytree(pathToDoneSiliconImageSilicon, pathToUploadFolderLocal + r'\\Силикон', dirs_exist_ok=True, ignore=ignore_patterns('*.xlsx'))
    copytree(pathToSecondImagesFolderSilicon, pathToSecondImageUploadFolder + r'\\Силикон', dirs_exist_ok=True, ignore=ignore_patterns('*.xlsx'))



def createExcelSilicon(modelList, addImage):
    listModel = pandas.DataFrame()
    pool = multiprocessing.Pool(6)
    for model in modelList:
        for color in model.colorList:
            if '.xlsx' not in color:
                pool.apply_async(CreateExcelForFolder, args=(model,color,addImage, ))
    pool.close()
    pool.join()
    for folder in listdir(pathToDoneSiliconImageSilicon):
        if '.xlsx' in folder and '~' not in folder:
            listModel = pandas.concat([listModel,read_excel(joinPath(pathToDoneSiliconImageSilicon, folder))])
            #listModel['Путь к файлу']=listModel['Путь к файлу'].astype(str)
            #listImageAll.extend(listModel)
    #listImageAllpd = pandas.DataFrame(listImageAll)
    #listImageAllpd['Путь к файлу']=listImageAllpd['Путь к файлу'].astype(str)
    #listImageAll  = pandas.concat(listModel)
    #listImageAll['Путь к файлу']=listImageAll['Путь к файлу'].astype(str)
    #listModel['Путь к файлу']=listModel['Путь к файлу'].astype(str)
    writer = pandas.ExcelWriter(pathToDoneSiliconImageSilicon + r'.xlsx', engine='xlsxwriter',options={'strings_to_urls': False})
    listModel.to_excel(writer, index=False)
    writer.close()
    #listModel.to_excel(pathToDoneSiliconImageSilicon + '.xlsx', index=False)


def createExcelSiliconNew(modelList, addImage):
    listModel = pandas.DataFrame()
    pool = multiprocessing.Pool(6)
    for model in modelList:
        for color in model.colorList:
            if '.xlsx' not in color:
                pool.apply_async(CreateExcelForFolderNew, args=(model,color,addImage, ))
    pool.close()
    pool.join()
    for folder in listdir(pathToDoneSiliconImageSilicon):
        if '.xlsx' in folder and '~' not in folder:
            listModel = pandas.concat([listModel,read_excel(joinPath(pathToDoneSiliconImageSilicon, folder))])
            #listModel['Путь к файлу']=listModel['Путь к файлу'].astype(str)
            #listImageAll.extend(listModel)
    #listImageAllpd = pandas.DataFrame(listImageAll)
    #listImageAllpd['Путь к файлу']=listImageAllpd['Путь к файлу'].astype(str)
    #listImageAll  = pandas.concat(listModel)
    #listImageAll['Путь к файлу']=listImageAll['Путь к файлу'].astype(str)
    #listModel['Путь к файлу']=listModel['Путь к файлу'].astype(str)
    writer = pandas.ExcelWriter(pathToDoneSiliconImageSilicon + r'.xlsx', engine='xlsxwriter',options={'strings_to_urls': False})
    listModel.to_excel(writer, index=False)
    writer.close()
    #listModel.to_excel(pathToDoneSiliconImageSilicon + '.xlsx', index=False)


def chekImage(fileName, supplier, force):
    pathToFileForUpload = joinPath(pathToDoneSiliconImageSilicon, fileName)
    listCase = read_xlsx(pathToFileForUpload)
    a = ImageCheker(listCase, supplier)
    a.setImageForCards(force)
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