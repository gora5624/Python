from email import header
import aiohttp
import asyncio
from aiohttp import ClientPayloadError, ServerDisconnectedError, ClientOSError
import pandas
import json
if __name__ == '__main__':
    from SplitStocksClass import SplitStocks
else:
    from Class.SplitStocksClass import SplitStocks

class GetStocks:
    def __init__(self, seller) -> None:
        if seller == 'Э.С. Караханян':
            tokenFBO = 'Mjc4YzZhY2YtOTlhMS00NDlkLTgwMTctZmFkMDk2YjQzNWEx'
            tokenFBS = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
        elif seller == 'М.С. Абраамян':
            tokenFBO = 'ZGRmZGU5ZjMtZjQzMS00MmY1LWE1YjAtM2Y4MWM3MWI0MDVh'
            tokenFBS = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
        elif seller == 'С.М. Абраамян':
            tokenFBO = 'M2VkZjI3NTQtYmMyOS00ZTYxLWE3NzctZjgwZDZhOWEyNTgw'
            tokenFBS = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
        self.tokenFBO = tokenFBO
        self.tokenFBS = tokenFBS
        self.urlStocks = 'https://suppliers-stats.wildberries.ru/api/v1/supplier/stocks?dateFrom=2019-01-01&key={}'
        self.urlPrice = 'https://suppliers-api.wildberries.ru/public/api/v1/info?quantity=0'


    async def getStocksTask(self):
        # loop = asyncio.get_event_loop()
        stocksTask = asyncio.create_task(self.getStocks())
        priceTask = asyncio.create_task(self.getPrice())
        stocks = await stocksTask
        price = await priceTask
        # price.to_excel(r'E:\price.xlsx', index=False)
        stocksWithPrice = stocks.drop(labels=['Price', 'Discount'],axis=1).merge(price, how='inner',on='nmId')
        #stocksWithPrice.to_excel(r'E:\123.xlsx', index=False)
        return stocksWithPrice
        # return loop.run_until_complete(self.getStocks())
        # quatityWithPrice.to_excel(r'E:\123.xlsx', index=False)


    def getStocksMain(self):
        return asyncio.run(self.getStocksTask())


    async def getPrice(self):
        while True:
            async with aiohttp.ClientSession() as session:
                while True:
                    try:
                        async with session.get(self.urlPrice, headers = {'Authorization': '{}'.format(self.tokenFBS)}) as response: 
                                if response.status != 200:
                                    print('Возникла ошибка при получении цен. STATUS CODE: ' + str(response.status) + ' TEXT: ' + await response.text())
                                    await asyncio.sleep(5)
                                    continue
                                else:
                                    try:
                                        data = json.loads(await response.text())
                                    except ClientPayloadError:
                                        print('Возникла ошибка с json. STATUS CODE: ' + str(response.status))
                                        await asyncio.sleep(5)
                                        continue
                                    break
                    except ClientOSError:
                        continue

            if data == None:
                continue
            else:
                break
        priceList = pandas.DataFrame(data)
        # quatity.to_excel(r'E:\quatity.xlsx', index=False)
        priceList['nmId']=priceList['nmId'].astype(str)
        return priceList


    async def getStocks(self):
        timerDelay = 5
        while True:
            async with aiohttp.ClientSession() as session:
                while True:
                    async with session.get(self.urlStocks.format(self.tokenFBO)) as response: 
                            if response.status != 200:
                                print('Возникла ошибка при получении остатков. STATUS CODE: ' + str(response.status) + ' TEXT: ' + await response.text())
                                if response.status == 429:
                                    print('Ждём {} секунд.'.format(str(timerDelay)))
                                    await asyncio.sleep(timerDelay)
                                    timerDelay +=1
                                await asyncio.sleep(5)
                                continue
                            else:
                                try:
                                    data = await response.json()
                                except ClientPayloadError:
                                    print('Возникла ошибка с json. STATUS CODE: ' + str(response.status))
                                    await asyncio.sleep(5)
                                    continue
                                break

            if data == None:
                continue
            else:
                break
        quatity = pandas.DataFrame(data)
        # quatity.to_excel(r'E:\quatity.xlsx', index=False)
        quatity = quatity[quatity.quantity != 0]
        quatity['barcode']=quatity['barcode'].astype(str)
        quatity['nmId']=quatity['nmId'].astype(str)
        typeCase = SplitStocks.getTypeCase()
        typeCase['barcode']=typeCase['barcode'].astype(str)
        quatityWithType = quatity.merge(typeCase, how='inner',on='barcode')
        # quatityWithType.to_excel(r'E:\quatityWithType.xlsx', index=False)
        return quatityWithType


if __name__ == '__main__':
    a = GetStocks('Э.С. Караханян')
    quatity = a.getStocksMain()
    # quatity['barcode']=quatity['barcode'].astype(str)
    # typeCase = SplitStocks.getTypeCase()
    # typeCase['barcode']=typeCase['barcode'].astype(str)
    # quatityWithType = quatity.merge(typeCase, how='inner',on='barcode')
    # quatityWithType.to_excel(r'E:\123.xlsx', index=False)
