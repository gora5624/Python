from os.path import join as joinPath
import aiohttp
import asyncio
import requests
import pandas

main_path = r'C:\Users\Public\Documents\WBUploadImage'
TokenKar = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
TokenArb = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
pathToDone = (r'F:\\')
DoneList = []
TMP_List = []


async def main(supplier, filter=None):
    Token = TokenKar if supplier =='Караханян' else TokenArb
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
            for offset in range(0,totalCards,100):
                tasks.append(asyncio.create_task(getCard(session, offset, cardslist, Url, Token, filter)))
            await asyncio.wait(tasks)
        else:
            tasks.append(asyncio.create_task(getCard(session, offset, cardslist, Url, Token, filter)))
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
                    "limit": 100,
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
                    "limit": 100,
                    "offset": offset,
                    "total":1000
                },
                "withError": False
            }
        }
    while True:
        async with session.post(Url, headers={
                        'Authorization': '{}'.format(Token)}, json=datajson) as response: 
                    if response.status != 200:
                        print(response.status)
                        print(await response.text())
                        await asyncio.sleep(2)
                        continue
                    else:
                        jsonCard = await response.json()
                        if 'error' not in jsonCard.keys():
                            datajson['params']['query']['offset'] = offset
                            cardslist.extend(jsonCard['result']['cards'])
                            break


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
