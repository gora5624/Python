from urllib import request
import aiohttp
import asyncio
import json
import time
import requests

class ChangeAvailability:
    def __init__(self, seller, listBarcodes) -> None:
        if seller == 'Э.С. Караханян':
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjgxYjczNGVmLWI2OWUtNGRhMi1iNTBiLThkMTEyYWM4MjhkMCJ9.pU1YOOirgRe3Om-WRYT61AofToggCLbV3na7GbXKGqU'
            warehouseId = 10237
        elif seller == 'М.С. Абраамян':
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjNhZmUzMzMzLWFmYjEtNDI5Yi1hN2Q1LTE1Yjc4ODg4MmU5MSJ9.kWUDkHkGrtD8WxE9sQHto5B7L3bQh-XRDf7EeZQiw7A'
            warehouseId = 141069
        elif seller == 'С.М. Абраамян':
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImUxNGFmM2UxLTc0YTctNDlkOC1hNGIyLTI1Y2Q4ZDc2YmM4NSJ9.bCTyIoPVS3wpbzy7TdK-Gt8Sgz3iyPamzJjnA_EH3Iw'
            warehouseId = 278784
        self.token = token
        self.warehouseId = warehouseId
        self.listBarcodes = listBarcodes
        self.url = 'https://suppliers-api.wildberries.ru/api/v3/stocks/{}'
        
        self.json = {"stocks": []}


    def takeOff(self):
        #return 0
        if len(self.listBarcodes)!=0:
            if type(self.listBarcodes[0]) != dict:
                for barcod in self.listBarcodes:
                    barcod = str(barcod) if type(barcod) == int else str(barcod)[0:-2] if type(barcod) == float else barcod
                    self.json.append({"barcode": barcod,
                                    "stock": 0,
                                    "warehouseId": self.warehouseId})
                return self.requestsAsyncMainDelet()
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
                return self.requestsAsyncMainDelet()
        
    #Тесовый функционал удаления остатков
    def takeOffDelet(self):
        #return 0
        if len(self.listBarcodes)!=0:
            if type(self.listBarcodes[0]) != dict:
                for barcod in self.listBarcodes:
                    barcod = str(barcod) if type(barcod) == int else str(barcod)[0:-2] if type(barcod) == float else barcod
                    self.json.append({"barcode": barcod,
                                    "warehouseId": self.warehouseId})
                return self.requestsAsyncMainDelet()
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
                    try:
                        count = int(line['count'])
                    except:
                        count = 10000
                    barcod = str(barcod) if type(barcod) == int else str(barcod)[0:-2] if type(barcod) == float else barcod
                    self.json['stocks'].append({
                                    "sku": barcod,
                                    "amount": count
                                    })
                return self.req()


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
                    async with session.delete(self.url.format(self.warehouseId), headers={
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
            # await response.text()
            return 0


    async def requestsAsync(self):
        errors = True
        timerDelay = 5
        for i in range(0,len(self.json),900):
            async with aiohttp.ClientSession() as session:
                while True:
                    json_ = {'stocks':self.json['stocks'][i:i+900] }
                    async with session.put(self.url.format(self.warehouseId), headers={
                            'Authorization': '{}'.format(self.token)}, json=json_) as response:
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

    def req(self):
        for i in range(0,len(self.json),900):
            json_ = {'stocks':self.json['stocks'][i:i+900] }
            response = requests.put(self.url.format(self.warehouseId), headers={
                    'Authorization': '{}'.format(self.token)}, json=json_)
            if response.status_code != 204:
                print('Возникла ошибка. STATUS CODE: ' + str(response.status_code) + ' TEXT: ' + response.text)
                if response.status_code == 429:
                    time.sleep(1)