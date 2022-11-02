import requests
import pandas
import multiprocessing
import os
import json
# -*- coding: utf-8 -*-


class ImageDeleter():
    def __init__(self,pathToPrintList ,pathToDB = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\ШК.txt') -> None:
        self.printList = pandas.DataFrame(pandas.read_excel(pathToPrintList)).to_dict('list')['Принты']
        self.db = pandas.DataFrame(pandas.read_table(pathToDB)).to_dict('records')
        self.barcodesList = []
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
        # self.vendorCodeManager = multiprocessing.Manager()
        # self.vendorCodelist = pandas.DataFrame(pandas.read_table(r'E:\\tmp.csv',sep=';')).to_dict('records')
        self.timeout = 2
        self.findBarcodesList()
        self.findVedorCodesForAllIP()
        a = pandas.DataFrame(self.vendorCodelist)
        a.to_excel(r'E:\\tmp.xlsx')
        self.deletPhoto()


    def findBarcodesList(self):
        for nomenclature in self.db:
            if nomenclature['Характеристика'] in self.printList:
                self.barcodesList.append(nomenclature['Штрихкод'])

            
    def findVedorCodesForAllIP(self):
        pool = multiprocessing.Pool()
        with multiprocessing.Manager() as manager:
            vendorCodelistTMP = manager.list()
            #processes = []
            for iP in self.tokens:
                # p = multiprocessing.Process(target=self.findVendorCodesForOneIP, args=(iP['token'],vendorCodelistTMP,))
                # p.start()
                # processes.append(p)
                pool.apply_async(self.findVendorCodesForOneIP, args=(iP['token'],vendorCodelistTMP,self.barcodesList))
            # for p in processes:
                # p.join()
            pool.close()
            pool.join()   
            self.vendorCodelist = list(vendorCodelistTMP)

        # pool.close()
        # pool.join()
        # pool = multiprocessing.Pool()
        # with multiprocessing.Manager() as manager:
        #     vendorCodelistTMP = manager.list()
        #     for iP in self.tokens:
        #         self.findVendorCodesForOneIP(iP['token'],vendorCodelistTMP, self.barcodesList)
        # pool.close()
        # pool.join()
            


    def findVendorCodesForOneIP(self, token, vendorCodelistTMP, barcodesList):
            url = 'https://suppliers-api.wildberries.ru/content/v1/cards/cursor/list'
            headersRequest = {'Authorization': '{}'.format(token)}
            # pool = multiprocessing.Pool()
            for barcode in barcodesList:
                # pool.apply_async(self.requestsVendorCode, args=(barcode, headersRequest, url, vendorCodelistTMP, token))
                self.requestsVendorCode(barcode, headersRequest, url, vendorCodelistTMP, token)
            # pool.close()
            # pool.join()
        

    def requestsVendorCode(self, barcode, headersRequest, url, vendorCodelistTMP, token):        
                json = {
                "sort": {
                    "cursor": {
                    "limit": 1000
                    },
                    "filter": {
                    "textSearch": str(barcode),
                    "withPhoto": -1
                    },
                    "sort": {
                    "sortColumn": "updateAt",
                    "ascending": False
                    }
                }
                }
                countTry = 0
                while countTry < 5:
                    try:
                        response = requests.post(url=url, headers=headersRequest, json=json, timeout=self.timeout)
                        if response.status_code == 200:
                            if len(response.json()['data']['cards']) !=0:
                                vendorCodelistTMP.append({'vendorCode': response.json()['data']['cards'][0]['vendorCode'], 'token': token})
                                a = list(vendorCodelistTMP)
                                break
                            else:
                                break
                        else:
                            countTry +=1
                            continue
                    except requests.ReadTimeout:
                        countTry +=1
                        continue
                    except requests.ConnectTimeout:
                        countTry +=1
                        continue
                    except:
                        countTry +=1
                        continue
    

    def deletPhoto(self):
        pool = multiprocessing.Pool()
        for vendorCode in self.vendorCodelist:
            pool.apply_async(self.pushPhoto, args=(vendorCode,))
        pool.close()
        pool.join()


    def pushPhoto(self, line):
        requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/media/save'
        jsonRequest = {
            "vendorCode": line['vendorCode'],
            "data": ['']
            }
        headersRequest = {'Authorization': '{}'.format(line['token']), 'X-Vendor-Code': line['vendorCode']}
        try:
            r = requests.post(requestUrl, data=json.dumps(jsonRequest, ensure_ascii=False).encode('utf-8'), headers=headersRequest)  
            print(r.text)
        except requests.ConnectionError:
            r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest) 
            print(r.text)

if __name__ =='__main__':
    imageDeleter = ImageDeleter(r'E:\Downloads\Принты Наруто.xlsx')