import aiohttp
import asyncio


class ChangeAvailability:
    def __init__(self, seller, listBarcodes) -> None:
        if seller == 'Э.С. Караханян':
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
        elif seller == 'М.С. Абраамян':
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
        elif seller == 'С.М. Абраамян':
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
        self.token = token
        self.listBarcodes = listBarcodes
        self.url = 'https://suppliers-api.wildberries.ru/api/v2/stocks'
        self.json = []


    def takeOff(self):
        for barcod in self.listBarcodes:
            barcod = str(barcod) if type(barcod) == int else str(barcod)[0:-2] if type(barcod) == float else barcod
            self.json.append({"barcode": barcod,
                            "stock": 0,
                            "warehouseId": 10237})
            return self.requestsAsyncMain()
        
        
    def takeOn(self):
        for barcod in self.listBarcodes:
            barcod = str(barcod) if type(barcod) == int else str(barcod)[0:-2] if type(barcod) == float else barcod
            self.json.append({"barcode": barcod,
                            "stock": 1000,
                            "warehouseId": 10237})
            return self.requestsAsyncMain()


    def requestsAsyncMain(self):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.requestsAsync())


    async def requestsAsync(self):
        timerDelay = 5
        async with aiohttp.ClientSession() as session:
            while True:
                async with session.post(self.url, headers={
                        'Authorization': '{}'.format(self.token)}, json=self.json) as response:
                        if response.status != 200:
                            print('Возникла ошибка. STATUS CODE: ' + str(response.status) + ' TEXT: ' + await response.text())
                            if response.status == 429:
                                print('Ждём {} секунд.'.format(str(timerDelay)))
                                await asyncio.sleep(timerDelay)
                                timerDelay +=1
                            await asyncio.sleep(5)
                            continue
                        else:
                            return 0