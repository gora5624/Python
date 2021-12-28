from os.path import join as joinpath
from datetime import datetime, timedelta
import requests
from my_lib import file_exists, read_xlsx
from os import makedirs
import pandas
from shutil import copyfile
import xlrd
import multiprocessing
from PrintStikersAutoArgs import main as printStiker
from PrintStikersAutoArgs import TMPDir
from os import remove, listdir

# Режим отладки 1 - да, 0 - боевой режим
Debug = 1

stopList = ['2009539898001', '2009539892009', '2009539656007',
            '2009539490007', '2009539287003', '2009538490008']

main_path = r'C:\Users\Public\Documents\WBGetOrder'
WBOrdersFileName = 'ФБС {} {} {}.xlsx' if Debug == 0 else 'DEBUG_ФБС {} {} {}.xlsx'
newOrderPath = joinpath(
    r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\Новые', WBOrdersFileName)
inWorkOrderPath = joinpath(
    r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\В работе', WBOrdersFileName)
doneOrderPath = joinpath(
    r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\Отработано', WBOrdersFileName)
Token_path = joinpath(main_path, r'Token.txt')
WBOrdersData = joinpath(
    main_path, r'WBOrdersData')
WBErrorsFileName = r'ErrorsBarcod.xlsx'
WBOrdersDataFileName = 'orders.xlsx'
listStuffPath = r'C:\Users\Public\Documents\WBGetOrder\TMPDir\Список номенклатуры — копия.XLSX'
FilePath = joinpath(WBOrdersData, WBOrdersFileName)
sizeListPath = r'\\192.168.0.33\shared\Отдел производство\Wildberries\список печати.xlsx'
OrderDir = r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\Новые'
pathToMakePrint = r'D:\tmp\my_prod\Python\python\WB_API\PrintStikersAutoArgs.py'
nowFileName = []


def startChek():
    """Начальная проверка на наличие нужных каталогов"""
    dirList = [main_path, WBOrdersData]
    if Debug == 1:
        print('ВНИМАНИЕ, ВКЛЮЧЁН РЕЖИМ ОТЛАДКИ')
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

        data_new[Barcod] = {'Название 1С': line['Название 1С'].replace('\xa0', ' ') if type(line['Название 1С']) == str else None,
                            'Код': line['Код'].replace('\xa0', '') if type(line['Код']) == str else None,
                            'Артикул WB':  str(line['Артикул WB'])[0:-2] if type(line['Артикул WB']) == float else line['Артикул WB'],
                            'Артикул поставщика': line['Артикул поставщика'],
                            'Код размера (chrt_id)': str(line['Код размера (chrt_id)'])[0:-2] if type(line['Код размера (chrt_id)']) == float else line['Код размера (chrt_id)'],
                            }
    return data_new


def read_xlsx_by_name(file_path, nameList):
    '''Считывает построчно xlsx файл и возращает список словарей - если title = 'Yes', список списков - если title = 'No'
    '''
    rd = xlrd.open_workbook(file_path)
    try:
        sheet = rd.sheet_by_name(nameList)
    except:
        sheet = rd.sheet_by_name('основной')
    try:
        Name_row = sheet.row_values(0)
    except IndexError:
        return None
    start = 1
    data = []
    for rownum in range(start, sheet.nrows):
        row = sheet.row_values(rownum)
        dct = {}
        for i, cel in enumerate(row):
            tmp = {Name_row[i]: cel}
            dct.update(tmp)
        data.append(dct)
    return data


def createLineForExcel(line, caseData):
    """Создаёт строку для записи в лист заказа нужного нам формата"""
    barcod = line['barcode'] if type(
        line['barcode']) == str else str(line['barcode'])[0:-2]
    orderNum = line['orderId'] if type(
        line['orderId']) == str else str(line['orderId'])[0:-2]
    # stiker = getStiker(orderNum)["wbStickerIdParts"]['A'] + \
    #     ' ' + getStiker(orderNum)["wbStickerIdParts"]['B']
    lineExcel = {'Название': caseData[barcod]['Название 1С'],
                 #  'Этикетка': stiker,
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
    while file_exists(FilePath.format(nametmp, day, piece)) or file_exists(newOrderPath.format(nametmp, day, piece)) or file_exists(inWorkOrderPath.format(nametmp, day, piece)) or file_exists(doneOrderPath.format(nametmp, day, piece)):
        numpiece += 1
        piece = "ч"+str(numpiece)
    print(FilePath.format(nametmp, day, piece))
    global nowFileName
    if "ФБС принты" not in FilePath.format(nametmp, day, piece):
        nowFileName.append(FilePath.format(nametmp, day, piece))
    return FilePath.format(nametmp, day, piece)


def getCountGlass(stuffNameIn1C):
    try:
        komplect = stuffNameIn1C.split(':')[0]
    except:
        return 1
    for let in komplect:
        try:
            return int(let)
        except:
            continue
    return 1


def getGlassType(stuffNameIn1C):
    """Если в заказе стекло, определяем дополнительно какое это стекло для разделения"""
    countGlass = getCountGlass(stuffNameIn1C)
    if "наностекло" in stuffNameIn1C or "пленка" in stuffNameIn1C:
        if "матов" in stuffNameIn1C:
            GlassType = "nanoglassMate"
        elif "глянцев" in stuffNameIn1C:
            GlassType = "nanoglassClear"
        elif "камеру" in stuffNameIn1C:
            GlassType = "nanoglassCamera"
        else:
            GlassType = 0
    elif ("Fullscreen" in stuffNameIn1C) or ('3D' in stuffNameIn1C) or ('керамич' in stuffNameIn1C):
        GlassType = "glass3D"
    return GlassType, countGlass


def getStuffType(barcodForGetType, caseData):
    """Определяем с каким товаром сейчас работаем, принты, не принты, стекло и т.п."""

    stuffType = 0
    try:
        stuffNameIn1C = caseData[barcodForGetType
                                 ]['Название 1С'].lower()
    except:
        return stuffType
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


def getSize(model):
    sizeList = read_xlsx(sizeListPath)
    for modelLine in sizeList:
        if modelLine['Название модели в 1С'].lower().replace('\\', '').replace('/', '') == model.lower().replace('\\', '').replace('/', ''):
            return modelLine['Типоразмер']
    return 'Нет в списке размеров'


def createNormalFromPrint(listOrderForChangeStatus):
    dataForOrder = []
    for orderLine in listOrderForChangeStatus:
        if 'прозрачный' in orderLine['Название'].lower():
            normalCase1pt = orderLine['Название'].split('прозрачный')[
                0]
            normalCase = normalCase1pt + 'прозрачный'
            dataForOrdertmp = {'Название': normalCase}
        elif 'матовый' in orderLine['Название'].lower():
            normalCase1pt = orderLine['Название'].split('матовый')[0]
            normalCase = normalCase1pt + 'матовый'
            dataForOrdertmp = {'Название': normalCase}
        elif 'блестки' in orderLine['Название'].lower():
            normalCase1pt = orderLine['Название'].split('блестки')[0]
            normalCase = normalCase1pt + 'блестки'
            dataForOrdertmp = {'Название': normalCase}
        elif 'skinshell' in orderLine['Название'].lower():
            normalCase1pt = orderLine['Название'].split('SkinShell')[0]
            normalCase = normalCase1pt + 'skinshell'
            dataForOrdertmp = {'Название': normalCase}
        elif 'fashion' in orderLine['Название'].lower():
            normalCase1pt = orderLine['Название'].split('Fashion')[0]
            normalCase = normalCase1pt + 'Fashion'
            dataForOrdertmp = {'Название': normalCase}
        elif 'df' in orderLine['Название'].lower():
            normalCase1pt = orderLine['Название'].split('DF')[0]
            normalCase = normalCase1pt + 'DF'
            dataForOrdertmp = {'Название': normalCase}
        dataForOrder.append(dataForOrdertmp)
    return dataForOrder


def createlineForOrderGlass(listOrderForChangeStatus):
    lineForOrderGlass = []
    for lineGlass in listOrderForChangeStatus:
        glassType, countGlass = getGlassType(lineGlass['Название'])
        if glassType == 'glass3D':
            nameGlassNew = lineGlass['Название'].split('для ')[1]
            data = {'Название': nameGlassNew,
                    'Количество': countGlass}
            lineForOrderGlass.append(data)
    return lineForOrderGlass


def createPrintExcel(listOrderForChangeStatus, fileName):
    listOrderForChangeStatuspd = pandas.DataFrame(listOrderForChangeStatus)
    listOrderForChangeOrders = createNormalFromPrint(
        listOrderForChangeStatus)
    listOrderForChangeOrderspd = pandas.DataFrame(listOrderForChangeOrders)
    listOrderForTable = []
    for orderLine in listOrderForChangeStatus:
        if 'книга' not in orderLine['Название']:
            model = orderLine['Название'].split('для ')[1].split(' сил')[0]
            size = getSize(model)
        elif 'книга' in orderLine['Название']:
            size = 'Книга'
        OrderLineData = {
            'Номер задания': orderLine['Номер задания'],
            'Название': orderLine['Название'],
            'Размер': size}
        # 'Этикетка': orderLine['Этикетка']}
        listOrderForTable.append(OrderLineData)
    listOrderForTablepd = pandas.DataFrame(listOrderForTable)
    with pandas.ExcelWriter(fileName) as writerCase:
        listOrderForChangeStatuspd.sort_values(
            'Название').to_excel(writerCase, sheet_name='основной', index=False)
        listOrderForTablepd.sort_values(
            'Название').to_excel(writerCase, sheet_name='Столы', index=False)
        listOrderForChangeOrderspd.groupby(['Название']).size().reset_index(name='Количество').to_excel(
            writerCase, sheet_name='Заказать', index=False)


def createExcel(listOrderForChangeStatus, listErrorBarcods, mode):
    if mode != 'glass':
        listErrorBarcods = pandas.DataFrame(listErrorBarcods)
        listOrderForChangeStatuspd = pandas.DataFrame(listOrderForChangeStatus)
        listOrderForOrder = pandas.DataFrame(listOrderForChangeStatus)
        listErrorBarcods.to_excel(FilePath, index=False)
        fileName = createFileName(FilePath, mode)
        if mode == 'case_without_print':
            with pandas.ExcelWriter(fileName) as writerCase:
                listOrderForChangeStatuspd.sort_values(
                    'Название').to_excel(writerCase, sheet_name='основной', index=False)
                listOrderForOrder.groupby(['Название', 'ШК']).size().reset_index(name='Количество').to_excel(
                    writerCase, sheet_name='Заказать', index=False)
        elif mode == 'case_print':
            createPrintExcel(listOrderForChangeStatus, fileName)
        elif mode == 'plankWithPrint':
            with pandas.ExcelWriter(fileName) as writerCase:
                listOrderForChangeStatuspd.sort_values(
                    'Название').to_excel(writerCase, sheet_name='основной', index=False)

    elif mode == 'glass':
        listErrorBarcods = pandas.DataFrame(listErrorBarcods)
        listErrorBarcods.to_excel(FilePath, index=False)
        list3DGlass = []
        listClearNanoglass = []
        listMateNanoglass = []
        listCameraNanoglass = []
        for lineGlass in listOrderForChangeStatus:
            glassType, countGlass = getGlassType(lineGlass['Название'])
            if glassType == 'glass3D':
                lineGlass['Количество'] = countGlass
                list3DGlass.append(lineGlass)
            elif glassType == 'nanoglassClear':
                lineGlass['Количество'] = countGlass
                listClearNanoglass.append(lineGlass)
            elif glassType == 'nanoglassMate':
                lineGlass['Количество'] = countGlass
                listMateNanoglass.append(lineGlass)
            elif glassType == 'nanoglassCamera':
                lineGlass['Количество'] = countGlass
                listCameraNanoglass.append(lineGlass)
        listForOrder3D = createlineForOrderGlass(listOrderForChangeStatus)
        listForOrder3Dpd = pandas.DataFrame(listForOrder3D)
        list3DGlass = pandas.DataFrame(list3DGlass)
        listClearNanoglass = pandas.DataFrame(listClearNanoglass)
        listMateNanoglass = pandas.DataFrame(listMateNanoglass)
        listCameraNanoglass = pandas.DataFrame(listCameraNanoglass)
        fileName = createFileName(FilePath, mode)
        with pandas.ExcelWriter(fileName) as writerglass:
            try:
                listForOrder3Dpd.groupby(['Название']).sum().reset_index().to_excel(
                    writerglass, sheet_name='Заказ_3D', index=False)
            except KeyError:
                listForOrder3Dpd.to_excel(
                    writerglass, sheet_name='Заказ_3D', index=False)
            try:
                list3DGlass.sort_values(
                    'Название').to_excel(
                    writerglass, sheet_name='3D_стекла', index=False)
            except KeyError:
                list3DGlass.to_excel(
                    writerglass, sheet_name='3D_стекла', index=False)
            try:
                listClearNanoglass.sort_values(
                    'Название').to_excel(
                    writerglass, sheet_name='глянец', index=False)
            except KeyError:
                listClearNanoglass.to_excel(
                    writerglass, sheet_name='глянец', index=False)
            try:
                listMateNanoglass.sort_values(
                    'Название').to_excel(
                    writerglass, sheet_name='матовые', index=False)
            except KeyError:
                listMateNanoglass.to_excel(
                    writerglass, sheet_name='матовые', index=False)
            try:
                listCameraNanoglass.sort_values(
                    'Название').to_excel(
                    writerglass, sheet_name='камеры', index=False)
            except KeyError:
                listCameraNanoglass.to_excel(
                    writerglass, sheet_name='камеры', index=False)
    if Debug != 1:
        copyfile(fileName, fileName.replace(WBOrdersData, OrderDir))


def orderFilter(ordersForFilter, mode):
    """Фильтруем заказы в соответствии с режимом на стекла, принты,не принты и планки с принтом"""
    caseData = recreate_data(read_xlsx(listStuffPath))
    listOrderForChangeStatus = []
    listErrorBarcods = []

    for lineOrdersForFilter in ordersForFilter:
        if lineOrdersForFilter['barcode'] in stopList:
            continue
        if lineOrdersForFilter['status'] == 0:

            try:
                stuffType = getStuffType(
                    lineOrdersForFilter['barcode'], caseData)
            except KeyError:
                listErrorBarcods.append(lineOrdersForFilter['barcode'])
                continue
            if stuffType == 0:
                listErrorBarcods.append(lineOrdersForFilter['barcode'])
                continue

            if stuffType == 'caseWithPrint' and mode == 'case_print':

                lineExcel = createLineForExcel(lineOrdersForFilter, caseData)
                listOrderForChangeStatus.append(lineExcel)
                continue

            elif stuffType == 'caseWithoutPrint' and mode == 'case_without_print':

                lineExcel = createLineForExcel(lineOrdersForFilter, caseData)
                listOrderForChangeStatus.append(lineExcel)
                continue

            elif stuffType == 'glass' and mode == 'glass':

                lineExcel = createLineForExcel(lineOrdersForFilter, caseData)
                listOrderForChangeStatus.append(lineExcel)
                continue

            elif stuffType == 'plankWithPrint' and mode == 'plankWithPrint':

                lineExcel = createLineForExcel(lineOrdersForFilter, caseData)
                listOrderForChangeStatus.append(lineExcel)
                continue

    if mode != 'glass':
        splitOrders(listOrderForChangeStatus, listErrorBarcods)
    else:
        createExcel(listOrderForChangeStatus, listErrorBarcods, mode)

    return listOrderForChangeStatus


def normalNameForSplit(order):
    if 'прозрачный' in order['Название'].lower():
        normalCase1pt = order['Название'].split('прозрачный')[
            0]
        normalCase = normalCase1pt + 'прозрачный'
    elif 'матовый' in order['Название'].lower():
        normalCase1pt = order['Название'].split('матовый')[0]
        normalCase = normalCase1pt + 'матовый'
    elif 'блестки' in order['Название'].lower():
        normalCase1pt = order['Название'].split('блестки')[0]
        normalCase = normalCase1pt + 'блестки'
    elif 'skinshell' in order['Название'].lower():
        normalCase1pt = order['Название'].split('SkinShell')[0]
        normalCase = normalCase1pt + 'skinshell'
    elif 'fashion' in order['Название'].lower():
        normalCase1pt = order['Название'].split('Fashion')[0]
        normalCase = normalCase1pt + 'Fashion'
    elif 'df' in order['Название'].lower():
        normalCase1pt = order['Название'].split('DF')[0]
        normalCase = normalCase1pt + 'DF'
    else:
        normalCase = order['Название']
    return normalCase


def splitOrders(listOrderForChangeStatus, listErrorBarcods):
    countOrder = len(listOrderForChangeStatus)
    print(countOrder)
    countOrdersFiles = 1
    while 60 <= countOrder // countOrdersFiles >= 90:
        countOrdersFiles += 1
    orders = []
    i = 0
    pdtmp = pandas.DataFrame(listOrderForChangeStatus).sort_values('Название')
    listOrderForChangeStatus = pdtmp.to_dict(orient='records')
    for order in listOrderForChangeStatus:
        if (i + 1 > int(float(countOrder) // countOrdersFiles)) and (normalNameForSplit(order) != normalNameForSplit(orders[-1])):
            createExcel(orders, listErrorBarcods, mode)
            i = 0
            orders = []
        orders.append(order)
        i += 1
    createExcel(orders, listErrorBarcods, mode)


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


def get_orders(Token, days=30):
    """Получает заказы за последние 3 дня"""
    print("Идёт получение свежих заказов, ожидайте...")
    Url = 'https://suppliers-api.wildberries.ru/api/v2/orders?date_start={}%2B03%3A00&take=1000&skip={}'

    start_data = (datetime.today() - timedelta(days=int(days))).isoformat('T', 'seconds').replace(
        ':', '%3A').replace('+', '%2B').replace('.', '%2E')
    count_skip = 0
    tmp = []
    dataorders = []
    flag = True
    while len(tmp) > 0 or flag:
        CountTry = 0
        flag = False
        while True:
            CountTry += 1
            try:
                response = requests.get(Url.format(start_data, count_skip), headers={
                    'Authorization': '{}'.format(Token)})
                if response.status_code == 200:
                    break
                elif CountTry > 500:
                    print("Не удалось достучасться до ВБ")
                else:
                    continue
            except:
                continue
        count_skip = count_skip+1000
        tmp = response.json()['orders']
        dataorders.extend(tmp)
    all_data = pandas.DataFrame(dataorders)
    all_data.to_excel(joinpath(WBOrdersData,
                               WBOrdersDataFileName), index=False)
    return dataorders


def changeStatus(listOrderForChangeStatus, Token):
    """Изменяет статус заказа на заданный, в данном случае "1" - на сборке"""
    if Debug != 1:
        orderListForChange = []
        Url = 'https://suppliers-api.wildberries.ru/api/v2/orders'
        if Debug == 1:
            status = 0
        else:
            status = 1
        for orderForChange in listOrderForChangeStatus:
            if len(orderListForChange) < 1000:
                datajson = []
                orderId = orderForChange['Номер задания']
                datajson = {"orderId": orderId,
                            "status": status}
                orderListForChange.append(datajson)
            else:
                while True:
                    try:
                        response = requests.put(Url, headers={
                            'Authorization': '{}'.format(Token)}, json=orderListForChange)
                        if response.status_code != 200:
                            continue
                        elif response.status_code == 200:
                            break
                    except:
                        continue
                orderListForChange = []
                print(response)
        while True:
            try:
                response = requests.put(Url, headers={
                    'Authorization': '{}'.format(Token)}, json=orderListForChange)
                if response.status_code != 200:
                    continue
                elif response.status_code == 200:
                    break
            except:
                continue
        print(response)


if __name__ == '__main__':
    if startChek() == 0:
        Pool = multiprocessing.Pool(4)
        Token = getToken()
        while input("Введите 0 чтобы выйти. Enter продожить получение заказов: ") != '0':
            data = get_orders(Token)
            mode = choiseMode()
            if mode == 0:
                break
            nowFileName = []
            changeStatus(orderFilter(data, mode), Token)
            if read_xlsx(r'C:\Users\Public\Documents\WBGetOrder\WBOrdersData\ФБС {} {} {}.xlsx', title='No') != []:
                print('ОБНОВИ БАЗУ')
        print('Не выключайте программу, идёт формирование ценников!')

        for order in nowFileName:
            Pool.apply_async(printStiker, args=(order, ))
        Pool.close()
        Pool.join()
        input("Ценники готовы, нажмите Enter")
        for file in listdir(TMPDir):
            remove(joinpath(TMPDir, file))
