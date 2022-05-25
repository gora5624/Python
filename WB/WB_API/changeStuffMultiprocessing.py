from audioop import mul
from os.path import join as joinpath
import sys
sys.path.insert(1, joinpath(sys.path[0], '../..'))
import requests
from my_mod.my_lib import read_xlsx
import json
import multiprocessing


# 1 - изменяем, 0 - нет
isChange = 1

main_path = r'C:\Users\Public\Documents\WBChangeStuff'
nameListStuff = r'StuffList.xlsx'
pathToListStuff = joinpath(main_path, nameListStuff)
pathToListMultiStuffKar = r'C:\Users\Public\Documents\WBChangeStuff\MultiBrandKar.xlsx'
pathToListMultiStuffAbr = r'C:\Users\Public\Documents\WBChangeStuff\MultiBrandAbr.xlsx'
pathToListMobiStuffKar = r'C:\Users\Public\Documents\WBChangeStuff\MultiBrandKar.xlsx'
pathToListMobiStuffAbr = r'C:\Users\Public\Documents\WBChangeStuff\MultiBrandAbr.xlsx'
tokenPath_kar = joinpath(main_path, r'Token.txt')
tokenPath_Arb = joinpath(main_path, r'TokenAbr.txt')
tokenList = [tokenPath_kar, tokenPath_Arb]


def getIdWithBarcod(barcod,tokenPath):
    with open(tokenPath, 'r', encoding='UTF-8') as file:
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
        a = response.json()['result']['cards'][0]
    except IndexError:
        return 0
    print(barcod)
    return response.json()['result']['cards'][0]['imtId']


def getCardBody(imtID,tokenPath):

    with open(tokenPath, 'r', encoding='UTF-8') as file:
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
    try:
        return json.loads(response.text)['result']['card']
    except:
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
        return json.loads(response.text)['result']['card']


def changeCard(cardBody, stuffLine,tokenPath):
    with open(tokenPath, 'r', encoding='UTF-8') as file:
        Token = file.read()
        file.close()
    changeCardUrl = 'https://suppliers-api.wildberries.ru/card/update'
    cardBody['countryProduction'] = 'Китай'
    for ad in list(stuffLine.keys())[1:]:
        flag = True
        for addin in cardBody['addin']:
            if addin['type'] == ad:
                par = stuffLine[ad].split(';')
                pars = []
                for a in par:
                    if a != '':
                        pars.append({'value': a.strip()})
                addin['params'] = pars
                flag = False
                print(pars)
        if flag:    
            par = stuffLine[ad].split(';')
            pars = []
            for a in par:
                if a != '':
                    pars.append({'value': a.strip()})
            ads = {'type': ad,
                   'params': pars}
            cardBody['addin'].append(ads)
    cardBodyNew = {
        "id": '1',
        "jsonrpc": "2.0",
        "params": {
            "card": cardBody
        }
    }
    if isChange == 1:
        while True:
            try:
                response = requests.post(changeCardUrl, headers={
                    'Authorization': '{}'.format(Token)}, json=cardBodyNew)
                if 'connect error' in response.text:
                    continue
                if ('error' not in response.text) and ('timeout' not in response.text):
                    break
                if response.status_code == 200:
                    print(response.text)
                    if 'Запрещено использовать символы в начале значения' in response.text:
                        pass
                    break
            except:
                print('error changeCard')
                continue



def changeBody(stuffLine,tokenPath):
    barcod = stuffLine['Баркод'] if type(
        stuffLine['Баркод']) == str else str(stuffLine['Баркод'])[0:-2]
    idStuff = getIdWithBarcod(barcod,tokenPath)
    if idStuff == 0:
        return 0
    cardBody = getCardBody(idStuff,tokenPath)
    changeCard(cardBody, stuffLine,tokenPath)


def cangeCardFromListStuff(pathToListStuff,tokenPath):
    dataFromLIstStuff = read_xlsx(pathToListStuff)
    pool = multiprocessing.Pool(3)
    for stuffLine in dataFromLIstStuff:
        pool.apply_async(changeBody, args=(stuffLine,tokenPath,))
    pool.close()
    pool.join()


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=cangeCardFromListStuff, args=(pathToListMultiStuffKar,tokenPath_kar,))
    p2 = multiprocessing.Process(target=cangeCardFromListStuff, args=(pathToListMultiStuffAbr,tokenPath_Arb,))
    p2.start()
    p1.start()
    p1.join()
    p2.join()
