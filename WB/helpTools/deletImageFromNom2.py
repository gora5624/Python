import requests
import pandas
import multiprocessing
import time
import json
# -*- coding: utf-8 -*-


class ImageDeleter():
    def __init__(self,pathToNomenclaturesIdList) -> None:
        self.nomenclaturesIdList = pandas.DataFrame(pandas.read_excel(pathToNomenclaturesIdList)).to_dict('list')['Артикул']
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

    def main(self):
        pool = multiprocessing.Pool()
        for id in self.nomenclaturesIdList:
            pool.apply_async(self.deletPhoto, args=(id,))
        pool.close()
        pool.join()


    def deletPhoto(self, id):
        (vendorCode, token) = self.findVendorCode(id)
        if (vendorCode, token) != (0,0):
            self.pushPhoto(vendorCode, token)


    def findVendorCode(self, id):
        jsonRequest = {
                "sort": {
                    "cursor": {
                    "limit": 1000
                    },
                    "filter": {
                    "textSearch": str(id),
                    "withPhoto": -1
                    },
                    "sort": {
                    "sortColumn": "updateAt",
                    "ascending": False
                    }
                }
                }
        requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/cards/cursor/list'
        for token in self.tokens:       
            headersRequest = {'Authorization': '{}'.format(token['token'])}
            try:
                r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest, timeout=5)  
                # print(r.text)
            except requests.ConnectionError:
                r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest, timeout=5) 
                print(r.text)
            except:
                r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest, timeout=5) 
                print(r.text)
            pass
            if  r.status_code == 200:
                if len(data:=r.json()['data']['cards'] ) != 0:
                    return (data[0]['vendorCode'], token['token'])
        return (0 , 0)
                    # self.pushPhoto(data['cards'][0]['vendorCode'], token['token'])
                    # break



    def pushPhoto(self, vendorCode, token):
        requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/media/save'
        jsonRequest = {
            "vendorCode": vendorCode,
            "data": ['']
            }
        headersRequest = {'Authorization': '{}'.format(token)}
        try:
            r = requests.post(requestUrl, data=json.dumps(jsonRequest, ensure_ascii=False).encode('utf-8'), headers=headersRequest, timeout= 1)  
            print(r.text)
        except requests.ConnectionError:
            r = requests.post(requestUrl, data=json.dumps(jsonRequest, ensure_ascii=False).encode('utf-8'), headers=headersRequest, timeout=5) 
            print(r.text)
        except:
            r = requests.post(requestUrl, data=json.dumps(jsonRequest, ensure_ascii=False).encode('utf-8'), headers=headersRequest, timeout=5) 
            print(r.text)

if __name__ =='__main__':
    imageDeleter = ImageDeleter(r'E:\удалить права.xlsx')
    imageDeleter.main()