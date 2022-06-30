from Class.CardBodyClass import CardCase, Nomenclature
import sys
from os.path import join as joinPath
sys.path.insert(1, joinPath(sys.path[0], '../..'))
from my_mod.my_lib import read_xlsx
import requests
import uuid


class WBnomenclaturesCreater:
    def __init__(self):
        self.tokenAb = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'   
        self.tokenKar = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
        self.tokenSam = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
        self.mainUrl = 'https://suppliers-api.wildberries.ru/card/batchCreate'
        self.pathToFileForUpload = ''

    def createNomenclatures(self, mode, barcodeList):
        if mode =='Караханян':
            Token = self.tokenKar
        elif mode =='Абраамян':
            Token = self.tokenAb
        elif mode =='Самвел':
            Token = self.tokenSam
        if self.pathToFileForUpload =='':
            print('Путь к файлу не указан')
            return 0
        data = read_xlsx(self.pathToFileForUpload)
        tmpListCard = {}
        for line in data:
            if line['Баркод'] not in barcodeList:
                nomenclature = Nomenclature(line['Артикул цвета'], line['Баркод'], line['Розничная цена'], line['Путь к файлу'])

                if line['Артикул поставщика'] in tmpListCard.keys():
                    id = tmpListCard[line['Артикул поставщика']].id
                    nomenclature.SetUUID(id)
                    tmpListCard[line['Артикул поставщика']].AddNomenklatures(nomenclature.GetStruct())
                else:
                    id = str(uuid.uuid4())
                    card = CardCase(id)
                    card.SetAddin(line)
                    card.SetStruct()
                    nomenclature.SetUUID(id)
                    card.AddNomenklatures(nomenclature.GetStruct())
                    tmpListCard.update({line['Артикул поставщика']:card})
        countTry = 0
        for item in tmpListCard.values():
            countTry = 0
            while countTry <100:
                datajson = item.GetStruct()
                datajson
                response = requests.post(url=self.mainUrl, headers={
                            'Authorization': '{}'.format(Token)}, json=datajson)
                if response.status_code != 200:
                    print('Ошибка ВБ попытка {}'.format(str(countTry)))
                    continue
                else:
                    print('Номенклатура создана, код {}, текст ответа {}'.format(str(response.status_code), response.text))
                    break
