import requests
import multiprocessing
import sys
import pandas
import time
import os
sys.path.append(r'D:\Python\WB\NEW_API')
from getNomenclatures.ClassGetNomenclatures import cardGetter


class exterminator():
    def __init__(self) -> None:
        self.urlExtChar = 'https://suppliers-api.wildberries.ru/content/v1/cards/update'
        self.urlExtImage = 'https://suppliers-api.wildberries.ru/content/v1/media/save'
        self.tokens = [
            {
                'IPName': 'Караханян',
                'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w',
                'pathToDB': r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_nom Караханян.txt'
            },
            {
                'IPName': 'Самвел',
                'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y',
                'pathToDB': r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_nom Самвел.txt'
            },
            
            {
                'IPName': 'Манвел',
                'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM',
                'pathToDB': r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_nom Манвел.txt'
            } ,
            
            {
                'IPName': 'Федоров',
                'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImIxYjQ3YjQzLTFhMTYtNGQ0Ni1iZTA1LWRlY2ExZTcxMTU0MSJ9.qTIJF6fEgbRux3Ps30ciMQ802UWqtAER-y94ALvE3PI',
                'pathToDB': r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_nom Федоров.txt'
            }             
        ]
        # self.tokenKar = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
        # self.tokenAbr = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'   
        # self.tokenSam = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
        # self.tokenFed = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImIxYjQ3YjQzLTFhMTYtNGQ0Ni1iZTA1LWRlY2ExZTcxMTU0MSJ9.qTIJF6fEgbRux3Ps30ciMQ802UWqtAER-y94ALvE3PI'
        self.keys = ['imtID', 'nmID', 'techSize', 'chrtID', 'price', 'skus', 'Предмет']

    
    def startExtChar(self, data):
        p1 = multiprocessing.Process(target=self.extChar, args=(data,), daemon=False)
        p1.start()
        p1.join()

    def startExtImage(self, data):
        p2 = multiprocessing.Process(target=self.extImage, args=(data,), daemon=False)
        p2.start()
        p2.join()
    
    def startDeletStoks(self, data, dataPath):
        p3 = multiprocessing.Process(target=self.deletStoks, args=(data,dataPath, ), daemon=False)
        p3.start()
        p3.join()


    def extChar(self, data):
        for key in self.keys:
                if key in data.columns:
                    continue
                else:
                    data = self.getDataFromWB(data)
                    break
        procList = []
        for seller in data['ИП'].unique().tolist():
            dataSeller = data[data['ИП'] == seller].to_dict('records')
            for token in self.tokens:
                if token['IPName'] == seller:
                    token = token['token']
                    break
            p = multiprocessing.Process(target=self.extCharProcess, args=(dataSeller,token, ), daemon=False)
            p.start()
            procList.append(p)
        for p in procList:
            p.join()


    def extCharProcess(self, data, token):
        headersRequest = {'Authorization': '{}'.format(token)}
        jsonDataFull = []
        for line in data:
            jsonDataFull.append({
                            "imtID": int(line['imtID']),
                            "nmID": int(line['nmID']),
                            "vendorCode": line['vendorCode'],
                            "sizes": [
                            {
                                "techSize": str(line['techSize']),
                                "chrtID": int(line['chrtID']),
                                "price": int(line['price']),
                                "skus": self.mkList(line['skus'])
                            }
                            ],
                            "characteristics": [
                            {"Предмет": line['Предмет']},
                            {'Описание': 'Товар'},
                            {'Высота упаковки': 19},
                            {'Ширина упаковки': 12},
                            {'Длина упаковки': 2}
                            ]
                        })
            if len(jsonDataFull) > 10:
                timeout = 10
                while timeout < 60:
                    try:
                        responce = requests.post(url=self.urlExtChar, json=jsonDataFull, headers=headersRequest, timeout=timeout)
                        if responce.status_code == 200:
                            jsonDataFull=[]
                            break
                        else:
                            timeout+=10
                            continue
                    except:
                        timeout+=10
                        continue
        timeout = 10
        while timeout < 60:
            try:
                responce = requests.post(url=self.urlExtChar, json=jsonDataFull, headers=headersRequest, timeout=timeout)
                if responce.status_code == 200:
                    jsonDataFull=[]
                    break
                else:
                    timeout+=10
                    continue
            except:
                timeout+=10
                continue


            # responce


    def extImage(self, data):
        for key in self.keys:
                if key in data.columns:
                    continue
                else:
                    data = self.getDataFromWB(data)
                    break
        procList = []
        for seller in data['ИП'].unique().tolist():
            dataSeller = data[data['ИП'] == seller].to_dict('records')
            for token in self.tokens:
                if token['IPName'] == seller:
                    token = token['token']
                    break
            p = multiprocessing.Process(target=self.extImageProcess, args=(dataSeller,token, ), daemon=False)
            p.start()
            procList.append(p)
        for p in procList:
            p.join()


    def extImageProcess(self, data, token):
        for line in data:
            jsonRequest = {
                "vendorCode": line['vendorCode'],
                "data": ['http://95.78.233.163:8001/wp-content/uploads/1.jpg']
                }
            headersRequest = {'Authorization': '{}'.format(token)}
            try:
                r = requests.post(self.urlExtImage, json=jsonRequest, headers=headersRequest, timeout=2)  
                r
            except requests.ConnectionError:
                r = requests.post(self.urlExtImage, json=jsonRequest, headers=headersRequest, timeout=5) 
            except requests.exceptions.ReadTimeout:
                r = requests.post(self.urlExtImage, json=jsonRequest, headers=headersRequest, timeout=5) 
        

    def deletStoks(self,data, dataPath):
        dfForStoks = pandas.DataFrame(columns=['Баркод'])
        dfForStoks['Баркод'] = data['sku']
        dfForStoks.insert(1, 'Группа', "Чехол производство (принт)")
        dfForStoks.insert(2, 'Основная характеристика', "(Принт 0)")
        dfForStoks.insert(3, 'Название 1С', "Хранилище ШК")
        dfForStoks.insert(4, 'Название полное', "Хранилище ШК")
        dfForStoks.insert(5, 'Размер печать', "")
        dfForStoks.to_excel(os.path.join(dataPath, 'stoks.xlsx'), index=False)



    def getDataFromWB(self, data):
        dataFull = pandas.DataFrame()
        if 'ИП' in data:
            for token in self.tokens:
                dataSeller = data[data['ИП'] == token['IPName']]
                if dataSeller.size !=0:
                    getter = cardGetter(token) 
                    getter.setListVendorCodeToGet(dataSeller['vendorCode'].unique().tolist())
                    dataFull = pandas.concat([dataFull, getter.returnNom()])
        else:
            for token in self.tokens:
                getter = cardGetter(token) 
                getter.setListVendorCodeToGet(data['vendorCode'].unique().tolist())
                dataFull = pandas.concat([dataFull, getter.returnNom()])
        return dataFull


    def mkList(self, string):
        if type(string) == str:
            string = string.replace('[','').replace(']','').replace("'",'').split(',')
            for i, j in enumerate(string):
                string[i] = j.strip()
            return string
        else:
            return string