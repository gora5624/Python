import requests
import pandas
import multiprocessing

class GetstocksFBS():
    def __init__(self) -> None:
        self.tokenList = [
            ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w', 'Караханян'),
            ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM', 'Манвел'),
            ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y', 'Самвел')
        ]
        self.url = 'https://suppliers-api.wildberries.ru/api/v2/stocks?skip={}&take={}'
        manager = multiprocessing.Manager()
        self.data = manager.list()
        



    def getTotalCardSeller(self, token):
        while True:
            response = requests.get(self.url.format('0','1'), headers={
                                    'Authorization': '{}'.format(token)})
            if response.status_code != 200:
                    print(response.status_code)
                    print(response.text)
                    continue
            json = response.json()
            return json['total']
            


    def getCards(self, token, i, ip):
        while True:
            response = requests.get(self.url.format(i,i+1000), headers={
                                    'Authorization': '{}'.format(token)})
            if response.status_code != 200:
                print(response.status_code)
                print(response.text)
                continue
            json = response.json()
            self.data.extend(json['stocks'])
            print(len(self.data))
            break         



    def tasksForGetStokcs(self):        
        tmpList = []
        pool = multiprocessing.Pool()
        for token in self.tokenList:
            totalCardsSeller = self.getTotalCardSeller(token[0])
            tmpList.append((token, totalCardsSeller))
        for line in tmpList:
            totalCardsSeller = line[1]
            token = line[0][0]
            ip = line[0][1]
            totalCardsSeller = self.getTotalCardSeller(token)
            for i in range(0,totalCardsSeller, 1000):
                pool.apply_async(self.getCards, args=(token,i,ip, ))
        pool.close()
        pool.join()


    def startGetStocksFBS(self):
        self.tasksForGetStokcs()
        pd = pandas.DataFrame(list(self.data))
        pd.to_excel(r'E:\\123.xlsx')


if __name__ == '__main__':
    a = GetstocksFBS()
    a.startGetStocksFBS()