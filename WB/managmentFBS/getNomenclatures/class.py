import pandas
import requests
import multiprocessing
import os
import time
import copy

class nomenclaturesGetter():
    def __init__(self, token) -> None:
        self.mainPath = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db'
        self.urlGetNom = 'https://suppliers-api.wildberries.ru/content/v1/cards/cursor/list'
        self.timeout = 10
        self.ip = token['IPName']
        self.token = token['token']
        self.dataBase = []
        self.nomenclatures1CDataPath = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\ШК.txt'
        self.nomenclatures1CData = pandas.DataFrame(pandas.read_table(self.nomenclatures1CDataPath, sep='\t'))
        

    def log(self, text):
        with open(os.path.join(__file__,'..','log.txt'), 'a') as fileLog:
            fileLog.write(text + '\n')
            fileLog.close()


    def getNomFromWB(self, updatedAt='',nmID='', timeout=5):
        dataCards = []
        if timeout> 300:
            return 0
        if updatedAt == '' and nmID == '':
            jsonRequestsGetNom = {
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
            jsonRequestsGetNom = {
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
                responce = requests.post(self.urlGetNom, json=jsonRequestsGetNom, headers=headersGetCard, timeout=timeout)
                if responce.status_code != 200:
                    timeout += 5
                    self.log(responce.text)
                    continue
                else:
                    try:
                        data = responce.json()['data']['cards']
                    except requests.exceptions.JSONDecodeError:
                        timeout += 5
                        continue
                    if len(data) != 0:
                        for card in data:
                            dataCard = {
                                        'nmID':card['nmID'],
                                        'object': card['object'],
                                        'brand': card['brand'],
                                        'vendorCode':card['vendorCode'],
                                        # 'barcodes': ','.join(card['sizes'][0]['skus']),
                                        'ip': self.ip,
                                        'mediaFiles': card['mediaFiles']
                                    }
                            for size in card['sizes']:
                                dataCard.update(size)
                                if len(size['skus'])!=0:
                                # if len(size['skus'])>1:
                                    # if len(size['skus']) >1:
                                    #     print('i')
                                    for barcode in size['skus']:
                                        # a = {'sku':barcode}
                                        # dataCard.update(a)
                                        dataCard.update({'sku':barcode})
                                        dataCardCopy = copy.copy(dataCard)
                                        dataCards.append(dataCardCopy)
                                else:
                                    dataCards.append(dataCard)
                            # dataCards.append(dataCard)
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
        # try:
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
        # except:
        #     self.createDB()


    def createDB(self):
        df = pandas.DataFrame(self.dataBase)
        df['barcode'] = df['sku'].astype('string')
        self.nomenclatures1CData['Штрихкод'] = self.nomenclatures1CData['Штрихкод'].astype('string')
        df = pandas.merge(df, self.nomenclatures1CData, how='left', left_on='sku', right_on='Штрихкод')
        df = df.drop(columns=['Штрихкод','barcode'])
        if len(list(self.dataBase)) < 1000000:
            df.to_excel(os.path.join(self.mainPath,'db_nom {}.xlsx'.format(self.ip)), index=False)
        df.to_csv(os.path.join(self.mainPath,'db_nom {}.txt'.format(self.ip)), sep='\t', index=False)
        # else:
        #     df = pandas.DataFrame(self.dataBase)
        #     df['barcode'] = df['sku'].astype('string')
        #     self.nomenclatures1CData['Штрихкод'] = self.nomenclatures1CData['Штрихкод'].astype('string')
        #     df = pandas.merge(df, self.nomenclatures1CData, how='left', left_on='sku', right_on='Штрихкод')
        #     df = df.drop(columns='Штрихкод')
        #     df.to_csv(os.path.join(self.mainPath,'db_nom {}.txt'.format(self.ip)), sep='\t', index=False)

class cardGetter():
    def __init__(self, token) -> None:
        self.mainPath = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db'
        self.urlGetCard = 'https://suppliers-api.wildberries.ru/content/v1/cards/filter'
        self.listDbNom = []
        self.listVendorCodeToGet = []
        self.listVendorCodeDone = []
        self.DbCards = []
        self.pathToDbNom = token['pathToDB']
        self.ip = token['IPName']
        self.token = token['token']
        self.nomenclatures1CDataPath = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\ШК.txt'
        self.nomenclatures1CData = pandas.DataFrame(pandas.read_table(self.nomenclatures1CDataPath, sep='\t'))
        self.getListVendorCode()
    
    
    def getListVendorCode(self):
        self.listVendorCodeToGet = pandas.DataFrame(pandas.read_table(self.pathToDbNom, sep='\t'))['vendorCode'].values.tolist()


    def getNom(self):
        # pool = multiprocessing.Pool(1)
        # for i in range(0,len(self.listVendorCodeToGet),100):
        #     pool.apply_async(self.getNomProcess, args=(self.listVendorCodeToGet[i:i+100], ))
        # pool.close()
        # pool.join()
        for i, vendorCode in enumerate(self.listVendorCodeToGet):
            if vendorCode not in self.listVendorCodeDone:
                self.getNomProcess([vendorCode], i)
        df = pandas.DataFrame(self.DbCards)
        df = pandas.merge(df, self.nomenclatures1CData, how='left', left_on='sku', right_on='Штрихкод')
        df = df.drop(columns='Штрихкод')
        if len(self.DbCards) <1000000:
            df.to_excel(os.path.join(self.mainPath, 'DB_card {}.xlsx'.format(self.ip)), index=False)
        df.to_csv(os.path.join(self.mainPath, 'DB_card {}.txt'.format(self.ip)), index=False, sep='\t')


    def getNomProcess(self, vendorCodes, i, timeout=20):
        headersGetCard = {'Authorization': '{}'.format(self.token)}
        jsonRequestsGetCard = {
                            "vendorCodes": vendorCodes
                            }
        while True:
            try:
                responce = requests.post(url=self.urlGetCard, json=jsonRequestsGetCard, headers=headersGetCard, timeout=timeout)
                if responce.status_code != 200:
                    timeout+=5
                    continue
                try:
                    data = responce.json()['data']
                except requests.exceptions.JSONDecodeError:
                    timeout+=5
                    continue
                for card in data:
                    self.listVendorCodeDone.append(card['vendorCode'])
                    try:
                        self.listVendorCodeToGet.remove(card['vendorCode'])
                    except ValueError:
                        pass
                    dataNew = {
                        'imtID':card['imtID'],
                        'nmID':card['nmID'],
                        'vendorCode':card['vendorCode'],
                        'mediaFiles':card['mediaFiles'],
                        'group': i
                        # 'sku':'',
                        # 'skus':'',
                        # 'isManySkus':'',
                        # 'price':'',
                        # 'chrtID':''
                    }
                    for char in card['characteristics']:
                        dataNew.update(char)
                    for size in card['sizes']:
                        dataNew.update(size)
                        if len(size['skus']) > 1:
                            dataNew.update({'isManyskus':True})
                        else:
                            dataNew.update({'isManyskus':False})
                        if len(size['skus']) != 0:
                            for sku in size['skus']:
                                dataNew.update({'sku':sku})
                                self.DbCards.append(dataNew)
                        else:
                            self.DbCards.append(dataNew)          
                self.DbCards                                         
                break
                # self.DbCards
                # df = pandas.DataFrame(self.DbCards)
                # df.to_excel(r'E:\\tmp.xlsx', index=False)
                    
            except requests.exceptions.ReadTimeout:
                timeout+=5
                continue
            except requests.exceptions.ConnectionError:
                timeout+=5
                continue
        

if __name__ == "__main__":
    start_time = time.time()
    b = {
                        'IPName': 'Самвел',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
                    }
    a = cardGetter(r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\db_nom Самвел.txt', b)
    a.getListVendorCode()
    a.getNom()

    print("--- %s seconds ---" % (time.time() - start_time))