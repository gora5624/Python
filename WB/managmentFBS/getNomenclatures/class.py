import pandas
import requests
import multiprocessing
import os
import time

class nomenclaturesGetter():
    def __init__(self, token) -> None:
        self.mainPath = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК'
        self.urlGetNom = 'https://suppliers-api.wildberries.ru/content/v1/cards/cursor/list'
        self.timeout = 10
        self.ip = token['IPName']
        self.token = token['token']
        self.dataBase = []
        

    def log(self, text):
        with open(os.path.join(__file__,'..','log.txt'), 'a') as fileLog:
            fileLog.write(text + '\n')
            fileLog.close()


    def getNomFromWB(self, updatedAt='',nmID='', timeout=5):
        dataCards = []
        if timeout> 300:
            return 0
        if updatedAt == '' and nmID == '':
            jsonRequestsGetCardFirst = {
                    "sort": {
                        "cursor": {
                            'limit': 1000
                        },
                        "filter": {
                        "withPhoto": -1
                        },
                        "sort": {
                        "sortColumn": "updateAt"
                        }
                    }
                    }
        else:
            jsonRequestsGetCardFirst = {
                    "sort": {
                        "cursor": {
                        "updatedAt": updatedAt,
                        'limit': 1000,
                        "nmID": nmID,
                        },
                        "filter": {
                        "withPhoto": -1
                        },
                        "sort": {
                        "sortColumn": "updateAt"
                        }
                    }
                    }
        headersGetCard = {'Authorization': '{}'.format(self.token)}
        while True:
            if timeout> 300:
                return 0
            try:
                responce = requests.post(self.urlGetNom, json=jsonRequestsGetCardFirst, headers=headersGetCard, timeout=timeout)
                if responce.status_code != 200:
                    timeout += 5
                    self.log(responce.text)
                    continue
                else:
                    data = responce.json()['data']['cards']
                    if len(data) != 0:
                        for card in data:
                            dataCard = {
                                        'nmID':card['nmID'],
                                        'object': card['object'],
                                        'brand': card['brand'],
                                        'vendorCode':card['vendorCode'],
                                        'barcodes': ','.join(card['sizes'][0]['skus']),
                                        'ip': self.ip,
                                        'mediaFiles': card['mediaFiles']
                                    }
                            dataCards.append(dataCard)
                        updatedAt = responce.json()['data']['cursor']['updatedAt']
                        nmID = responce.json()['data']['cursor']['nmID']
                        total = responce.json()['data']['cursor']['total']
                        return dataCards, updatedAt, nmID, total
                    else:
                        timeout +=5
                        continue
            except requests.exceptions.ReadTimeout:
                timeout +=5
                continue
            except requests.exceptions.ConnectionError:
                timeout +=5
                continue
         

    def getPiaceOfNom(self):
        try:
            updatedAt = nmID = ''
            while True:
                try:
                    # a = self.getNomFromWB(updatedAt, nmID)
                    data, updatedAt, nmID, total = self.getNomFromWB(updatedAt, nmID)
                except TypeError:
                    self.createDB()
                    self.log('TypeError')
                    break
                # except:
                #     self.createDB()
                #     print('error')
                #     self.log('error')
                #     break
                self.dataBase.extend(data)
                if total < 1000:
                    self.createDB()
                    break
                else:
                    continue
        except:
            self.createDB()


    def createDB(self):
        if len(list(self.dataBase)) < 1000000:
            df = pandas.DataFrame(self.dataBase)
            df.to_excel(os.path.join(self.mainPath,'cardsTMP {}.xlsx'.format(self.ip)), index=False)
            df.to_csv(os.path.join(self.mainPath,'cardsTMP {}.txt'.format(self.ip)), sep='\t')
        else:
            df = pandas.DataFrame(self.dataBase)
            df.to_csv(os.path.join(self.mainPath,'cardsTMP {}.txt'.format(self.ip)), sep='\t')


    # def start(self):
    #     tokens = [
    #         {
    #             'IPName': 'Самвел',
    #             'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
    #         },
    #         {
    #             'IPName': 'Караханян',
    #             'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
    #         },
    #         {
    #             'IPName': 'Манвел',
    #             'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
    #         }             
    #     ]
    #     pool = multiprocessing.Pool(3)
    #     for token in tokens:
    #         getter = nomenclaturesGetter(token)
    #         pool.apply_async(getter.getPiaceOfNom)
    #     pool.close()
    #     pool.join()

if __name__ == "__main__":
    start_time = time.time()
    tokens = [
                {
                    'IPName': 'Самвел',
                    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
                },
                {
                    'IPName': 'Караханян',
                    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
                },
                {
                    'IPName': 'Манвел',
                    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
                }             
            ]
    pool = multiprocessing.Pool(3)
    for token in tokens:
        getter = nomenclaturesGetter(token)
        pool.apply_async(getter.getPiaceOfNom)
    pool.close()
    pool.join()

    print("--- %s seconds ---" % (time.time() - start_time))