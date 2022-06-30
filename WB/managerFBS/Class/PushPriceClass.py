import aiohttp
import asyncio
from aiohttp import ClientPayloadError, ServerDisconnectedError, ClientOSError
import pandas


class PushPrice():
    def __init__(self, seller, price, discount, filter) -> None:
        if seller == 'Э.С. Караханян':
            self.tokenFBO = 'Mjc4YzZhY2YtOTlhMS00NDlkLTgwMTctZmFkMDk2YjQzNWEx'
            self.tokenFBS = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
        elif seller == 'М.С. Абраамян':
            self.tokenFBO = 'ZGRmZGU5ZjMtZjQzMS00MmY1LWE1YjAtM2Y4MWM3MWI0MDVh'
            self.tokenFBS = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
        elif seller == 'С.М. Абраамян':
            self.tokenFBO = 'M2VkZjI3NTQtYmMyOS00ZTYxLWE3NzctZjgwZDZhOWEyNTgw'
            self.tokenFBS = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
        self.price = int(price)
        self.discount = int(discount)
        self.priceMax = int(self.getPriceMax())
        self.filter = filter
        self.countnmIDInRequest = 1000
        self.urlPrice = 'https://suppliers-api.wildberries.ru/public/api/v1/prices'
        self.urlDiscount = 'https://suppliers-api.wildberries.ru/public/api/v1/updateDiscounts'
        self.urlRevokeDiscount = 'https://suppliers-api.wildberries.ru/public/api/v1/revokeDiscounts'


    def getPriceMax(self):
        return self.price/((100-int(self.discount))/100)


    async def pushPriceMain(self, session, nmIdList):
        dataJson = []
        for nmId in nmIdList:
            dataJson.append(
                        {
                            "nmId": int(nmId),
                            "price": int(self.priceMax)
                        })
        while True:
            try:
                async with session.post(self.urlPrice, headers={
                                'Authorization': '{}'.format(self.tokenFBS)}, json=dataJson) as response: 
                            if response.status == 408:
                                await asyncio.sleep(20)
                                continue
                            elif response.status == 504:
                                await asyncio.sleep(20)
                                continue
                            elif response.status != 200:
                                if 'все номенклатуры с ценами' in await response.text():
                                    break
                                print(response.status)
                                print(await response.text())
                                await asyncio.sleep(5)
                                continue
                            else:
                                try:
                                    print(await response.text())
                                except ClientPayloadError:
                                    await asyncio.sleep(5)
                                    print('ClientPayloadError in getCard')
                                    continue
                                if 'error' in await response.text():
                                    await response.text()
                                    break
                                elif 'alreadyExists' in await response.text():
                                    await response.text()
                                    break
                                else:
                                    break

            except ServerDisconnectedError:
                tasks = []
                print('ServerDisconnectedError in updateOneCard, create new session')
                await asyncio.sleep(15)
                async with aiohttp.ClientSession() as sessionNew:
                    tasks.append(asyncio.create_task(self.pushPriceMain(sessionNew, nmIdList)))
                    await asyncio.wait(tasks)
                break
            except ClientOSError:
                tasks = []
                print('ClientOSError in updateOneCard, create new session')
                await asyncio.sleep(15)
                async with aiohttp.ClientSession() as sessionNew:
                    tasks.append(asyncio.create_task(self.pushPriceMain(sessionNew, nmIdList)))
                    await asyncio.wait(tasks)
                break
            except asyncio.TimeoutError:
                tasks = []
                print('TimeoutError in updateOneCard, create new session')
                await asyncio.sleep(20)
                async with aiohttp.ClientSession() as sessionNew:
                    tasks.append(asyncio.create_task(self.pushPriceMain(sessionNew, nmIdList)))
                    await asyncio.wait(tasks)
                break

    
    async def pushDiscountMain(self, session, nmIdList):
        dataJson = []
        for nmId in nmIdList:
            dataJson.append(
                        {
                            "discount": self.discount,
                            "nm": int(nmId)
                        })
        while True:
            try:
                async with session.post(self.urlDiscount, headers={
                                'Authorization': '{}'.format(self.tokenFBS)}, json=dataJson) as response: 
                            if response.status == 408:
                                await asyncio.sleep(20)
                                continue
                            elif response.status == 504:
                                await asyncio.sleep(20)
                                continue
                            elif response.status != 200:
                                if 'все номенклатуры со скидками' in await response.text():
                                    break
                                print(response.status)
                                print(await response.text())
                                await asyncio.sleep(5)
                                continue
                            else:
                                try:
                                    print(await response.text())
                                except ClientPayloadError:
                                    await asyncio.sleep(5)
                                    print('ClientPayloadError in getCard')
                                    continue
                                if 'error' in await response.text():
                                    await response.text()
                                    break
                                elif 'alreadyExists' in await response.text():
                                    await response.text()
                                    break
                                else:
                                    break

            except ServerDisconnectedError:
                tasks = []
                print('ServerDisconnectedError in updateOneCard, create new session')
                await asyncio.sleep(15)
                async with aiohttp.ClientSession() as sessionNew:
                    tasks.append(asyncio.create_task(self.pushDiscountMain(sessionNew, nmIdList)))
                    await asyncio.wait(tasks)
                break
            except ClientOSError:
                tasks = []
                print('ClientOSError in updateOneCard, create new session')
                await asyncio.sleep(15)
                async with aiohttp.ClientSession() as sessionNew:
                    tasks.append(asyncio.create_task(self.pushDiscountMain(sessionNew, nmIdList)))
                    await asyncio.wait(tasks)
                break
            except asyncio.TimeoutError:
                tasks = []
                print('TimeoutError in updateOneCard, create new session')
                await asyncio.sleep(20)
                async with aiohttp.ClientSession() as sessionNew:
                    tasks.append(asyncio.create_task(self.pushDiscountMain(sessionNew, nmIdList)))
                    await asyncio.wait(tasks)
                break


    async def pushPriceTask(self):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for i in range(0,len(self.filter.nmIdList),self.countnmIDInRequest):
                tasks.append(asyncio.create_task(self.pushPriceMain(session, self.filter.nmIdList[i: i + self.countnmIDInRequest])))
                tasks.append(asyncio.create_task(self.pushDiscountMain(session, self.filter.nmIdList[i: i + self.countnmIDInRequest])))
            await asyncio.wait(tasks)

    def pushPrice(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.pushPriceTask())