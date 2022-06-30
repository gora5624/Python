from os.path import join as joinPath
import aiohttp
import asyncio
import requests
import pandas
from aiohttp import ClientPayloadError, ServerDisconnectedError

main_path = r'C:\Users\Public\Documents\WBUploadImage'
TokenKar = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
TokenArb = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
TokenSam = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
pathToDone = (r'F:\\')
DoneList = []
TMP_List = []


async def main(supplier, filter=None):
    if supplier =='Караханян':
        Token = TokenKar
    elif supplier =='Абраамян':
        Token = TokenArb
    elif supplier =='Самвел':
        Token = TokenSam
    Url = 'https://suppliers-api.wildberries.ru/card/list'
    offset = 0
    datajson = {
        "id": "1",
        "jsonrpc": "2.0",
        "params": {
            "filter": {
                "order": {
                    "column": "createdAt",
                    "order": "asc"
                }
            },

            "query": {
                "limit": 1,
                "offset": offset,
                "total":1000
            },
            "withError": False
        }
    }
    while True:
        totalCardsResponse = requests.post(Url, headers={
                        'Authorization': '{}'.format(Token)}, json=datajson)
        if totalCardsResponse.status_code ==200:
            break
        else:
            print(str(totalCardsResponse.status_code))
            continue
    totalCards = totalCardsResponse.json()['result']['cursor']['total']
    tasks = []
    cardslist = []
    barcodeList = []
    async with aiohttp.ClientSession() as session:
        if filter == None:
            for offset in range(0,totalCards,10):
                tasks.append(asyncio.create_task(getCard(session, offset, cardslist, Url, Token, filter)))
            await asyncio.wait(tasks)
        else:
            for i in range(0,len(filter),10):
                tasks.append(asyncio.create_task(getCard(session, offset, cardslist, Url, Token, filter[i: i+10])))
            await asyncio.wait(tasks)
    return cardslist


async def getCard(session, offset, cardslist, Url, Token, filter=None):
    if filter == None:
        datajson = {
            "id": "1",
            "jsonrpc": "2.0",
            "params": {
                "filter": {
                    "order": {
                        "column": "createdAt",
                        "order": "asc"
                    }
                },

                "query": {
                    "limit": 10,
                    "offset": offset,
                    "total":1000
                },
                "withError": False
            }
        }
    else: 
        datajson = {
            "id": "1",
            "jsonrpc": "2.0",
            "params": {
                "filter": {
                    "find": [
                  {
                    "column": "supplierVendorCode",
                    "search": filter
                  }
                ],
                    "order": {
                        "column": "createdAt",
                        "order": "asc"
                    }
                },

                "query": {
                    "limit": 10,
                    "offset": offset,
                    "total":1000
                },
                "withError": False
            }
        }
    while True:
        try:
            async with session.post(Url, headers={
                            'Authorization': '{}'.format(Token)}, json=datajson) as response: 
                        if response.status != 200:
                            print(response.status)
                            print(await response.text())
                            await asyncio.sleep(1)
                            continue
                        else:
                            try:
                                jsonCard = await response.json()
                            except ClientPayloadError:
                                await asyncio.sleep(1)
                                print('error')
                                continue
                            if 'error' not in jsonCard.keys():
                                datajson['params']['query']['offset'] = offset
                                cardslist.extend(jsonCard['result']['cards'])
                                break
        except ServerDisconnectedError:
            print('error')
            await asyncio.sleep(1)
            continue



def getValue(paramsList):
    values = []
    if len(paramsList) == 1:
        return paramsList[0]['value']
    else:
        for value in paramsList:
            values.append(value)
        return ';'.join(values)



def createListNomenclatures(cardslist, supplier):
    listCard = []
    barcodeList = []
    for card in cardslist:
        for nomenclatures in card['nomenclatures']:
            for variant in nomenclatures['variations']:
                if len(variant['barcodes'])!=0:
                    for barcod in variant['barcodes']:
                        barcodeList.append(barcod)
                        dataDefault = {'Бренд': getValue(card['addin'][0]['params']),
                                    'Предмет':card['object'],
                                    'Код размера (chrt_id)': variant['chrtId'],
                                    'Артикул поставщика': card['supplierVendorCode'] + nomenclatures['vendorCode'],
                                    'Артикул WB':nomenclatures['nmId'],
                                    'Артикул ИМТ':card['supplierVendorCode'],
                                    'Артикул Цвета': nomenclatures['vendorCode'],
                                    'Размер':'0',
                                    'Баркод': barcod,
                                    'Розничная цена, руб': '',#variant['addin'][0]['params'][0]['count']
                                    'Комплектация':''}
                        dataAdvanced = {'id':'',
                        'imtId':'',
                        'object':'',
                        'parant':'',
                        'supplierVendorCode':'',
                        'addin.Бренд':'',
                        'addin.Наименование':'',
                        'addin.Тнвэд':'',
                        'addin.Комплектация':'',
                        'addin.Тран':''
                        }
                        listCard.append(dataDefault)
    listCardpd = pandas.DataFrame(listCard)
    filename = r'Список номенклатуры {}.xlsx'.format(supplier)
    try:
        listCardpd.to_excel(joinPath(pathToDone, filename),index=False)
    except PermissionError:
        filename = r'Список номенклатуры {}_1.xlsx'.format(supplier)
        listCardpd.to_excel(joinPath(pathToDone, filename),index=False)
    return barcodeList


def getListCard(supplier, filter=None):
    loop = asyncio.get_event_loop()
    cardslist = loop.run_until_complete(main(supplier,filter))
    if filter == None:
        return createListNomenclatures(cardslist, supplier)
    else:
        return cardslist
