
from os.path import abspath, join as joinPath
import sys
sys.path.append(abspath(joinPath(__file__,'../..')))
from Moduls.GetCardAsincio import getListCard
import asyncio
import aiohttp
from aiohttp import ClientOSError, ServerDisconnectedError       

TokenKar = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
TokenArb = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
TokenSam = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'

class ImageCheker:
    def __init__(self, listCase, supplier) -> None:
        if supplier =='Караханян':
            self.token = TokenKar
        elif supplier =='Абраамян':
            self.token = TokenArb
        elif supplier =='Самвел':
            self.token = TokenSam
        self.listBarcods = self.getListBarcode(listCase)
        self.listVendorCods = self.getVendorCods(listCase)
        self.listCards = getListCard(supplier, self.listVendorCods)
        self.listCardsForUpdate = []
        self.listImages = self.getlistImages(listCase)
        self.status = 'Есть пустые фото'


    def getListBarcode(self, listCase):
        listBarcods = []
        for case in listCase:
            Barcode = case['Баркод'] if type(case['Баркод']) == str else str(case['Баркод'])[0:-2] if type(case['Баркод']) == float else str(case['Баркод'])
            listBarcods.append(Barcode)
        return listBarcods

    def getVendorCods(self, listCase):
        listVendorCods = []
        for case in listCase:
            if case['Артикул поставщика'] not in listVendorCods:
                listVendorCods.append(case['Артикул поставщика'])
        return listVendorCods

    def getlistImages(self, listCase):
        listImages = {}
        for case in listCase:
            Barcode = case['Баркод'] if type(case['Баркод']) == str else str(case['Баркод'])[0:-2] if type(case['Баркод']) == float else str(case['Баркод'])
            dataTMP = {Barcode: case['Путь к файлу'].split('#')}
            listImages.update(dataTMP)
        return listImages

    def setImageForCards(self, force):
        self.listCardsForUpdate = []
        for card in self.listCards:
            cardUpdate = True
            for nomenclature in card['nomenclatures']:
                imageUpdate = False
                for variant in nomenclature['variations']:
                    for barcod in variant['barcodes']:
                        if barcod not in self.listBarcods:
                            print('Штихкод {} не принадлежит карточке'.format(barcod))
                            continue
                        else:
                            for addin in nomenclature['addin']:
                                if addin['type'] == 'Фото':
                                    # if len(addin['params']) == len(self.listImages[barcod]):
                                    #     imageUpdate = True
                                    #     cardUpdate = True * cardUpdate
                                    #     continue
                                    if force == 2:
                                        TMPList = []
                                        for imageURL in self.listImages[barcod]:
                                            dataTMP = {'value': imageURL}
                                            TMPList.append(dataTMP)
                                            addin['params'] = TMPList
                                        cardUpdate = False * cardUpdate
                                    elif len(addin['params']) == len(self.listImages[barcod]):
                                        imageUpdate = True
                                        cardUpdate = True * cardUpdate
                                        continue
                                    else:
                                        TMPList = []
                                        for imageURL in self.listImages[barcod]:
                                            dataTMP = {'value': imageURL}
                                            TMPList.append(dataTMP)
                                            addin['params'] = TMPList
                                        cardUpdate = False * cardUpdate
                                    imageUpdate = True
                                    break
                            if not imageUpdate:
                                TMPList = []
                                for imageURL in self.listImages[barcod]:
                                    dataTMP = {'value': imageURL}
                                    TMPList.append(dataTMP)
                                dataImage = {'type':'Фото',
                                             'params':TMPList}
                                nomenclature['addin'].append(dataImage)
                                cardUpdate = False * cardUpdate
            if not cardUpdate:
                self.listCardsForUpdate.append(card)

    async def updateOneCard(self, session, card):
        Url = 'https://suppliers-api.wildberries.ru/card/update'
        json = {
            "id": '1',
            "jsonrpc": "2.0",
            "params": {
                "card": card
            }}
        while True:
            try:
                async with session.post(Url, headers={
                            'Authorization': '{}'.format(self.token)}, json=json) as response: 
                    if 'Комплектация' in await response.text():
                        card['addin'].append({'type': 'Комплектация',
                                                'params':[{'value': 'Чехол 1 шт'}]})
                        json = {
                                "id": '1',
                                "jsonrpc": "2.0",
                                "params": {
                                    "card": card
                                }}
                        continue
                    if 'connect error' in await response.text():
                        continue
                    if 'internal error' in await response.text():
                        continue
                    if 'err' in await response.text():
                        print(await response.text())
                        print(','.join(card["nomenclatures"][0]["variations"][0]['barcodes']))
                        break
                    print(await response.text())
                    break
            except ClientOSError:
                tasks = []
                print('ClientOSError in updateOneCard, create new session')
                await asyncio.sleep(5)
                async with aiohttp.ClientSession() as sessionNew:
                    tasks.append(asyncio.create_task(self.updateOneCard(sessionNew, card)))
                    await asyncio.wait(tasks)
                break
            except ServerDisconnectedError:
                tasks = []
                print('ServerDisconnectedError in updateOneCard, create new session')
                await asyncio.sleep(15)
                async with aiohttp.ClientSession() as sessionNew:
                    tasks.append(asyncio.create_task(self.updateOneCard(sessionNew, card)))
                    await asyncio.wait(tasks)
                break
            # finally:
            #     tasks = []
            #     print('other error in updateOneCard, create new session')
            #     await asyncio.sleep(15)
            #     async with aiohttp.ClientSession() as sessionNew:
            #         tasks.append(asyncio.create_task(self.updateOneCard(sessionNew, card)))
            #         await asyncio.wait(tasks)
            #     break



    async def updateCardsFromList(self):
        tasks = []
        async with aiohttp.ClientSession() as session:
            if len(self.listCardsForUpdate) !=0:
                print('-----------------------------{}-----------------------'.format(len(self.listCardsForUpdate)))
                for card in self.listCardsForUpdate:
                    tasks.append(asyncio.create_task(self.updateOneCard(session, card)))
                await asyncio.wait(tasks)
            else:
                print("Во всех карточках присутствуют фото.")
                self.status = 'Во всех карточках присутствуют фото.'


    def updateCardsStart(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.updateCardsFromList())
        print("Готово.")
        
