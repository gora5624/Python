from os.path import join as joinpath
from datetime import datetime, timedelta
import requests
from my_lib import file_exists, read_xlsx
from os import makedirs
import pandas


main_path = r'C:\Users\Public\Documents\WBGetOrder'
Token_path = joinpath(main_path, r'Token.txt')
WBOrdersFileName = 'ФБС {} {} {}.xlsx'
WBOrdersData = joinpath(
    main_path, r'WBOrdersData')
WBErrorsFileName = r'ErrorsBarcod.xlsx'
WBOrdersDataFileName = 'orders.xlsx'
listStuffPath = r'C:\Users\Public\Documents\WBGetOrder\TMPDir\Список номенклатуры.XLSX'
FilePath = joinpath(WBOrdersData, WBOrdersFileName)


def startChek():
    """Начальная проверка на наличие нужных каталогов"""
    dirList = [main_path, WBOrdersData]
    for dir_ in dirList:
        if not file_exists(dir_):
            makedirs(dir_)
    if not file_exists(Token_path):
        print('Токен авторизации по адресу {} не обнаружен, получение заказов невозможно.'.format(
            Token_path))
        with open(Token_path, 'w', encoding='UTF-8') as file:
            file.close()
        print('Файл для токена был создан, впишите его туда.')
        return 1
    return 0


def recreate_data(CaseList):
    """Создаём из простого списка товаров именованый список, для более удобного доступа по баркорду"""
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
    """Создаёт строку для записи в лист заказа нужного нам формата"""
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
                 'Количество': '1',
                 'Артикул поставщика': caseData[barcod]['Артикул поставщика'],
                 'Номер задания': orderNum}
    return lineExcel


def createFileName(FilePath, mode):
    """Создаёт правильное название файла под каждый заказ"""
    numpiece = 1
    piece = "ч"+str(numpiece)
    if mode == 'case_print':
        nametmp = 'принты'
    elif mode == 'case_without_print':
        nametmp = 'без принтов'
    elif mode == 'glass':
        nametmp = 'стекла'
    elif mode == 'case_without_print':
        nametmp = 'без принтов'
    elif mode == 'plankWithPrint':
        nametmp = 'планки принты'
    day = datetime.today().date().strftime(r"%d.%m.%Y")
    while file_exists(FilePath.format(nametmp, day, piece)):
        numpiece += 1
        piece = "ч"+str(numpiece)
    return FilePath.format(nametmp, day, piece)


def getGlassType(stuffNameIn1C):
    """Если в заказе стекло, определяем дополнительно какое это стекло для разделения"""
    if "наностекло" in stuffNameIn1C or "пленка" in stuffNameIn1C:
        if "матов" in stuffNameIn1C:
            GlassType = "nanoglassMate"
        elif "глянцев" in stuffNameIn1C:
            GlassType = "nanoglassClear"
        elif "камеру" in stuffNameIn1C:
            GlassType = "nanoglassCamera"
        else:
            GlassType = 0
    elif "Fullscreen" in stuffNameIn1C:
        GlassType = "glass3D"
    return GlassType


def getStuffType(barcodForGetType, caseData):
    """Определяем с каким товаром сейчас работаем, принты, не принты, стекло и т.п."""
    stuffType = 0
    stuffNameIn1C = caseData[barcodForGetType
                             ]['Название 1С'].lower()
    if "чехол" in stuffNameIn1C and "принт" in stuffNameIn1C:
        stuffType = 'caseWithPrint'
    elif "чехол" in stuffNameIn1C and "принт" not in stuffNameIn1C:
        stuffType = 'caseWithoutPrint'
    elif "планка" in stuffNameIn1C and "принт" not in stuffNameIn1C:
        stuffType = 'caseWithoutPrint'
    elif "стекло" in stuffNameIn1C or "пленка" in stuffNameIn1C:
        stuffType = 'glass'
    elif "планка" in stuffNameIn1C and "принт" in stuffNameIn1C:
        stuffType = 'plankWithPrint'
    return stuffType


def createExcel(listOrderForChangeStatus, listErrorBarcods, mode):
    if mode != 'glass':
        listErrorBarcods = pandas.DataFrame(listErrorBarcods)
        listOrderForChangeStatus = pandas.DataFrame(listOrderForChangeStatus)
        listErrorBarcods.to_excel(FilePath, index=False)
        fileName = createFileName(FilePath, mode)
        listOrderForChangeStatus.to_excel(fileName, index=False)
    elif mode == 'glass':
        listErrorBarcods = pandas.DataFrame(listErrorBarcods)
        listErrorBarcods.to_excel(FilePath, index=False)
        list3DGlass = []
        listClearNanoglass = []
        listMateNanoglass = []
        listCameraNanoglass = []
        for lineGlass in listOrderForChangeStatus:
            glassType = getGlassType(lineGlass['Название'])
            if glassType == 'glass3D':
                list3DGlass.append(lineGlass)
            elif glassType == 'nanoglassClear':
                listClearNanoglass.append(lineGlass)
            elif glassType == 'nanoglassMate':
                listMateNanoglass.append(lineGlass)
            elif glassType == 'nanoglassCamera':
                listCameraNanoglass.append(lineGlass)
        list3DGlass = pandas.DataFrame(list3DGlass)
        listClearNanoglass = pandas.DataFrame(listClearNanoglass)
        listMateNanoglass = pandas.DataFrame(listMateNanoglass)
        listCameraNanoglass = pandas.DataFrame(listCameraNanoglass)
        with pandas.ExcelWriter(createFileName(FilePath, mode)) as writerglass:
            list3DGlass.to_excel(
                writerglass, sheet_name='3D_стекла', index=False)
            listClearNanoglass.to_excel(
                writerglass, sheet_name='глянец', index=False)
            listMateNanoglass.to_excel(
                writerglass, sheet_name='матовые', index=False)
            listCameraNanoglass.to_excel(
                writerglass, sheet_name='камеры', index=False)


def orderFilter(ordersForFilter, mode):
    """Фильтруем заказы в соответствии с режимом на стекла, принты,не принты и планки с принтом"""
    caseData = recreate_data(read_xlsx(listStuffPath))
    listOrderForChangeStatus = []
    listErrorBarcods = []
    for lineOrdersForFilter in ordersForFilter:
        if lineOrdersForFilter['status'] == 0:

            try:
                stuffType = getStuffType(
                    lineOrdersForFilter['barcode'], caseData)
            except KeyError:
                listErrorBarcods.append(lineOrdersForFilter['barcode'])
                continue
            if stuffType == 'caseWithPrint' and mode == 'case_print':

                lineExcel = createLineForExcel(lineOrdersForFilter, caseData)
                listOrderForChangeStatus.append(lineExcel)

            elif stuffType == 'caseWithoutPrint' and mode == 'case_without_print':

                lineExcel = createLineForExcel(lineOrdersForFilter, caseData)
                listOrderForChangeStatus.append(lineExcel)

            elif stuffType == 'glass' and mode == 'glass':

                lineExcel = createLineForExcel(lineOrdersForFilter, caseData)
                listOrderForChangeStatus.append(lineExcel)

            elif stuffType == 'plankWithPrint' and mode == 'plankWithPrint':

                lineExcel = createLineForExcel(lineOrdersForFilter, caseData)
                listOrderForChangeStatus.append(lineExcel)

    createExcel(listOrderForChangeStatus, listErrorBarcods, mode)

    return listOrderForChangeStatus


def getToken():
    """Получаем токен для авторизации"""
    with open(Token_path, 'r', encoding='UTF-8') as file:
        Token = file.read()
        file.close()
    return Token


def choiseMode():
    """Выбор какие заказы получать"""
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
        mode = 'plankWithPrint'
    else:
        print("Вы ввели неправильный режим.")
        return 100
    return mode


def get_orders(Token, days=4):
    """Получает заказы за последние 4 дня"""
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


def changeStatus(listOrderForChangeStatus, Token):
    """Изменяет статус заказа на заданный, в данном случае "1" - на сборке"""
    for orderForChange in listOrderForChangeStatus:
        orderId = orderForChange['Номер задания']
        Url = 'https://suppliers-api.wildberries.ru/api/v2/orders'
        datajson = [{"orderId": orderId,
                     "status": 1}]
        while True:
            try:
                response = requests.put(Url, headers={
                    'Authorization': '{}'.format(Token)}, json=datajson)
                break
            except:
                continue
        print(response)


if startChek() == 0:
    Token = getToken()
    data = get_orders(Token)
    mode = choiseMode()
    #orderFilter(data, mode)
    changeStatus(orderFilter(data, mode), Token)
    a = input("Заказы получены, нажмите Enter")

#Token = getToken()
#changeStatus(read_xlsx(r"C:\Users\Public\Documents\WBGetOrder\WBOrdersData\ФБС принты 31.08.2021 ч3.xlsx"),Token)
