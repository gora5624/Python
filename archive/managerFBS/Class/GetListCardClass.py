import aiohttp
import asyncio
import requests
from aiohttp import ClientPayloadError, ServerDisconnectedError, ClientOSError

class GetlistCard():
    def __init__(self, seller) -> None:
        if seller == 'Э.С. Караханян':
            self.tokenFBO = 'Mjc4YzZhY2YtOTlhMS00NDlkLTgwMTctZmFkMDk2YjQzNWEx'
            self.tokenFBS = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
        elif seller == 'М.С. Абраамян':
            self.tokenFBO = 'ZGRmZGU5ZjMtZjQzMS00MmY1LWE1YjAtM2Y4MWM3MWI0MDVh'
            self.tokenFBS = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
        elif seller == 'С.М. Абраамян':
            self.tokenFBO = 'M2VkZjI3NTQtYmMyOS00ZTYxLWE3NzctZjgwZDZhOWEyNTgw'
            self.tokenFBS = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
        self.cardslist = []

    async def getListCardMain(self):
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
                            'Authorization': '{}'.format(self.tokenFBS)}, json=datajson)
            if totalCardsResponse.status_code ==200:
                break
            else:
                print(str(totalCardsResponse.status_code))
                continue
        totalCards = totalCardsResponse.json()['result']['cursor']['total']
        tasks = []
        async with aiohttp.ClientSession() as session:
            for offset in range(0,totalCards,10):
                tasks.append(asyncio.create_task(self.getCard(session, offset, Url)))
            await asyncio.wait(tasks)
        return self.cardslist


    async def getCard(self, session, offset, Url):
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
        while True:
            try:
                async with session.post(Url, headers={
                                'Authorization': '{}'.format(self.tokenFBS)}, json=datajson) as response: 
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
                                if 'error' not in jsonCard.keys():
                                    datajson['params']['query']['offset'] = offset
                                    self.cardslist.extend(jsonCard['result']['cards'])
                                    break
            except ServerDisconnectedError:
                tasks = []
                print('ServerDisconnectedError in updateOneCard, create new session')
                await asyncio.sleep(15)
                async with aiohttp.ClientSession() as sessionNew:
                    tasks.append(asyncio.create_task(self.getCard(sessionNew, offset, Url)))
                    await asyncio.wait(tasks)
                break
            except ClientOSError:
                tasks = []
                print('ClientOSError in updateOneCard, create new session')
                await asyncio.sleep(15)
                async with aiohttp.ClientSession() as sessionNew:
                    tasks.append(asyncio.create_task(self.getCard(sessionNew, offset, Url)))
                    await asyncio.wait(tasks)
                break
            except asyncio.TimeoutError:
                tasks = []
                print('TimeoutError in updateOneCard, create new session')
                await asyncio.sleep(20)
                async with aiohttp.ClientSession() as sessionNew:
                    tasks.append(asyncio.create_task(self.getCard(sessionNew, offset, Url)))
                    await asyncio.wait(tasks)
                break
            # finally:
            #     tasks = []
            #     print('Unknown in updateOneCard, create new session')
            #     await asyncio.sleep(20)
            #     async with aiohttp.ClientSession() as sessionNew:
            #         tasks.append(asyncio.create_task(self.getCard(sessionNew, session, offset, Url)))
            #         await asyncio.wait(tasks)
            #     break

    def getListCard(self):
        loop = asyncio.get_event_loop()
        result =  loop.run_until_complete(self.getListCardMain())
        return result

if __name__ == '__main__':
    a = GetlistCard('С.М. Абраамян')
    b = a.getListCard()