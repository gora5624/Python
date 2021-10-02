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


pathToListStuff = r'D:\barcods.xlsx'
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
    try:
        return response.json()['result']['cards'][0]['imtId']
    except:
        tmp = {'barcod': barcod}
        TmpLIst.append(tmp)


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


def changeCard(cardBody, name):
    data = {}
    with open(Token_path, 'r', encoding='UTF-8') as file:
        Token = file.read()
        file.close()
    changeCardUrl = 'https://suppliers-api.wildberries.ru/card/update'
    cardBody['countryProduction'] = 'Китай'
    for addin in cardBody['addin']:
        if addin['type'] == 'Наименование':
            addin['params'] = [
                {'value': name}]
    cardBodyNew = {
        "id": '1',
        "jsonrpc": "2.0",
        "params": {
            "card": cardBody
        }
    }
    while True:
        try:
            response = requests.post(changeCardUrl, headers={
                'Authorization': '{}'.format(Token)}, json=cardBodyNew)
            if response.status_code == 200:
                break
        except:
            print('error changeCard')
            continue
    TmpLIst.append({'Артикул': cardBody['nomenclatures'][0]['nmId'],
                    'Баркод': cardBody['nomenclatures'][0]['variations'][0]['barcodes'][0]})
    print(response.text)


def cangeCardFromListStuff(pathToListStuff):
    dataFromLIstStuff = read_xlsx(pathToListStuff)
    for stuffLine in dataFromLIstStuff:
        barcod = stuffLine['Баркод'] if type(
            stuffLine['Баркод']) == str else str(stuffLine['Баркод'])[0:-2]
        idStuff = getIdWithBarcod(barcod)
        cardBody = getCardBody(idStuff)
        name = stuffLine['Название']
        changeCard(cardBody, name)


cangeCardFromListStuff(pathToListStuff)
TmpLIstpd = pandas.DataFrame(TmpLIst)
TmpLIstpd.to_excel(r'D:\barcodes and art1.xlsx', index=False)

'''imtID = getIdWithBarcod('2009040627008')
cardBody = getCardBody(imtID)
changeCard(cardBody)'''
