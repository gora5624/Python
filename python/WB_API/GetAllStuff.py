from os.path import join as joinpath
import requests
from my_lib import file_exists, read_xlsx
from os import makedirs
import pandas


main_path = r'C:\Users\Public\Documents\WBGetStuff'
Token_path = joinpath(main_path, r'Token.txt')
WBOrdersDataFileName = r'Data_stuff_1.xlsx'
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
    Url = 'https://suppliers-api.wildberries.ru/card/list'
    tmp = []
    data = []
    for line in read_xlsx(r'\\192.168.0.33\shared\Отдел производство\Wildberries\Новая номенклатура.xlsx'):
        barcode = line['barcode']
        datajson = {
            "id": "1",
            "jsonrpc": "2.0",
            "params": {
                "filter": {

                    "find": [
                        {
                            "column": "nomenclatures.variations.barcode",
                            "search": barcode
                        }
                    ],
                    "order": {
                        "column": "createdAt",
                        "order": "asc"
                    }
                },

                "query": {
                    "limit": 10,
                    "offset": 0
                },
                "withError": False
            }
        }
        response = requests.post(Url, headers={
            'Authorization': '{}'.format(Token)}, json=datajson)
        tmp = response.json()['result']['cards']
        data.extend(tmp)
    all_data = pandas.DataFrame(data)
    all_data.to_excel(joinpath(WBOrdersData,
                               WBOrdersDataFileName), index=False)
    return data


startChek()
get_stuff()
