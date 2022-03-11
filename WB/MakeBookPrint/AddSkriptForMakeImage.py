import multiprocessing
from os.path import abspath, join as joinPath, isdir, exists
from os import listdir, rename, remove
from shutil import rmtree
import sys
sys.path.append(abspath(joinPath(__file__,'../../..')))
import pandas
from my_mod.my_lib import  read_xlsx, multiReplace
import requests
import time


diskWithPrint = 'F'
pathToCategoryList = abspath(joinPath(__file__, '..', 'cat.xlsx'))
pathToBookPrint = r'{}:\Готовые картинки Fashion по моделям'.format(diskWithPrint)

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



def createModelExcel(model):
    modelForExcel = model.replace('&','/')
    for color in listdir(joinPath(pathToBookPrint, model)):
        if '.xlsx' in color:
            continue
        listColor = []
        RenameImage(joinPath(pathToBookPrint, model,color))
        listArt = genArtColor(color, listdir(joinPath(pathToBookPrint, model,color)))
        listBarcodes = generate_bar_WB(len(listArt))
        for i, art in enumerate(listArt):
            name = 'Чехол книга {} {} с силиконовый вставкой Fashion'.format(modelForExcel, color.lower())
            data = {'Баркод': listBarcodes[i],
                    'Группа': 'Чехол производство (принт)',
                    'Основная характеристика': art['Принт'],
                    'Название 1С': multiReplace(name, reductionDict),
                    'Название полное': name,
                    'Название полное с принтом': name + ' ' + art['Принт'],
                    'Размер печать': '',
                    'Категория': art['Категория'],
                    'Код категории': art['Код категории'],
                    'Код цвета': art['Код цвета'],
                    'Артикул цвета': art['Артикул цвета'],
                    'Код камеры':art['Код камеры'],
                    'Рисунок':art['Рисунок'],
                    'Любимые герои': art['Любимые герои']}
            listColor.append(data)
        listColorpd = pandas.DataFrame(listColor)
        listColorpd.to_excel(joinPath(pathToBookPrint, model,color)+'.xlsx', index=False)



def createExcel(resp):
    listImageAll = []
    pool = multiprocessing.Pool(6)
    for model in listdir(pathToBookPrint):
        if '.xlsx' in model:
            continue
        pool.apply_async(createModelExcel, args=(model,))
    pool.close()
    pool.join()
    for model in listdir(pathToBookPrint):
        if '.xlsx' in model:
            continue
        listModel = []
        for color in listdir(joinPath(pathToBookPrint, model)):
            if '.xlsx' in color:
                listColor = read_xlsx(joinPath(pathToBookPrint, model, color))
                listModel.extend(listColor)
        listModelpd = pandas.DataFrame(listModel)
        listModelpd.to_excel(joinPath(pathToBookPrint, model) + '.xlsx', index=False)
        listImageAll.extend(listModel)
    listImageAllpd = pandas.DataFrame(listImageAll)
    listImageAllpd.to_excel(pathToBookPrint + '.xlsx', index=False)
    resp.put(0)


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
    artColor_3 = 'NTU'
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




def deleteImage():
    for catalog in listdir(pathToBookPrint):
        if isdir(joinPath(pathToBookPrint,catalog)):
            # resp = 0
            # while resp != None:
            #     try:
            #         resp = removedirs(joinPath(pathToBookPrint,catalog))
            #     except OSError:
            #         for image in listdir(joinPath(pathToBookPrint,catalog)):
            #             remove(joinPath(pathToBookPrint,catalog,image))
            rmtree(joinPath(pathToBookPrint,catalog))
        else:
            remove(joinPath(pathToBookPrint,catalog))
    if exists(pathToBookPrint+'.xlsx'):
        remove(pathToBookPrint+'.xlsx')



def generate_bar_WB(count):
    listBarcode = []
    countTry = 0
    url = "https://suppliers-api.wildberries.ru/card/getBarcodes"
    headers = {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImEyNjQwNTAzLTk0NjktNGFkYy04MzVhLWM5MTQzZWU0NDBkYiJ9.UCh5I_5bnet0S2JcV92oDWS3p8RgUP5dsOwglCYu6ZE',
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