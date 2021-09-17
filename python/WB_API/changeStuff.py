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


pathToListStuff = r'D:\barcodes.xlsx'
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

    for i, addin in enumerate(cardBody['addin']):
        if addin['type'] == 'Бренд':
            addin['params'] = [{'value': 'Чехол OnePlus Nord N-100'}]
        if addin['type'] == 'Наименование':
            addin['params'] = [
                {'value': 'Чехол OnePlus Nord N-100 с рисунком (принт)'}]
        if addin['type'] == 'Тип чехлов':
            addin['params'] = [
                {'value': ''}]
        if addin['type'] == 'Материал изделия':
            addin['params'] = [
                {'value': ''}]

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
    print(response.text)


def cangeCardFromListStuff(pathToListStuff):
    dataFromLIstStuff = read_xlsx(pathToListStuff)
    for stuffLine in dataFromLIstStuff:
        barcod = stuffLine['Баркод'] if type(
            stuffLine['Баркод']) == str else str(stuffLine['Баркод'])[0:-2]
        idStuff = getIdWithBarcod(barcod)
        cardBody = getCardBody(idStuff)
        changeCard(cardBody)


cangeCardFromListStuff(pathToListStuff)

'''imtID = getIdWithBarcod('2001988340698')
cardBody = getCardBody(imtID)
changeCard(cardBody)
TmpLIstpd = pandas.DataFrame(TmpLIst)
TmpLIstpd.to_excel(r'D:\c21y.xlsx', index=False)'''
