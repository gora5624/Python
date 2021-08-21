from os.path import join as joinpath
from datetime import datetime, timedelta
import requests
from my_lib import file_exists, read_xlsx
from os import makedirs
import pandas
from shutil import copyfile


main_path = r'C:\Users\Public\Documents\WBGetOrder'
Token_path = joinpath(main_path, r'Token.txt')
WBOrdersFileName = 'ФБС {} {} {}.xlsx'
WBOrdersData = joinpath(
    main_path, r'WBOrdersData')
WBErrorsFileName = r'ErrorsBarcod.xlsx'
WBOrdersDataFileName = 'orders.xlsx'
FilePath = joinpath(WBOrdersData, WBOrdersFileName)


def startChek():
    dirList = [main_path, WBOrdersData]
    for dir_ in dirList:
        if not file_exists(dir_):
            makedirs(dir_)
    if not file_exists(Token_path):
        print('Токен авторизации по адресу {} не обнаружен, получение заказов невозможно.'.format(
            Token_path))
        with open(Token_path, 'w', encoding='UTF-8') as file:
            file.close()


def recreate_data(CaseList):
    data_new = {}
    for line in CaseList:
        if type(line['Баркод']) == float:
            Barcod = str(line['Баркод'])[0:-2]
        else:
            Barcod = line['Баркод']
        data_new[Barcod] = {'Название 1С': line['Название 1С'],
                            'Код': line['Код'],
                            'Артикул WB':  str(line['Артикул WB'])[0:-2] if type(line['Артикул WB']) == float else line['Артикул WB'],
                            'Артикул поставщика': line['Артикул поставщика'],
                            'Код размера (chrt_id)': str(line['Код размера (chrt_id)'])[0:-2] if type(line['Код размера (chrt_id)']) == float else line['Код размера (chrt_id)'],
                            }
    return data_new


def createLineForExcel(line, caseData):
    barcod = line['barcode'] if type(
        line['barcode']) == str else str(line['barcode'])[0:-2]
    stiker = line['sticker']["wbStickerIdParts"]['A'] + \
        ' ' + line['sticker']["wbStickerIdParts"]['B']
    orderNum = line['orderId'] if type(
        line['orderId']) == str else str(line['orderId'])[0:-2]
    lineExcel = {'Название': caseData[barcod]['Название 1С'],
                 'Этикетка': stiker,
                 'Код': caseData[barcod]['Код'],
                 'ШК': barcod,
                 'Артикул поставщика': caseData[barcod]['Артикул поставщика'],
                 'Номер задания': orderNum}
    return lineExcel


def createFileName(FilePath, mode):
    numpiece = 1
    piece = " ч"+str(numpiece)
    if mode == 'case_print':
        nametmp = 'принты'
    elif mode == 'case_without_print':
        nametmp = 'без принтов'
    elif mode == 'glass':
        nametmp = 'стекла'
    elif mode == 'case_without_print':
        nametmp = 'без принтов'
    elif mode == 'planks':
        nametmp = 'планки принты'
    day = datetime.today().date().strftime(r"%d.%m.%Y")
    while file_exists(FilePath.format(nametmp, day, piece)):
        numpiece += 1
        piece = " ч"+str(numpiece)
    return FilePath.format(nametmp, day, piece)


def ChangeStatusOrder(dataorders, Token, mode):
    caseData = recreate_data(read_xlsx(r'D:\Список номенклатуры.XLSX'))
    countNewOrder, countPrint, countGlass, countPlanks, countWithOutPrint, CountplanksWithOutPrint, CountplanksPrint = 0, 0, 0, 0, 0, 0, 0
    data_new = []
    tmp = []
    data_errors = []
    errors_barcods = []
    for line in dataorders:
        try:
            if line['status'] == 0:
                barcod = line['barcode'] if type(
                    line['barcode']) == str else str(line['barcode'])[0:-2]
                countNewOrder += 1
                casePrint = "чехол" in caseData[barcod
                                                ]['Название 1С'].lower() and "принт" in caseData[barcod
                                                                                                 ]['Название 1С'].lower()
                caseWithOutPrint = "чехол" in caseData[barcod
                                                       ]['Название 1С'].lower() and "принт" not in caseData[barcod
                                                                                                            ]['Название 1С'].lower()
                glass = "стекло" in caseData[barcod
                                             ]['Название 1С'].lower() or "пленка" in caseData[barcod
                                                                                              ]['Название 1С'].lower()
                planksWithOutPrint = "планка" in caseData[barcod
                                                          ]['Название 1С'].lower() and "принт" not in caseData[barcod
                                                                                                               ]['Название 1С'].lower()
                planksPrint = "планка" in caseData[barcod
                                                   ]['Название 1С'].lower() and "принт" in caseData[barcod
                                                                                                    ]['Название 1С'].lower()
                orderId = line['orderId']
                if casePrint and mode == 'case_print':
                    countPrint += 1
                    lineExcel = createLineForExcel(line, caseData)
                    tmp.append(lineExcel)
                elif caseWithOutPrint and mode == 'case_without_print':
                    countWithOutPrint += 1
                    lineExcel = createLineForExcel(line, caseData)
                    tmp.append(lineExcel)
                elif glass and mode == 'glass':
                    countGlass += 1
                    lineExcel = createLineForExcel(line, caseData)
                    tmp.append(lineExcel)
                elif planksWithOutPrint and mode == 'case_without_print':
                    countWithOutPrint += 1
                    lineExcel = createLineForExcel(line, caseData)
                    tmp.append(lineExcel)
                elif planksPrint and mode == 'planks':
                    CountplanksPrint += 1
                    lineExcel = createLineForExcel(line, caseData)
                    tmp.append(lineExcel)
                casePrint = False
                caseWithOutPrint = False
                glass = False
                planksWithOutPrint = False
                planksPrint = False
        except KeyError:
            errors_barcods.append(barcod)
            continue
    data_new.extend(tmp)
    data_errors.extend(errors_barcods)
    data_errors = pandas.DataFrame(data_errors)
    data_new = pandas.DataFrame(data_new)
    data_errors.to_excel(joinpath(WBOrdersData,
                                  WBErrorsFileName), index=False)
    fileName = createFileName(FilePath, mode)
    data_new.to_excel(fileName, index=False)
    for lineTmp in tmp:
        orderId = lineTmp['Номер задания']
        changeStatus(orderId, Token)


def getToken():
    with open(Token_path, 'r', encoding='UTF-8') as file:
        Token = file.read()
        file.close()
    return Token


def choiseMode():
    print("Чтобы получить заказы без принтов, введите 1")
    print("Чтобы получить заказы с принтами, введите 2")
    print("Чтобы получить заказы стекла, введите 3")
    print("Чтобы получить заказы планки с принтами, введите 4")
    num = int(input())
    if num == 1:
        mode = 'case_without_print'
    elif num == 2:
        mode = 'case_print'
    elif num == 3:
        mode = 'glass'
    elif num == 4:
        mode = 'planks'
    else:
        print("Вы ввели неправильный режим.")
        return 100
    return mode


def get_orders(Token, days=4):
    print("Идёт получение свежих заказов, ожидайте...")
    Url = 'https://suppliers-api.wildberries.ru/api/v2/orders?date_start={}%2B03%3A00&take=1000&skip={}'

    start_data = (datetime.today() - timedelta(days=int(days))).isoformat('T', 'seconds').replace(
        ':', '%3A').replace('+', '%2B').replace('.', '%2E')
    count_skip = 0
    tmp = []
    dataorders = []
    flag = True
    while len(tmp) > 0 or flag:
        flag = False
        response = requests.get(Url.format(start_data, count_skip), headers={
            'Authorization': '{}'.format(Token)})
        if response.status_code != 200:
            print('Не удалось получить заказы, ошибка на стороне ВБ.')
            return 1
        count_skip = count_skip+1000
        tmp = response.json()['orders']
        dataorders.extend(tmp)
        for line in dataorders:
            line.update(wbStickerEncoded=line['sticker']['wbStickerEncoded'])
            line.update(
                wbStickerSvgBase64=line['sticker']['wbStickerSvgBase64'])
    all_data = pandas.DataFrame(dataorders)
    all_data.to_excel(joinpath(WBOrdersData,
                               WBOrdersDataFileName), index=False)
    return dataorders


def changeStatus(orderId, Token):
    Url = 'https://suppliers-api.wildberries.ru/api/v2/orders'
    datajson = [{"orderId": orderId,
                 "status": 0}]
    response = requests.put(Url, headers={
        'Authorization': '{}'.format(Token)}, json=datajson)
    print(response)


startChek()
Token = getToken()
data = get_orders(Token)
mode = choiseMode()
ChangeStatusOrder(data, Token, mode)
# a = input("Заказы получены, нажмите любую клавишу")
