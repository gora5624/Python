import pandas
import requests
import multiprocessing
import os
import time

class nomenclaturesGetter():
    def __init__(self) -> None:
        self.pathToListNomenclaturesFrom1c = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\ШК — копия.txt'
        self.mainPath = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК'
        self.tokens = [
                {
                    'IPName': 'Караханян',
                    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
                },
                {
                    'IPName': 'Манвел',
                    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
                },
                {
                    'IPName': 'Самвел',
                    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
                }

            ]
        self.listBarcodes = ''
        self.listVendorCodes = ''
        self.urlGetNom = 'https://suppliers-api.wildberries.ru/content/v1/cards/cursor/list'
        manager = multiprocessing.Manager()
        self.listDoneBarcodes = manager.list()
        self.dataCards = manager.list()
        self.timeout = 10
        
    def readListBarcodes(self):
        dataNomenclaturesFrom1c = pandas.DataFrame(pandas.read_table(self.pathToListNomenclaturesFrom1c, sep='\t'))
        self.listBarcodes = dataNomenclaturesFrom1c['Штрихкод'].values.tolist()


    def log(self, text):
        with open(os.path.join(__file__,'..','log.txt'), 'a') as fileLog:
            fileLog.write(text + '\n')
            fileLog.close()


    def getNomFromWB(self, barcode, token, timeout=0, countTry=0):
        if barcode not in list(self.listDoneBarcodes):
            jsonRequestsGetCardFirst = {
                    "sort": {
                        "cursor": {
                        "limit": 1000
                        },
                        "filter": {
                        "textSearch": str(2044382352843),
                        "withPhoto": -1
                        },
                        "sort": {
                        "sortColumn": "updateAt"
                        }
                    }
                    }

            headersGetCard = {'Authorization': '{}'.format(token['token'])}
            try:
                responce = requests.post(self.urlGetNom, json=jsonRequestsGetCardFirst, headers=headersGetCard, timeout=self.timeout+timeout)
                if countTry <5:
                    if responce.status_code != 200:
                        self.log(responce.text)
                        self.getNomFromWB(barcode, token,0,countTry+1)
                    else:
                        if len(data:=responce.json()['data']['cards']) != 0:
                            for card in data:
                                listDoneBarcodesCard = []
                                for size in card['sizes']:
                                    self.listDoneBarcodes.extend(size['skus'])
                                    listDoneBarcodesCard.extend(size['skus'])
                                dataCard = {
                                    'nmID':card['nmID'],
                                    'object': card['object'],
                                    'Бренд': card['brand'],
                                    'vendorCode':card['vendorCode'],
                                    'barcodes': ','.join(listDoneBarcodesCard),
                                    'ip': token['IPName']
                                }
                                self.dataCards.append(dataCard)
                else:
                    self.log(responce.text + ' countTry>5')
            except requests.exceptions.ReadTimeout:
                if timeout < 60:
                    self.getNomFromWB(barcode, token,timeout+1)
                else:
                    print(str(barcode)+' ReadTimeout')
                    self.log(str(barcode)+' ReadTimeout')
                    return 0
            except requests.exceptions.ConnectTimeout:
                if timeout < 60:
                    self.getNomFromWB(barcode, token,timeout+1)
                else:
                    print(str(barcode)+' ReadTimeout')
                    self.log(str(barcode)+' ReadTimeout')
                    return 0
            except:
                if timeout < 60:
                    self.getNomFromWB(barcode, token,timeout+1)
                else:
                    print(str(barcode)+' ReadTimeout')
                    self.log(str(barcode)+' ReadTimeout')
                    return 0            


    def createDB(self):
        if len(list(self.dataCards)) < 1000000:
            df = pandas.DataFrame(list(self.dataCards))
            df.to_excel(os.path.join(self.mainPath,'cardsTMP.xlsx'))
        else:
            df = pandas.DataFrame(list(self.dataCards))
            df.to_csv(os.path.join(self.mainPath,'cardsTMP.txt'), sep='/t')


    def getNomFromListBarcode(self):
        # manager = multiprocessing.Manager()
        # self.listDoneBarcodes = manager.list()
        # self.dataCards = manager.list()
        pool = multiprocessing.Pool()
        for barcode in self.listBarcodes:
            for token in self.tokens:
                pool.apply_async(self.getNomFromWB, args=(barcode, token))
                # self.getNomFromWB(barcode, token['token'])
        pool.close()
        pool.join()

if __name__ == "__main__":
    start_time = time.time()
    a = nomenclaturesGetter()
    a.readListBarcodes()
    try:
        a.getNomFromListBarcode()
        a.createDB()
    except:
        if len(list(a.dataCards)) < 1000000:
            df = pandas.DataFrame(list(a.dataCards))
            df.to_excel(os.path.join(a.mainPath,'cardsTMP.xlsx'))
        else:
            df = pandas.DataFrame(list(a.dataCards))
            df.to_csv(os.path.join(a.mainPath,'cardsTMP.txt'), sep='/t')
    print("--- %s seconds ---" % (time.time() - start_time))