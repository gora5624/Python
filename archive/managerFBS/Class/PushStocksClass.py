import aiohttp
import asyncio
from aiohttp import ClientPayloadError, ServerDisconnectedError, ClientOSError

class PushStocks():
    def __init__(self, seller, availability, filter) -> None:
        if seller == 'Э.С. Караханян':
            self.tokenFBO = 'Mjc4YzZhY2YtOTlhMS00NDlkLTgwMTctZmFkMDk2YjQzNWEx'
            self.tokenFBS = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
            self.warehouseId = 10237
        elif seller == 'М.С. Абраамян':
            self.tokenFBO = 'ZGRmZGU5ZjMtZjQzMS00MmY1LWE1YjAtM2Y4MWM3MWI0MDVh'
            self.tokenFBS = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
            self.warehouseId = 141069
        elif seller == 'С.М. Абраамян':
            self.tokenFBO = 'M2VkZjI3NTQtYmMyOS00ZTYxLWE3NzctZjgwZDZhOWEyNTgw'
            self.tokenFBS = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
            self.warehouseId = 278784
        self.availability = availability
        self.filter = filter
        self.countBarcodInRequest = 10000
        self.url = 'https://suppliers-api.wildberries.ru/api/v2/stocks'

    async def pushStocksMain(self, session, barcodList):
        dataJson = []
        for barcod in barcodList:
            if type(barcod) == str:
                barcod = barcod
            elif type(barcod) == float:
                barcod = str(barcod)[0:-2]
            elif type(barcod) == int:
                barcod = str(barcod)
            dataJson.append(
                        {
                            "barcode": barcod,
                            "stock": self.availability,
                            "warehouseId": self.warehouseId
                        })
        while True:
            try:
                async with session.post(self.url, headers={
                                'Authorization': '{}'.format(self.tokenFBS)}, json=dataJson) as response: 
                            if response.status != 200:
                                print(response.status)
                                print(await response.text())
                                await asyncio.sleep(5)
                                continue
                            else:
                                try:
                                    jsonCard = await response.json()
                                except ClientPayloadError:
                                    await asyncio.sleep(5)
                                    print('ClientPayloadError in getCard')
                                    continue
                                if jsonCard['error'] == True:
                                    print(str(jsonCard['data']['errors']))
                                    break
                                else:
                                    break

            except ServerDisconnectedError:
                tasks = []
                print('ServerDisconnectedError in updateOneCard, create new session')
                await asyncio.sleep(15)
                async with aiohttp.ClientSession() as sessionNew:
                    tasks.append(asyncio.create_task(self.pushStocksMain(sessionNew, barcodList)))
                    await asyncio.wait(tasks)
                break
            except ClientOSError:
                tasks = []
                print('ClientOSError in updateOneCard, create new session')
                await asyncio.sleep(15)
                async with aiohttp.ClientSession() as sessionNew:
                    tasks.append(asyncio.create_task(self.pushStocksMain(sessionNew, barcodList)))
                    await asyncio.wait(tasks)
                break
            except asyncio.TimeoutError:
                tasks = []
                print('TimeoutError in updateOneCard, create new session')
                await asyncio.sleep(20)
                async with aiohttp.ClientSession() as sessionNew:
                    tasks.append(asyncio.create_task(self.pushStocksMain(sessionNew, barcodList)))
                    await asyncio.wait(tasks)
                break

    async def pushStocksTask(self):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for i in range(0,len(self.filter.barcodList),self.countBarcodInRequest):
                tasks.append(asyncio.create_task(self.pushStocksMain(session, self.filter.barcodList[i: i + self.countBarcodInRequest])))
            await asyncio.wait(tasks)

    def pushStocks(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.pushStocksTask())