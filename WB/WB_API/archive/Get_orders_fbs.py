from os.path import join as joinpath
from datetime import datetime, timedelta
import pandas
import requests
import json
from my_lib import file_exists
from os import makedirs

main_path = r'C:\Users\Public\Documents\WBGetOrder'
Token_path = joinpath(main_path, r'Token.txt')
WBOrdersDataFileName = r'Data_orders.xlsx'
WBOrdersJsonDataFileName = r'Order.json'
WBOrdersData = joinpath(
    main_path, r'WBOrdersData')
TMPDir = joinpath(
    main_path, r'TMPDir')


def startChek():
    dirList = [main_path, WBOrdersData, TMPDir]
    for dir_ in dirList:
        if not file_exists(dir_):
            makedirs(dir_)
    if not file_exists(Token_path):
        print('Токен авторизации по адресу {} не обнаружен, получение заказов невозможно.'.format(
            Token_path))
        with open(Token_path, 'w', encoding='UTF-8') as file:
            file.close()


def get_orders(days):
    with open(Token_path, 'r', encoding='UTF-8') as file:
        Token = file.read()
        file.close()
    print("Идёт получение свежих заказов, ожидайте...")
    Url = 'https://suppliers-api.wildberries.ru/api/v2/orders?date_start={}%2B03%3A00&take=1000&skip={}'

    start_data = (datetime.today() - timedelta(days=int(days))).isoformat('T', 'seconds').replace(
        ':', '%3A').replace('+', '%2B').replace('.', '%2E')
    count_skip = 0
    data = '123'
    all_data = pandas.DataFrame()
    while len(data) > 0:
        response = requests.get(Url.format(start_data, count_skip), headers={
            'Authorization': '{}'.format(Token)})
        if response.status_code != 200:
            print('Не удалось получить заказы, ошибка на стороне ВБ.')
            return 1
        count_skip = count_skip+1000
        data = response.json()['orders']
        for line in data:
            line.update(wbStickerEncoded=line['sticker']['wbStickerEncoded'])
            line.update(
                wbStickerSvgBase64=line['sticker']['wbStickerSvgBase64'])
        with open(joinpath(WBOrdersData, WBOrdersJsonDataFileName), 'w') as file:
            json.dump(data, file)
        file.close()
        tmp = pandas.read_json(
            joinpath(WBOrdersData, WBOrdersJsonDataFileName))
        all_data = all_data.append(tmp)
    all_data.to_excel(joinpath(WBOrdersData,
                               WBOrdersDataFileName), index=False)
    return 0


def getOrdersOrNot():

    if str(input('Получить новые заказы? 1 - Да, 2 - Нет: ')) == str(1):
        days = input(
            "Ведите количество дней, за которое нужно получить заказы или нажмите Enter: ")
        if days == '':
            print("Вы не ввели кличество дней, получаю за последние 10 дней.")
            days = 10
        resp = get_orders(days)
    else:
        resp = 0
    return resp


startChek()
getOrdersOrNot()
a = input("Заказы получены, нажмите любую клавишу")
