from json import encoder
from os.path import join as joinpath
from datetime import datetime, timedelta
import re
import requests
from my_lib import file_exists, read_xlsx
from os import makedirs
import pandas
from my_lib import read_xlsx
import json


pathToListStuff = r'C:\Users\user\Downloads\Остатки ФБС\РЕалми с21у.xlsx'
main_path = r'C:\Users\Public\Documents\WBGetStuff'
Token_path = joinpath(main_path, r'Token.txt')
TmpLIst = []


def getIdWithBarcod(barcod):
    with open(Token_path, 'r', encoding='UTF-8') as file:
        Token = file.read()
        file.close()
    Url = 'https://suppliers-api.wildberries.ru/card/list'

    datajson = {
        "id": "1",
        "jsonrpc": "2.0",
        "params": {
            "filter": {

                "find": [
                  {
                      "column": "nomenclatures.variations.barcode",
                      "search": barcod
                  }

                ],
                "order": {
                    "column": "createdAt",
                    "order": "asc"
                }
            },

            "query": {
                "limit": 5,
                "offset": 0
            },
            "withError": False
        }
    }
    while True:
        try:
            response = requests.post(Url, headers={
                'Authorization': '{}'.format(Token)}, json=datajson)
            if response.status_code == 200:
                break
            else:
                print(response.text)
                continue
        except:
            continue

    return response.json()['result']['cards'][0]['imtId']


def getCardBody(imtID):

    with open(Token_path, 'r', encoding='UTF-8') as file:
        Token = file.read()
        file.close()
    getCardBodyUrl = 'https://suppliers-api.wildberries.ru/card/cardByImtID'

    getCardBodyDataJson = {
        "jsonrpc": "2.0",
        "params": {
            "imtID": imtID
        }
    }

    while True:
        try:
            response = requests.post(getCardBodyUrl, headers={
                'Authorization': '{}'.format(Token)}, json=getCardBodyDataJson)
            if response.status_code == 200:
                break
            else:
                print(response.text)
                continue
        except:
            continue
    response
    return json.loads(response.text)['result']['card']


def changeCard(cardBody):
    data = {}
    with open(Token_path, 'r', encoding='UTF-8') as file:
        Token = file.read()
        file.close()
    changeCardUrl = 'https://suppliers-api.wildberries.ru/card/update'

    cardBody['addin'][2]['params'][0][
        'value'] = 'Чехол для Realme C21y (C21 y)/Реалми С21у (Реалме С 21 у).(не стекло) силикон с картинкой (принт)'
    cardBodyNew = {
        "id": '1',
        "jsonrpc": "2.0",
        "params": {
            "card": cardBody
        }
    }
    data = {'Баркод': cardBody['nomenclatures']
            [0]['variations'][0]['barcodes'][0],
            'Артикул WB': cardBody['nomenclatures'][0]['nmId']}

    TmpLIst.append(data)
    while True:
        try:
            response = requests.post(changeCardUrl, headers={
                'Authorization': '{}'.format(Token)}, json=cardBodyNew)
            if response.status_code == 200:
                break
        except:
            print('error changeCard')
            continue
    response


def cangeCardFromListStuff(pathToListStuff):
    dataFromLIstStuff = read_xlsx(pathToListStuff, title='No')
    for stuffLine in dataFromLIstStuff:
        barcod = stuffLine[0] if type(
            stuffLine[0]) == str else str(stuffLine['Баркод'])[0:-2]
        idStuff = getIdWithBarcod(barcod)
        cardBody = getCardBody(idStuff)
        changeCard(cardBody)


cangeCardFromListStuff(pathToListStuff)

'''imtID = getIdWithBarcod('2007346811008')
cardBody = getCardBody(imtID)
changeCard(cardBody)'''
TmpLIstpd = pandas.DataFrame(TmpLIst)
TmpLIstpd.to_excel(r'D:\c21y.xlsx', index=False)
