import requests
import pandas
import multiprocessing
from ClassExterminator import exterminator

class getterFBO():
    def __init__(self) -> None:
        self.urlGetStocksFNO = 'https://statistics-api.wildberries.ru/api/v1/supplier/stocks'
        self.tokensInfo = [
            {
                'IPName': 'Караханян',
                'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w',
                'tokenStat': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImU1ZGNjYWE2LWVjZDUtNDAzZC04MDA4LWRiNDZiYWJlYzBmYiJ9.7frmMigIpFCPJnpd8jopqeew1PKC4KhWpDIGSxE81Zs',
                'pathToDB': r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_nom Караханян.txt',
                'warehouse':'10237'
            },
            {
                'IPName': 'Самвел',
                'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y',
                'tokenStat': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjZjM2Y5MmM0LWQyMDgtNDMwZi04M2RhLWI2ODhjNzVhNWNlMSJ9.AOGxlP2tH7_SvUA0zOQCDRCP6uWd4pUlk9j7pncTqtQ',
                'pathToDB': r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_nom Самвел.txt',
                'warehouse':'278784'
            },
            
            {
                'IPName': 'Манвел',
                'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM',
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
        self.keys = ['imtID', 'nmID', 'techSize', 'chrtID', 'price', 'skus', 'Предмет']

    def getStocks(self, data):
        for key in self.keys:
            if key in data.columns:
                continue
            else:
                ext = exterminator()
                data = ext.getDataFromWB(data)
                break
        procList = []
        for seller in data['ИП'].unique().tolist():
            dataSeller = data[data['ИП'] == seller]
            for info in self.tokensInfo:
                if info['IPName'] == seller:
                    token = info['tokenStat']
                    break
            p = multiprocessing.Process(target=self.getStocksSeller, args=(dataSeller,token, ), daemon=False)
            p.start()
            procList.append(p)
        for p in procList:
            p.join()
            p.terminate()


    def getStocksSeller(self,dataSeller,token):
        headersRequest = {'Authorization': '{}'.format(token)}
        timeout = 10
        while timeout <60:
            try:
                r = requests.get(url=self.urlGetStocksFNO, headers=headersRequest, params={'dateFrom':'2019-06-20'}, timeout=timeout)
                if r.status_code == 200:
                    data = r.json()
                    dataNew = pandas.merge(dataSeller, pandas.DataFrame(data), how='left', left_on='vendorCode', right_on='supplierArticle')
                    dataNew.to_excel(r'E:\\stocks.xlsx', index=False)
                    break
                    # return pandas.DataFrame(dataNew)
            except requests.exceptions.ReadTimeout:
                r = requests.get(url=self.urlGetStocksFNO, headers=headersRequest, params={'dateFrom':'2019-06-20'}, timeout=timeout)
                timeout+=10
                continue
            except requests.exceptions.ConnectionError:
                r = requests.get(url=self.urlGetStocksFNO, headers=headersRequest, params={'dateFrom':'2019-06-20'}, timeout=timeout)
                timeout+=10
                continue
        
        



if __name__ == '__main__':
    a = getterFBO()
    a.start('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjZjM2Y5MmM0LWQyMDgtNDMwZi04M2RhLWI2ODhjNzVhNWNlMSJ9.AOGxlP2tH7_SvUA0zOQCDRCP6uWd4pUlk9j7pncTqtQ')

