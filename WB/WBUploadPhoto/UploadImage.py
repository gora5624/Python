from os.path import join as joinpath, abspath
import sys
sys.path.insert(1, joinpath(sys.path[0], '../..'))
import requests
from my_mod.my_lib import read_xlsx
import json
import multiprocessing
import asyncio
import datetime
import pandas

main_path = r'C:\Users\Public\Documents\WBUploadImage'
nameListStuff = r'StuffList.xlsx'
pathToListStuff = joinpath(__file__, '..', 'Photo.xlsx')
#Token_path = joinpath(main_path, r'Token.txt')
Token_path = joinpath(main_path, r'TokenAbr.txt')
mainUrl = 'http://cj15871-wordpress-1.tw1.ru/upload/'
DoneList = []
TMP_List = []

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
        a = response.json()['result']['cards'][0]
    except IndexError:
        return 0
    return response.json()['result']['cards'][0]['imtId']



def createDictWithBarcode(pathToListStuff):
    data = read_xlsx(pathToListStuff)
    dataNew = {}
    print('Получаю список ссылок...')
    for line in data:
        tmpDict = {line['Баркод']: {"Баркод": line['Баркод'],
                                    "Принт": line['Основная характеристика'],
                                    "Цвет": line['Код цвета'],
                                    "Модель": line['Модель'],
                                    "Ссылка": line['Ссылка']}}
        dataNew.update(tmpDict)
    print('Готово.')
    return dataNew


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


def changeCard(cardBody, dataFromLIstStuff):
    with open(Token_path, 'r', encoding='UTF-8') as file:
        Token = file.read()
        file.close()
    changeCardUrl = 'https://suppliers-api.wildberries.ru/card/update'
    if cardBody['countryProduction'] == '':
        cardBody['countryProduction'] = 'Китай'
    cardBody['addin'].append({'type':'Комплектация',
    'params':[{'value':'Чехол'}]})
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(TestMain(cardBody,dataFromLIstStuff, changeCardUrl, Token))
    for i, nomenclatures in enumerate(cardBody['nomenclatures']):
        for variantion in nomenclatures['variations']:
            for barcodNom in variantion['barcodes']:
                if barcodNom not in DoneList:
                    try:
                        data = dataFromLIstStuff[barcodNom]
                        DoneList.append(barcodNom)
                        break
                    except KeyError:
                        print("По баркоду {} нет фото в списке.".format(barcodNom))
                        continue
        url_1 = data['Ссылка']
        url_2 = mainUrl + 'Вторые картинки/' + data['Модель'] + '/' + data['Цвет'] + '/' + '2.jpg'
        url_3 = mainUrl + 'Вторые картинки/' + data['Модель'] + '/' + data['Цвет'] + '/' + '3.jpg'
        url_4 =mainUrl + 'Вторые картинки/' + data['Модель'] + '/' + data['Цвет'] + '/' + '4.jpg'
        a = {
            "type": "Фото",
            "params": [
                {
                "value": url_1.replace(' ', '%20')
                },
                {
                "value": url_2.replace(' ', '%20')
                },
                {
                "value": url_3.replace(' ', '%20')
                },
                {
                "value": url_4.replace(' ', '%20')
                }
            ]
            }
        flag = True
        flag2 = False
        for j, addin in enumerate(cardBody['nomenclatures'][i]['addin']):
            if addin['type'] == 'Фото':
                if len(addin['params']) != 4:
                    cardBody['nomenclatures'][i]['addin'][j] = a
                    TMP_List.append(barcodNom + ' ;не все фото')
                    print(barcodNom + ' ;Не все фото')
                    flag2 = True
                else:
                    TMP_List.append(barcodNom + ' ;было фото')
                    print(barcodNom + ' ;было фото')
                flag = False
                break
        if flag:
            cardBody['nomenclatures'][i]['addin'].append(a)
            TMP_List.append(barcodNom +' ;не было фото')
            print(barcodNom +' ;не было фото')
            flag2 = True
        cardBodyNew = {
            "id": '1',
            "jsonrpc": "2.0",
            "params": {
                "card": cardBody
            }
        }
        if flag2:
            while True:
                response = requests.post(changeCardUrl, headers={
                    'Authorization': '{}'.format(Token)}, json=cardBodyNew)
                if response.status_code == 200:
                    print(response.text)
                    break



# async def TestMain(cardBody,dataFromLIstStuff, changeCardUrl, Token):
#     listTask = []
#     for i, nomenclatures in enumerate(cardBody['nomenclatures']):
#         listTask.append(test(i, nomenclatures,dataFromLIstStuff, cardBody, changeCardUrl, Token))
#     await asyncio.wait(listTask)


# async def test(i, nomenclatures,dataFromLIstStuff, cardBody, changeCardUrl, Token):
#     for variantion in nomenclatures['variations']:
#             for barcodNom in variantion['barcodes']:
#                 if barcodNom not in DoneList:
#                     try:
#                         data = dataFromLIstStuff[barcodNom]
#                         DoneList.append(barcodNom)
#                         break
#                     except KeyError:
#                         print("По баркоду {} нет фото в списке.".format(barcodNom))
#                         continue
#     url_1 = data['Ссылка']
#     url_2 = mainUrl + 'Вторые картинки/' + data['Модель'] + '/' + data['Цвет'] + '/' + '2.jpg'
#     url_3 = mainUrl + 'Вторые картинки/' + data['Модель'] + '/' + data['Цвет'] + '/' + '3.jpg'
#     url_4 =mainUrl + 'Вторые картинки/' + data['Модель'] + '/' + data['Цвет'] + '/' + '4.jpg'
#     a = {
#         "type": "Фото",
#         "params": [
#             {
#             "value": url_1.replace(' ', '%20')
#             },
#             {
#             "value": url_2.replace(' ', '%20')
#             },
#             {
#             "value": url_3.replace(' ', '%20')
#             },
#             {
#             "value": url_4.replace(' ', '%20')
#             }
#         ]
#         }
#     flag = True
#     flag2 = False
#     for j, addin in enumerate(cardBody['nomenclatures'][i]['addin']):
#         if addin['type'] == 'Фото':
#             if len(addin['params']) != 4:
#                 cardBody['nomenclatures'][i]['addin'][j] = a
#                 TMP_List.append(barcodNom + ' ;не все фото')
#                 print(barcodNom + ' ;Не все фото')
#                 flag2 = True
#             else:
#                 TMP_List.append(barcodNom + ' ;было фото')
#                 print(barcodNom + ' ;было фото')
#             flag = False
#             break
#     if flag:
#         cardBody['nomenclatures'][i]['addin'].append(a)
#         TMP_List.append(barcodNom +' ;не было фото')
#         print(barcodNom +' ;не было фото')
#         flag2 = True
#     cardBodyNew = {
#         "id": '1',
#         "jsonrpc": "2.0",
#         "params": {
#             "card": cardBody
#         }
#     }
#     if flag2:
#         while True:
#             response = requests.post(changeCardUrl, headers={
#                 'Authorization': '{}'.format(Token)}, json=cardBodyNew)
#             if response.status_code == 200:
#                 print(response.text)
#                 break



def changeBody(barcod, dataFromLIstStuff):
    barcod = barcod if type(
        barcod) == str else str(barcod)[0:-2]
    idStuff = getIdWithBarcod(barcod)
    if idStuff == 0:
        return 0
    cardBody = getCardBody(idStuff)
    changeCard(cardBody, dataFromLIstStuff)


def startChangeCard(poolBarcodes, dataFromListStuff):
    for barcod in poolBarcodes:
        if barcod not in DoneList:
            changeBody(barcod, dataFromListStuff)


def splitList(listForSplit, chunksCount):
    splitList =[]
    tmp = []
    countInLine = len(listForSplit)// chunksCount
    i = 0
    for stuff in listForSplit:
        i+=1
        tmp.append(stuff)
        if i>=countInLine:
            i = 0
            splitList.append(tmp)
            tmp=[]
    splitList.append(tmp)
    return splitList


if __name__ == '__main__':
    while True:
        manager = multiprocessing.Manager()
        doneList = manager.list()
        dataFromListStuff = createDictWithBarcode(pathToListStuff)
        countThreadMax = multiprocessing.cpu_count() - 2 if multiprocessing.cpu_count() > 2 else 0
        pool = multiprocessing.Pool(countThreadMax)
        for poolBarcodes in splitList(dataFromListStuff, countThreadMax):
            pool.apply_async(startChangeCard, args=(poolBarcodes,dataFromListStuff,))
        pool.close()
        pool.join()



