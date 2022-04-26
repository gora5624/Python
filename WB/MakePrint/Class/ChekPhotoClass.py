
from GetCardAsincio import getListCard
import asyncio
import aiohttp

TokenKar = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
TokenArb = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'

class ImageCheker:
    def __init__(self, listCase, supplier) -> None:
        self.token = TokenKar if supplier =='Караханян' else TokenArb
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

    def setImageForCards(self):
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
                                    if len(addin['params']) == len(self.listImages[barcod]):
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
        async with session.post(Url, headers={
                        'Authorization': '{}'.format(self.token)}, json=json) as response: 
            print(await response.text())          


    async def updateCardsFromList(self):
        tasks = []
        async with aiohttp.ClientSession() as session:
            if len(self.listCardsForUpdate) !=0:
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
        
