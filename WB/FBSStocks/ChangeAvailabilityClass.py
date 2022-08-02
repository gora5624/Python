import aiohttp
import asyncio
import json


class ChangeAvailability:
    def __init__(self, seller, listBarcodes) -> None:
        if seller == 'Э.С. Караханян':
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
            warehouseId = 10237
        elif seller == 'М.С. Абраамян':
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
            warehouseId = 141069
        elif seller == 'С.М. Абраамян':
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
            warehouseId = 278784
        self.token = token
        self.warehouseId = warehouseId
        self.listBarcodes = listBarcodes
        self.url = 'https://suppliers-api.wildberries.ru/api/v2/stocks'
        
        self.json = []


    def takeOff(self):
        #return 0
        if len(self.listBarcodes)!=0:
            if type(self.listBarcodes[0]) != dict:
                for barcod in self.listBarcodes:
                    barcod = str(barcod) if type(barcod) == int else str(barcod)[0:-2] if type(barcod) == float else barcod
                    self.json.append({"barcode": barcod,
                                    "stock": 0,
                                    "warehouseId": self.warehouseId})
                return self.requestsAsyncMain()
            else:
                tmpList = []
                for line in self.listBarcodes:
                    tmpList.append(line['barcod'])
                self.listBarcodes = tmpList
                for barcod in self.listBarcodes:
                    barcod = str(barcod) if type(barcod) == int else str(barcod)[0:-2] if type(barcod) == float else barcod
                    self.json.append({"barcode": barcod,
                                    "stock": 0,
                                    "warehouseId": self.warehouseId})
                return self.requestsAsyncMain()
        
    #Тесовый функционал удаления остатков
    def takeOffDelet(self):
        #return 0
        if len(self.listBarcodes)!=0:
            if type(self.listBarcodes[0]) != dict:
                for barcod in self.listBarcodes:
                    barcod = str(barcod) if type(barcod) == int else str(barcod)[0:-2] if type(barcod) == float else barcod
                    self.json.append({"barcode": barcod,
                                    "warehouseId": self.warehouseId})
                return self.requestsAsyncMain()
            else:
                tmpList = []
                for line in self.listBarcodes:
                    tmpList.append(line['barcod'])
                self.listBarcodes = tmpList
                for barcod in self.listBarcodes:
                    barcod = str(barcod) if type(barcod) == int else str(barcod)[0:-2] if type(barcod) == float else barcod
                    self.json.append({"barcode": barcod,
                                    "warehouseId": self.warehouseId})
                return self.requestsAsyncMainDelet()


    def takeOn(self, count = 10000):
        #return 0
        if len(self.listBarcodes)!=0:
            if type(self.listBarcodes[0]) != dict:
                for barcod in self.listBarcodes:
                    barcod = str(barcod) if type(barcod) == int else str(barcod)[0:-2] if type(barcod) == float else barcod
                    self.json.append({"barcode": barcod,
                                    "stock": count,
                                    "warehouseId": self.warehouseId})
                return self.requestsAsyncMain()
            else:
                for line in self.listBarcodes:
                    barcod = line['barcod']
                    count = int(line['count'])
                    barcod = str(barcod) if type(barcod) == int else str(barcod)[0:-2] if type(barcod) == float else barcod
                    self.json.append({"barcode": barcod,
                                    "stock": count,
                                    "warehouseId": self.warehouseId})
                return self.requestsAsyncMain()


    def requestsAsyncMain(self):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.requestsAsync())

    #Тесовый функционал удаления остатков
    def requestsAsyncMainDelet(self):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.requestsAsyncDelet())


    #Тесовый функционал удаления остатков
    async def requestsAsyncDelet(self):
        errors = True
        timerDelay = 5
        for i in range(0,len(self.json),9000):
            async with aiohttp.ClientSession() as session:
                while True:
                    async with session.delete(self.url, headers={
                            'Authorization': '{}'.format(self.token)}, json=self.json[i:i+9000]) as response:
                            if response.status != 200:
                                print('Возникла ошибка. STATUS CODE: ' + str(response.status) + ' TEXT: ' + await response.text())
                                if response.status == 429:
                                    print('Ждём {} секунд.'.format(str(timerDelay)))
                                    await asyncio.sleep(timerDelay)
                                    timerDelay +=1
                                await asyncio.sleep(5)
                                continue
                            else:
                                errors = False
                                break
        if not errors:
            return 0


    async def requestsAsync(self):
        errors = True
        timerDelay = 5
        for i in range(0,len(self.json),9000):
            async with aiohttp.ClientSession() as session:
                while True:
                    async with session.post(self.url, headers={
                            'Authorization': '{}'.format(self.token)}, json=self.json[i:i+9000]) as response:
                            if response.status != 200:
                                print('Возникла ошибка. STATUS CODE: ' + str(response.status) + ' TEXT: ' + await response.text())
                                if response.status == 429:
                                    print('Ждём {} секунд.'.format(str(timerDelay)))
                                    await asyncio.sleep(timerDelay)
                                    timerDelay +=1
                                await asyncio.sleep(5)
                                continue
                            else:
                                errors = False
                                break
        if not errors:
            return 0