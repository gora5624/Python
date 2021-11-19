import requests
from os.path import join as joinpath
from os import listdir
import xlrd

main_path = r'C:\Users\Public\Documents\WBGetOrder'
Token_path = joinpath(main_path, r'Token.txt')
Debug = 1


def read_xlsx(file_path, title='Yes'):
    nameList = 'основной' if 'стекла' not in file_path else [
        '3D_стекла', 'глянец', 'матовые', 'камеры']
    rd = xlrd.open_workbook(file_path)
    if type(nameList) == str:
        try:
            sheet = rd.sheet_by_name(nameList)
        except:
            data = []
            return data
        if title == 'Yes':
            Name_row = sheet.row_values(0)
            start = 1
        elif title == 'No':
            Name_row = None
            start = 0
        data = []
        for rownum in range(start, sheet.nrows):
            row = sheet.row_values(rownum)
            if title == 'Yes':
                dct = {}
                for i, cel in enumerate(row):
                    tmp = {Name_row[i]: cel}
                    dct.update(tmp)
                data.append(dct)
            elif title == 'No':
                data.append(row)
        return data
    elif type(nameList) == list:
        data = []
        for name in nameList:
            try:
                sheet = rd.sheet_by_name(name)
            except:
                return data
            if title == 'Yes':
                try:
                    Name_row = sheet.row_values(0)
                except IndexError:
                    continue
                start = 1
            elif title == 'No':
                Name_row = None
                start = 0
            for rownum in range(start, sheet.nrows):
                row = sheet.row_values(rownum)
                if title == 'Yes':
                    dct = {}
                    for i, cel in enumerate(row):
                        tmp = {Name_row[i]: cel}
                        dct.update(tmp)
                    data.append(dct)
                elif title == 'No':
                    data.append(row)
        return data


# def changeStatus(orderForChandeStatus, Token):
#     orderId = orderForChandeStatus
#     Url = 'https://suppliers-api.wildberries.ru/api/v2/orders'
#     status = 3
#     datajson = [{"orderId": str(orderId),
#                  "status": status}]
#     while True:
#         try:
#             response = requests.put(Url, headers={
#                 'Authorization': '{}'.format(Token)}, json=datajson)
#             if response.status_code != 200:
#                 print('Ошибка Вб')
#                 continue
#             elif response.status_code == 200 and response.text:
#                 print("Заказ {} Успешно отменён.".format(orderForChandeStatus))
#             return 0
#         except:
#             continue


def changeStatus(orderForChandeStatus, Token):
    orderId = orderForChandeStatus
    Url = 'https://suppliers-api.wildberries.ru/api/v2/orders'
    status = 3
    datajson = [{"orderId": str(orderId),
                 "status": status}]
    while True:
        try:
            response = requests.put(Url, headers={
                'Authorization': '{}'.format(Token)}, json=datajson)
            if response.status_code != 200:
                print('Ошибка Вб')
                continue
            elif response.status_code == 200 and response.text:
                print("Заказ {} Успешно отменён.".format(orderForChandeStatus))
            return 0
        except:
            continue


def getStiker(OrderNum):
    with open(Token_path, 'r', encoding='UTF-8') as file:
        Token = file.read()
        file.close()
    UrlStiker = 'https://suppliers-api.wildberries.ru/api/v2/orders/stickers'
    trying = 0
    OrderNumJson = {"orderIds": OrderNum}
    while True:
        trying += 1
        try:
            response = requests.post(UrlStiker, headers={
                'Authorization': '{}'.format(Token)}, json=OrderNumJson)
            if response.status_code == 200:
                break
            elif trying > 500:
                print("Не удолось достучаться до сервера ВБ")
                return 1
            else:
                continue
        except:
            continue

    return response.json()['data']


def findDirOrder(stiker):
    mainPath = r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд'
    dirListForFind = [joinpath(mainPath, r'Новые'),
                      joinpath(mainPath, r'В работе'),
                      joinpath(mainPath, r'Отработано')]
    for dir_ in dirListForFind:
        if findFileOrder(dir_, stiker) == 0:
            return 0


def findLineOrder(fileOrder):
    tmp = []
    for line in fileOrder:
        try:
            tmp.append(int(line['Номер задания']))
        except:
            continue
    return tmp


def findFileOrder(dir_, stiker):
    for file in listdir(dir_):
        if '.xls' in file and "$" not in file:
            data = read_xlsx(joinpath(dir_, file))
            listOrderNum = findLineOrder(data)
            stikers = getStiker(listOrderNum)
            for line in stikers:
                if int(stiker) == line['sticker']['wbStickerId']:
                    if changeStatus(line['orderId'], Token) == 0:
                        return 0


def getToken():
    """Получаем токен для авторизации"""
    with open(Token_path, 'r', encoding='UTF-8') as file:
        Token = file.read()
        file.close()
    return Token


if __name__ == '__main__':
    while True:
        stiker = str(input("Введите номер стикера или номер заказа: "))
        if len(stiker) == 10:
            Token = getToken()
            findDirOrder(stiker)
        elif len(stiker) == 9:
            Token = getToken()
            orderForChandeStatus = stiker
            changeStatus(orderForChandeStatus, Token)
        else:
            print('Вы ввели не верные данные.')
            continue
