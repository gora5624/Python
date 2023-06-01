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
        self.urlDetelStokcs = 'https://suppliers-api.wildberries.ru/api/v3/stocks/{}'
        self.tokensInfo = [
            {
                'IPName': 'Караханян',
                'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjgxYjczNGVmLWI2OWUtNGRhMi1iNTBiLThkMTEyYWM4MjhkMCJ9.pU1YOOirgRe3Om-WRYT61AofToggCLbV3na7GbXKGqU',
                'tokenStat': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImU1ZGNjYWE2LWVjZDUtNDAzZC04MDA4LWRiNDZiYWJlYzBmYiJ9.7frmMigIpFCPJnpd8jopqeew1PKC4KhWpDIGSxE81Zs',
                'pathToDB': r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_nom Караханян.txt',
                'warehouse':'10237'
            },
            {
                'IPName': 'Самвел',
                'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImUxNGFmM2UxLTc0YTctNDlkOC1hNGIyLTI1Y2Q4ZDc2YmM4NSJ9.bCTyIoPVS3wpbzy7TdK-Gt8Sgz3iyPamzJjnA_EH3Iw',
                'tokenStat': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjZjM2Y5MmM0LWQyMDgtNDMwZi04M2RhLWI2ODhjNzVhNWNlMSJ9.AOGxlP2tH7_SvUA0zOQCDRCP6uWd4pUlk9j7pncTqtQ',
                'pathToDB': r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_nom Самвел.txt',
                'warehouse':'278784'
            },
            
            {
                'IPName': 'Манвел',
                'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjNhZmUzMzMzLWFmYjEtNDI5Yi1hN2Q1LTE1Yjc4ODg4MmU5MSJ9.kWUDkHkGrtD8WxE9sQHto5B7L3bQh-XRDf7EeZQiw7A',
                'tokenStat': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImIwZDJlZTA4LTM3ZDEtNDViZC1iNTY2LWMwOTE4NjNjNjk1NyJ9.tseNJFDf2vf1PQ6YlkPaic_f-f1lolmXmr7-TG1HSRM',
                'pathToDB': r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_nom Манвел.txt',
                'warehouse':'141069'
            } ,
            
            {
                'IPName': 'Федоров',
                'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImIxYjQ3YjQzLTFhMTYtNGQ0Ni1iZTA1LWRlY2ExZTcxMTU0MSJ9.qTIJF6fEgbRux3Ps30ciMQ802UWqtAER-y94ALvE3PI',
                'tokenStat': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImNhODU0ZTllLTM2MzYtNDFjNS1hODczLWNlYWYzNTI3NzYzZCJ9.i7XVHJm5goeXyBF-c4hc_YUg9pYL3nxu1Y6ZUliZ61I',
                'pathToDB': r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_nom Федоров.txt',
                'warehouse':'652361'
            }             
        ]
        # self.tokenKar = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
        # self.tokenAbr = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'   
        # self.tokenSam = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
        # self.tokenFed = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImIxYjQ3YjQzLTFhMTYtNGQ0Ni1iZTA1LWRlY2ExZTcxMTU0MSJ9.qTIJF6fEgbRux3Ps30ciMQ802UWqtAER-y94ALvE3PI'
        self.keys = ['imtID', 'nmID', 'techSize', 'chrtID', 'price', 'skus', 'Предмет']

    
    def startExtChar(self, data):
        p1 = multiprocessing.Process(target=self.extChar, args=(data,), daemon=False)
        # p2 = multiprocessing.Process(target=self.extImage, args=(data,), daemon=False)
        p1.start()
        # p2.start()
        # p2.join()
        p1.join()
        p1.terminate()
        # p2.terminate()

    def startExtImage(self, data):
        while True:
            p2 = multiprocessing.Process(target=self.extImage, args=(data,), daemon=False)
            p2.start()
            p2.join()
            p2.terminate()
    
    def generateBarcodesFileFor1CBtn(self, data, dataPath):
        p3 = multiprocessing.Process(target=self.generateBarcodesFileFor1C, args=(data,dataPath, ), daemon=False)
        p3.start()
        p3.join()
        p3.terminate()

    def startDeletStoks(self, data):
        p4 = multiprocessing.Process(target=self.deleteStocks, args=(data, ), daemon=False)
        p4.start()
        p4.join()
        p4.terminate()


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
            for info in self.tokensInfo:
                if info['IPName'] == seller:
                    token = info['token']
                    break
            p = multiprocessing.Process(target=self.extCharProcess, args=(dataSeller,token, ), daemon=False)
            p.start()
            procList.append(p)
        for p in procList:
            p.join()
            p.terminate()


    def extCharProcess(self, data, token):
        headersRequest = {'Authorization': '{}'.format(token)}
        jsonDataFull = []
        doneDataList = []
        listVendorCodeDone = [i.replace('\n','') for i in open(r'D:\Python\WB\NEW_API\managmentFBS\done.txt', 'r', encoding='utf-8').readlines()]
        for line in data:
            if line['vendorCode'] not in doneDataList:
                doneDataList.append(line['vendorCode'])
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
                                {"Бренд": 'Mobi115'},
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
                                with open(r'D:\Python\WB\NEW_API\managmentFBS\done.txt', 'a', encoding='utf-8') as fileDone:
                                    fileDone.writelines([i+'\n' for i in doneDataList])
                                    doneDataList = []
                                    fileDone.close()
                                time.sleep(1)
                                break
                            else:
                                if 'Указанные Артикулы товара находятся в корзине' in responce.text:
                                    jsonDataFull=[]
                                    break
                                if 'артикулы wb' in responce.text.lower():
                                    try:
                                        dataErrors = [i.strip() for i in responce.json()['additionalErrors']['Неверные артикулы WB'].split(',')]
                                        with open(r'D:\Python\WB\NEW_API\managmentFBS\errors.txt', 'a', encoding='utf-8') as fileErrors:
                                            fileErrors.writelines([i+'\n' for i in dataErrors])
                                            fileErrors.close()
                                        i = 0
                                        while True and (i <500):
                                            i +=1
                                            for j,line in enumerate(jsonDataFull):
                                                if str(line['nmID']) in dataErrors:
                                                    jsonDataFull.pop(j)
                                                    break
                                                else:
                                                    continue
                                            if j >= len(jsonDataFull)-1:
                                                break
                                    except:
                                        with open(r'D:\Python\WB\NEW_API\managmentFBS\errors.txt', 'a', encoding='utf-8') as fileErrors:
                                            fileErrors.writelines('***' + responce.text + '***' + '\n')
                                            fileErrors.close()
                                    timeout+=10
                                    continue
                                timeout+=10
                                time.sleep(1)
                                continue
                        except:
                            timeout+=10
                            time.sleep(1)
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
            for info in self.tokensInfo:
                if info['IPName'] == seller:
                    token = info['token']
                    break
            p = multiprocessing.Process(target=self.extImageProcess, args=(dataSeller,token, ), daemon=False)
            p.start()
            procList.append(p)
        for p in procList:
            p.join()
            p.terminate()


    def extImageProcess(self, data, token):
        list_ = [i.replace('\n','') for i in open(r'D:\Python\WB\NEW_API\managmentFBS\doneImg.txt', 'r', encoding='utf-8').readlines()]
        for line in data:
            if line['vendorCode'] not in list_:
                jsonRequest = {
                    "vendorCode": line['vendorCode'],
                    "data": ['http://95.78.233.163:8001/wp-content/uploads/1.jpg']
                    }
                headersRequest = {'Authorization': '{}'.format(token)}
                try:
                    r = requests.post(self.urlExtImage, json=jsonRequest, headers=headersRequest, timeout=2)  
                    time.sleep(0.6)
                    if 'Неверный запрос' in r.text:
                        with open(r'D:\Python\WB\NEW_API\managmentFBS\doneImg.txt', 'a', encoding='utf-8') as fileDone:
                            fileDone.writelines(line['vendorCode'] + '\n')
                            fileDone.close()
                        print(r.text)
                    if r.status_code == 200:
                        with open(r'D:\Python\WB\NEW_API\managmentFBS\doneImg.txt', 'a', encoding='utf-8') as fileDone:
                            fileDone.writelines(line['vendorCode'] + '\n')
                            fileDone.close()
                    print(r.text)
                except requests.exceptions.ConnectTimeout:
                    r = requests.post(self.urlExtImage, json=jsonRequest, headers=headersRequest, timeout=10) 
                    if r.status_code == 200:
                        with open(r'D:\Python\WB\NEW_API\managmentFBS\doneImg.txt', 'a', encoding='utf-8') as fileDone:
                            fileDone.writelines(line['vendorCode'] + '\n')               
                            fileDone.close()
                    time.sleep(0.7)
                except requests.exceptions.ReadTimeout:
                    r = requests.post(self.urlExtImage, json=jsonRequest, headers=headersRequest, timeout=10) 
                    if r.status_code == 200:
                        with open(r'D:\Python\WB\NEW_API\managmentFBS\doneImg.txt', 'a', encoding='utf-8') as fileDone:
                            fileDone.writelines(line['vendorCode'] + '\n')               
                            fileDone.close()
                    time.sleep(0.7)
                except requests.ConnectionError:
                    r = requests.post(self.urlExtImage, json=jsonRequest, headers=headersRequest, timeout=10) 
                    if r.status_code == 200:
                        with open(r'D:\Python\WB\NEW_API\managmentFBS\doneImg.txt', 'a', encoding='utf-8') as fileDone:
                            fileDone.writelines(line['vendorCode'] + '\n')
                            fileDone.close()
                    time.sleep(0.7)


                except:
                    r = requests.post(self.urlExtImage, json=jsonRequest, headers=headersRequest, timeout=30) 
                    if r.status_code == 200:
                        with open(r'D:\Python\WB\NEW_API\managmentFBS\doneImg.txt', 'a', encoding='utf-8') as fileDone:
                            fileDone.writelines(line['vendorCode'] + '\n')                 
                            fileDone.close()
                    time.sleep(0.7)

        

    def deleteStocks(self, data):
        for key in self.keys:
            if key in data.columns:
                continue
            else:
                data = self.getDataFromWB(data)
                break
        procList = []
        for seller in data['ИП'].unique().tolist():
            dataSeller = data[data['ИП'] == seller]
            dataSeller['sku'] = dataSeller['sku'].apply(int)
            dataSeller['sku'] = dataSeller['sku'].apply(str)
            barcodeList = dataSeller['sku'].values.tolist()
            for info in self.tokensInfo:
                if info['IPName'] == seller:
                    token = info['token']
                    wh = info['warehouse']
                    break
            p = multiprocessing.Process(target=self.deleteStocksProcess, args=(barcodeList,token, wh,), daemon=False)
            p.start()
            procList.append(p)
        for p in procList:
            p.join()
            p.terminate()


    def deleteStocksProcess(self, data, token, wh):
        step = 1000
        for i in range(0,len(data),step):
            jsonRequest = {
                            "skus": data[i:i+step]
                            }
            headersRequest = {'Authorization': '{}'.format(token)}
            countTry =0
            while True and countTry <5:
                try:
                    countTry+=1
                    r = requests.delete(self.urlDetelStokcs.format(wh), json=jsonRequest, headers=headersRequest, timeout=15)  
                    if r.status_code == 404:
                        try:
                            d = r.json()
                            for barcode in d['data']:
                                jsonRequest['skus'].remove(barcode)
                            jsonRequest
                            countTry+=1
                            if len(jsonRequest['skus'])>0:
                                continue
                            else:
                                break
                        except:
                            pass
                    elif r.status_code == 204:
                        break
                    r
                except requests.ConnectionError:
                    r = requests.delete(self.urlExtImage, json=jsonRequest, headers=headersRequest, timeout=60) 
                    countTry+=1
                    break
                except requests.exceptions.ReadTimeout:
                    r = requests.delete(self.urlExtImage, json=jsonRequest, headers=headersRequest, timeout=60) 
                    countTry+=1
                    break



    def generateBarcodesFileFor1C(self,data, dataPath):
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
            for info in self.tokensInfo:
                dataSeller = data[data['ИП'] == info['IPName']]
                if dataSeller.size !=0:
                    getter = cardGetter(info) 
                    getter.listVendorCodeDone = [i.replace('\n','') for i in open(r'D:\Python\WB\NEW_API\managmentFBS\done.txt', 'r', encoding='utf-8').readlines()]
                    if 'vendorCode' in data:
                        getter.setListVendorCodeToGet(dataSeller['vendorCode'].unique().tolist())
                    elif 'Артикул товара' in data:
                        getter.setListVendorCodeToGet(dataSeller['Артикул товара'].unique().tolist())
                    dataFull = pandas.concat([dataFull, getter.returnNom()])
        else:
            for info in self.tokensInfo:
                getter = cardGetter(info) 
                if 'vendorCode' in data:
                    getter.setListVendorCodeToGet(data['vendorCode'].unique().tolist())
                elif 'Артикул товара' in data:
                    getter.setListVendorCodeToGet(data['Артикул товара'].unique().tolist())
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