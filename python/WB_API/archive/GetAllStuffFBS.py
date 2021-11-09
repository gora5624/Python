from os.path import join as joinpath
import requests
from my_lib import file_exists, read_xlsx
from os import makedirs
import pandas


main_path = r'C:\Users\Public\Documents\WBGetStuff'
Token_path = joinpath(main_path, r'Token.txt')
WBOrdersDataFileName = r'Data_stuff.xlsx'
WBOrdersData = joinpath(
    main_path, r'WBStuffData')


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


def get_stuff():
    with open(Token_path, 'r', encoding='UTF-8') as file:
        Token = file.read()
        file.close()
    print("Идёт получение товаров, ожидайте...")
    Url = 'https://suppliers-api.wildberries.ru/api/v2/stocks?skip={}&take=1000&sort=article&order=asc'
    count_skip = 0
    tmp = []
    data = []
    flag = True
    while tmp != None or flag:
        flag = False
        response = requests.get(Url.format(count_skip), headers={
            'Authorization': '{}'.format(Token)})
        if response.status_code != 200:
            print('Не удалось получить остатки, ошибка на стороне ВБ.')
            return 1
        count_skip = count_skip+1000
        data.extend(tmp)
        tmp = response.json()['stocks']
    all_data = pandas.DataFrame(data)
    all_data.to_excel(joinpath(WBOrdersData,
                               WBOrdersDataFileName), index=False)
    return data


startChek()
get_stuff()
