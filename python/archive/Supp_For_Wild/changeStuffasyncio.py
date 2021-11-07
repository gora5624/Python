from json import encoder
from os.path import join as joinpath
from datetime import datetime, timedelta
import requests
from my_lib import file_exists, read_xlsx
from os import makedirs
import pandas
from my_lib import read_xlsx
import json
import multiprocessing


pathToListStuff = r'D:\AllCasePrint.xlsx'
main_path = r'C:\Users\Public\Documents\WBGetStuff'
Token_path = joinpath(main_path, r'Token.txt')


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
    a = response.json()['result']['cards'][0]
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
    a = json.loads(response.text)
    return json.loads(response.text)['result']['card']


def changeCard(cardBody, name, TmpLIst):
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
            # if 'error' not in response.text and 'timeout' not in response.text:
            #     break
            if response.status_code == 200:
                break
        except:
            print('error changeCard')
            continue
    for nomenclature in cardBody['nomenclatures']:
        TmpLIst.append({'Артикул WB': nomenclature['nmId'],
                        'Баркод': nomenclature['variations'][0]['barcodes'][0]})
    print((response.text, name))


def changeOneCard(cardBody, name):
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
            if 'error' not in response.text and 'timeout' not in response.text:
                break
            if response.status_code == 200:
                break
        except:
            print('error changeCard')
            continue
    print((response.text))


def changeBody(stuffLine, TmpLIst):
    barcod = stuffLine['Баркод'] if type(
        stuffLine['Баркод']) == str else str(stuffLine['Баркод'])[0:-2]
    idStuff = getIdWithBarcod(barcod)
    cardBody = getCardBody(idStuff)
    name = stuffLine['Название']
    changeCard(cardBody, name, TmpLIst)


def cangeCardFromListStuff(pathToListStuff, TmpLIst):
    dataFromLIstStuff = read_xlsx(pathToListStuff)
    pool = multiprocessing.Pool()
    for stuffLine in dataFromLIstStuff:
        pool.apply_async(changeBody, args=(stuffLine, TmpLIst,))
    pool.close()
    pool.join()


if __name__ == '__main__':
    with multiprocessing.Manager() as manager:
        TmpLIst = manager.list()
        cangeCardFromListStuff(pathToListStuff, TmpLIst)
        TmpLIst = list(TmpLIst)
        TmpLIstpd = pandas.DataFrame(TmpLIst)
        TmpLIstpd.to_excel(r'D:\barcodes and art1.xlsx', index=False)

# imtID = getIdWithBarcod('2001256753199')
# cardBody = getCardBody(imtID)
# name = 'Чехол для Samsung Galaxy A03s (A03 s)|чехол Самсунг Галакси А03с (А03 с) бампер силикон (не стекло)'
# changeOneCard(cardBody, name)
