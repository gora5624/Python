import requests
import time
import pandas

class nomenclatures():
    def __init__(self) -> None:
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
        self.pathToFileWithNom = 'E:\\nomenclatures.xlsx'
        self.dataNomenclatures = []


    # получить список всех номенклатур по всем ИП
    def getListNomenclatures(self):
        getListNomenclaturesRequestUrl = 'https://suppliers-api.wildberries.ru/content/v1/cards/list'
        dataNomenclatures = []
        for token in self.tokens:
            headersRequest = {'Authorization': '{}'.format(token['token'])}
            countSkip = 0
            while True:
                jsonRequest = {
                                "sort": {
                                    "limit": 1000,
                                    "offset": countSkip,
                                    "searchValue": "",
                                    "sortColumn": "",
                                    "ascending": False
                                }
                                }
                countTry = 0
                while countTry <10:
                    try:
                        responce = requests.post(getListNomenclaturesRequestUrl, json=jsonRequest, headers=headersRequest)
                        break
                    except ConnectionError:
                        time.sleep(2)
                        countTry +=1
                        continue
                if responce.status_code == 200:
                    responceJson = responce.json()
                    if responceJson['error']:
                        print(responceJson['errorText'])
                        print(responceJson['additionalErrors'])
                    else:
                        if len(responceJson['data']['cards']) < 1000:
                            dataNomenclatures.extend(responceJson['data']['cards'])
                            break
                        else:
                            dataNomenclatures.extend(responceJson['data']['cards'])
                            countSkip +=1000
        if __name__ == '__main__':
            df = pandas.DataFrame(dataNomenclatures)
            df.to_excel(self.pathToFileWithNom, index=False)
            self.dataNomenclatures = dataNomenclatures
        else:
            self.dataNomenclatures = dataNomenclatures


    
    def getListCharacteristics(self):
        pass


if __name__ == '__main__':
    nom = nomenclatures()
    nom.getListNomenclatures()