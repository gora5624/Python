
from os.path import join as joinpath
import requests
from my_lib import read_xlsx
import pandas
import json
import multiprocessing


main_path = r'C:\Users\Public\Documents\WBChangeStuff'
nameListStuff = r'StuffList.xlsx'
pathToListStuff = joinpath(main_path, nameListStuff)
Token_path = joinpath(main_path, r'Token.txt')
outListName = 'barcodes and art.xlsx'
outListName2 = 'barcodes and art2.xlsx'
outListPath = joinpath(main_path, outListName)
outListPath2 = joinpath(main_path, outListName2)


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
    print(barcod)
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
    # print(response.text)
    return json.loads(response.text)['result']['card']


def changeCard(cardBody, name, TmpLIst):
    with open(Token_path, 'r', encoding='UTF-8') as file:
        Token = file.read()
        file.close()
    changeCardUrl = 'https://suppliers-api.wildberries.ru/card/update'
    cardBody['countryProduction'] = 'Китай'
    for addin in cardBody['addin']:
        if addin['type'] == 'Комплектация':
            addin['params'] = [
                {'value': name}]
        if addin['type'] == 'Бренд':
            addin['params'] = [
                {'value': 'Mobi711'}]
    cardBodyNew = {
        "id": '1',
        "jsonrpc": "2.0",
        "params": {
            "card": cardBody
        }
    }
    # while True:
    #     try:
    #         response = requests.post(changeCardUrl, headers={
    #             'Authorization': '{}'.format(Token)}, json=cardBodyNew)
    #         if 'error' not in response.text and 'timeout' not in response.text:
    #             break
    #         if response.status_code == 200:
    #             break
    #     except:
    #         print('error changeCard')
    #         continue
    for nomenclature in cardBody['nomenclatures']:
        try:
            TmpLIst.append({'Артикул WB': nomenclature['nmId'],
                            'Баркод': nomenclature['variations'][0]['barcodes'][0]})
        except:
            continue
    #print((response.text, name, ))


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
            if response.status_code == 200 and 'err' not in response.text and 'timeout' not in response.text:
                break
        except:
            print('error changeCard')
            continue
    print((response.text))


def changeBody(stuffLine, TmpLIst, TmpLIst2):
    barcod = stuffLine['Баркод'] if type(
        stuffLine['Баркод']) == str else str(stuffLine['Баркод'])[0:-2]
    idStuff = getIdWithBarcod(barcod)
    if idStuff == 0:
        return 0
    cardBody = getCardBody(idStuff)
    #name = stuffLine['Название']
    if 'чехол' in str(stuffLine['Название']).lower():
        name = 'Чехол'
    elif 'стекло' in str(stuffLine['Название']).lower():
        name = 'Защитное стекло'
    elif 'планка' in str(stuffLine['Название']).lower():
        name = 'Пластина для держалетя прямоугольная и круглая'
    else:
        name = 'Чехол'
    changeCard(cardBody, name, TmpLIst)


def cangeCardFromListStuff(pathToListStuff, TmpLIst, TmpLIst2):
    dataFromLIstStuff = read_xlsx(pathToListStuff)
    pool = multiprocessing.Pool()
    for stuffLine in dataFromLIstStuff:
        pool.apply_async(changeBody, args=(stuffLine, TmpLIst, TmpLIst2,))
    pool.close()
    pool.join()

# def cangeCardFromListStuff(pathToListStuff, TmpLIst, TmpLIst2):
#     dataFromLIstStuff = read_xlsx(pathToListStuff)
#     changeBody
#     pool = multiprocessing.Pool()
#     for stuffLine in dataFromLIstStuff:
#         changeBody(stuffLine, TmpLIst, TmpLIst2)
#         pool.apply_async(changeBody, args=(stuffLine, TmpLIst, TmpLIst2,))
#     pool.close()
#     pool.join()


if __name__ == '__main__':
    with multiprocessing.Manager() as manager:
        TmpLIst = manager.list()
        TmpLIst2 = manager.list()
        cangeCardFromListStuff(pathToListStuff, TmpLIst, TmpLIst2)
        TmpLIst = list(TmpLIst)
        TmpLIst2 = list(TmpLIst2)
        TmpLIstpd = pandas.DataFrame(TmpLIst)
        TmpLIstpd2 = pandas.DataFrame(TmpLIst2)
        TmpLIstpd.to_excel(outListPath, index=False)
        TmpLIstpd2.to_excel(outListPath2, index=False)

# imtID = getIdWithBarcod('2011753370003')
# cardBody = getCardBody(imtID)
# name = 'Защитное стекло для Samsung Galaxy M52 (M 52) (5G)|Cтекло Самсунг М52 (М 52) (5G) (не чехол)'
# changeOneCard(cardBody, name)
