import sys
from os.path import join as joinPath, basename
sys.path.insert(1, joinPath(sys.path[0], '../..'))
import requests
import pandas
import copy
import time
import pickle
import aiohttp
from aiohttp import ClientConnectorError
import subprocess
from Class.priceModif import priceMod


class ExistsNomenclaturesCreater:    
    def __init__(self, data, mode, pathToFileForUpload):
        # self.tokenAb = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM5NjgxZDkxLWVmYzctNGVjOC05NzIzLTgyN2JkZTY2NWFkYyJ9.j4gqyXEe0Guzr_CbKNmFRxf_zyqjjyJ6dODc4oQII2E'   
        # self.tokenIvan = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImUyZTIyZGE1LTYxYWYtNDgyMi1hMDVkLTZiNzVlMTBiNzlmMiJ9.yDq9XasZjs-oB1PapNbD_NWIH8tgWEz_WyKLvVTNgBs'
        # self.tokenKar = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImU4NjQ1YWI5LWFjM2UtNGFkOS1hYmIyLThkMTMzMGM1YTU3NyJ9.8nz9gIHurlCVKIhruG6hY8MRBtMLvLYggVzisxgKivY'
        # self.tokenSam = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImQ3ZTJkN2I4LWVjZDEtNDNiNC04ODkxLTg2ZWZhNDA0ODI0YyJ9.6qCa4264GF5uv76laTgfnvKD7RXyBLDOk8U_cHPoDDU'
        self.urlGetCards = 'https://suppliers-api.wildberries.ru/content/v1/cards/filter'
        self.urlUpdateCards = 'https://suppliers-api.wildberries.ru/content/v2/cards/update'
        self.pathTo1CNom = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\Список стандартный поиск номенклатура.txt'
        self.data = data # pandas.DataFrame(pandas.read_excel(self.pathToFileForUpload))
        self.vendorCodesAndBarcodes = pandas.DataFrame()
        self.dataDict = data.to_dict('records')
        self.listVendorCodeToGet = self.data['Артикул товара'].values.tolist()
        self.pathToFileForUpload = pathToFileForUpload
        self.modelForUploads = []
        self.listDoneVendorCode = []
        self.alredyGetVendorCode = []
        self.listCardToChange = []
        self.nmIdsList = []
        self.errorsList = []
        self.dataFromDB = pandas.DataFrame()
        if mode =='Караханян':
            self.DBpath = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Караханян.txt'
            self.token = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njg4MiwiaWQiOiI4YjEzZWUzOC03MGIxLTQ3ZjgtYTdlNC03OTIzY2Q2ZmQ3ZTciLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjEwMTA2MiwicyI6MTAsInNpZCI6IjNhOTNkZGMxLWFhNTctNWMyYi05YzVjLWRkZDIyMTg4OTQ0MCIsInVpZCI6NDUzMjI5MjB9.DXm6RuooUieyrnNdXr3FfPPdwK5uV4aiTF5SZIryJUhbQW4uScXQLEb-n8p0iM3RT6Js6aVKijiyOkawE6r76g'
        elif mode =='Абраамян':
            self.DBpath = r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Манвел.txt"
            self.token = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njk1MSwiaWQiOiIyMzUyZGFmYS05NTdhLTQ0MzAtYWFhMi1lZGM5NDZkZDY0ODEiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjUyNzczNiwicyI6MTAsInNpZCI6ImFhNDdlNDg5LTU5ZTAtNDIzMi1hMWJmLTBlMTIzOWYwNDJmMSIsInVpZCI6NDUzMjI5MjB9.j9s_VtDpTEWceEd1vUTWf6uofUuSY30q0UrR-H047qZE40sb8atwtAviABB7eoeLQdu3T69UosBdn_Bvj2-2ZQ'   
        elif mode =='Самвел':
            self.DBpath = r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Самвел2.txt"
            self.token = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njk3MiwiaWQiOiJjZWE4ZTNmYy1iYzg5LTRjYjktYmNmNy0xN2ZiNmNjNzk1MTQiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjgxOTI0NiwicyI6MTAsInNpZCI6IjBhYjhiMTA1LTA1MWYtNGVkNi04NzBiLTM5OWU3NWUxMDI4NiIsInVpZCI6NDUzMjI5MjB9.bOmPtl_ZXx-1C25-5CbftPJVQuuHzwG5iH9QUx0x8CdZCjI9ZnbFgMU1ijL-lfgn_N1JxPvojV2dBrKTpDnolw'
        elif mode =='Иван':
            self.DBpath = r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Федоров.txt"
            self.token = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5NzAwNywiaWQiOiI1ZWRjMWY0Ni04OWVhLTQxMzktYjVjYi1hNDM5OGUwMzUxNTMiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjExNzEwNDQsInMiOjEwLCJzaWQiOiJkOWU0OGUxZi05ZjgxLTQ1MmMtODRiYy05ZGYxZWRiMzNmNDkiLCJ1aWQiOjQ1MzIyOTIwfQ.y2sbT8zqvoM-iSxKJcsdiEphMoLRfNq8pBsIQnmGQIbc1btCIoe7Qkz65Ur91fVEqyDbQZ-Ry_1tTkgof5hKDw'
        self.headersGetCard = {'Authorization': '{}'.format(self.token)}
        self.countValueInField ={
                'Цвет': 1,
                'Вид застежки': 2,
                'Рисунок': 1,
                'Любимые герои': 1,
                'Декоративные элементы': 1,
                'Назначение подарка': 3,
                'Особенности чехла': 3,
                'Совместимость': 10,
                'Модель': 3,
                'Тип чехлов': 1,
                'Повод': 3,
                'Материал изделия': 3
            }


    def start(self):
        try:
            print("Начал делать " + self.pathToFileForUpload)
            self.getNomFromWB()
            self.changeCards()
            self.pushChanges()
            self.updateFileForUpload()
            self.AdFunc()
            self.splitNom()
            self.changePrice()
            try:
                if len(self.errorsList) != 0:
                    pandas.DataFrame(self.errorsList).to_excel(joinPath(r'E:\MyProduct\Python\WB\MakePrint',basename(self.pathToFileForUpload)), index=False)
            except:
                pass
            # self.createFileFor1C()
        except: print(self.pathToFileForUpload + ' БЫЛА ГДЕ ТО ОШИБКА')

    def AdFunc(self):

        listdf = pandas.DataFrame(self.listCardToChange)
        self.CategoryAndIDs = listdf.merge(self.data,how='left',left_on='vendorCode',right_on='Артикул товара')#.merge(pandas.read_excel(r"E:\MyProduct\Python\WB\MakePrint\категории.xlsx"),'left',left_on='Принт',right_on='Принт')
        self.CategoryAndIDs = self.CategoryAndIDs.merge(pandas.read_excel(r"E:\MyProduct\Python\WB\MakePrint\категории.xlsx"),'left',left_on='Принт',right_on='Принт')
        self.CategoryAndIDs = self.CategoryAndIDs.loc[:,['nmID_x','Категория_y']]
        test = self.CategoryAndIDs.groupby('Категория_y')
        self.CategoryAndIDsByGroup = [test.get_group(x) for x in test.groups]
        self.CategoryAndIDsByGroup
        test
        # dfWithPrintName = self.data.loc[self.data['Артикул товара'] == self.listVendorCodeToGet]
        # listdf



    def chekCountField(self, field, values):
            maxCount = self.countValueInField[field]
            return values.split(';')[0:maxCount]



    def changePrice(self):
        price = 999
        if 'fashion' in self.pathToFileForUpload.lower():
            discount = 35
        elif 'под карту' in self.pathToFileForUpload.lower():
            discount = 45
        elif 'newpoket' in self.pathToFileForUpload.lower():
            discount = 45
            # price = 999
        elif 'проз' in self.pathToFileForUpload.lower():
            discount = 50
            price = 1002
        elif 'мат' in self.pathToFileForUpload.lower():
            discount = 50
            price = 1002
        elif 'skinshell' in self.pathToFileForUpload.lower():
            discount = 50
            price = 1002


        pr = priceMod(self.nmIdsList ,self.token, price, discount)
        pr.pushPrice()
        # pr.pushDiscounts()

    
    def createFileFor1C(self):
        dataFor1C = []
        Nom1CData = pandas.DataFrame(pandas.read_table(self.pathTo1CNom, sep='\t'))
        nameFile = basename(self.pathToFileForUpload)
        nameCase = nameFile.replace('.xlsx', '')
        nameCaseFull = Nom1CData[Nom1CData['Наименование']==nameCase]['Наименование для печати'].values[0]
        size = Nom1CData[Nom1CData['Наименование']==nameCase]['Размер чехла'].values[0]
        if pandas.isnull(size) and 'книга' in nameCase:
                size = ''
        for line in self.dataDictNew:
            tmp = {
                'Баркод':line['Баркод товара'],
                'Группа':'Чехол производство (принт)',
                'Основная характеристика':line['Принт'],
                'Название 1С':nameCase,
                'Название полное':nameCaseFull,
                'Размер Печать':size
            }
            dataFor1C.append(tmp)
        df = pandas.DataFrame(dataFor1C)
        df.to_excel(self.pathToFileForUpload.replace(name:=basename(self.pathToFileForUpload),'1C_'+ name), index=False)


    def updateFileForUpload(self):
        self.vendorCodesAndBarcodes = self.vendorCodesAndBarcodes.set_index('Артикул товара')
        self.vendorCodesAndBarcodes = self.vendorCodesAndBarcodes.reindex(index=self.data['Артикул товара'])
        self.vendorCodesAndBarcodes = self.vendorCodesAndBarcodes.reset_index()
        self.data['Баркод товара'] = self.vendorCodesAndBarcodes['Баркоды']
        self.data['nmID'] = self.vendorCodesAndBarcodes['nmID']
        self.dataDict = self.data.to_dict('records')
        self.dataDictNew = []
        for i, line in enumerate(self.dataDict):
            if len(line['Баркод товара']) > 1:
                for barcode in line['Баркод товара']:
                    lineNew = copy.deepcopy(line)
                    tmp = {'Баркод товара':barcode, 'nmID':line['nmID']}
                    lineNew.update(tmp)
                    self.dataDictNew.append(lineNew)
            else:
                tmp = {'Баркод товара':''.join(line['Баркод товара']), 'nmID':line['nmID']}
                line.update(tmp)
                self.dataDictNew.append(line)
        df = pandas.DataFrame(self.dataDictNew)
        df.to_excel(self.pathToFileForUpload, index=False)

        # self.data['Баркод товара'] = 
        # for case in self.data:



    @staticmethod
    def uplaodImage(path, mode):
        if mode =='Караханян':
            token = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njg4MiwiaWQiOiI4YjEzZWUzOC03MGIxLTQ3ZjgtYTdlNC03OTIzY2Q2ZmQ3ZTciLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjEwMTA2MiwicyI6MTAsInNpZCI6IjNhOTNkZGMxLWFhNTctNWMyYi05YzVjLWRkZDIyMTg4OTQ0MCIsInVpZCI6NDUzMjI5MjB9.DXm6RuooUieyrnNdXr3FfPPdwK5uV4aiTF5SZIryJUhbQW4uScXQLEb-n8p0iM3RT6Js6aVKijiyOkawE6r76g'
           # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjgxYjczNGVmLWI2OWUtNGRhMi1iNTBiLThkMTEyYWM4MjhkMCJ9.pU1YOOirgRe3Om-WRYT61AofToggCLbV3na7GbXKGqU'
        elif mode =='Абраамян':
            token = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njk1MSwiaWQiOiIyMzUyZGFmYS05NTdhLTQ0MzAtYWFhMi1lZGM5NDZkZDY0ODEiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjUyNzczNiwicyI6MTAsInNpZCI6ImFhNDdlNDg5LTU5ZTAtNDIzMi1hMWJmLTBlMTIzOWYwNDJmMSIsInVpZCI6NDUzMjI5MjB9.j9s_VtDpTEWceEd1vUTWf6uofUuSY30q0UrR-H047qZE40sb8atwtAviABB7eoeLQdu3T69UosBdn_Bvj2-2ZQ'   
            # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjNhZmUzMzMzLWFmYjEtNDI5Yi1hN2Q1LTE1Yjc4ODg4MmU5MSJ9.kWUDkHkGrtD8WxE9sQHto5B7L3bQh-XRDf7EeZQiw7A'   
        elif mode =='Самвел':
            token = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njk3MiwiaWQiOiJjZWE4ZTNmYy1iYzg5LTRjYjktYmNmNy0xN2ZiNmNjNzk1MTQiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjgxOTI0NiwicyI6MTAsInNpZCI6IjBhYjhiMTA1LTA1MWYtNGVkNi04NzBiLTM5OWU3NWUxMDI4NiIsInVpZCI6NDUzMjI5MjB9.bOmPtl_ZXx-1C25-5CbftPJVQuuHzwG5iH9QUx0x8CdZCjI9ZnbFgMU1ijL-lfgn_N1JxPvojV2dBrKTpDnolw'
            # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImUxNGFmM2UxLTc0YTctNDlkOC1hNGIyLTI1Y2Q4ZDc2YmM4NSJ9.bCTyIoPVS3wpbzy7TdK-Gt8Sgz3iyPamzJjnA_EH3Iw'
        elif mode =='Иван':
            token = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5NzAwNywiaWQiOiI1ZWRjMWY0Ni04OWVhLTQxMzktYjVjYi1hNDM5OGUwMzUxNTMiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjExNzEwNDQsInMiOjEwLCJzaWQiOiJkOWU0OGUxZi05ZjgxLTQ1MmMtODRiYy05ZGYxZWRiMzNmNDkiLCJ1aWQiOjQ1MzIyOTIwfQ.y2sbT8zqvoM-iSxKJcsdiEphMoLRfNq8pBsIQnmGQIbc1btCIoe7Qkz65Ur91fVEqyDbQZ-Ry_1tTkgof5hKDw'
            # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImIxYjQ3YjQzLTFhMTYtNGQ0Ni1iZTA1LWRlY2ExZTcxMTU0MSJ9.qTIJF6fEgbRux3Ps30ciMQ802UWqtAER-y94ALvE3PI'
        args = [sys.executable, r'E:\MyProduct\Python\WB\MakePrint\Moduls\udatePhoto.py', path.replace(' ', '#'), token]
        subprocess.Popen(args, shell=True).wait()
        # args2 = [sys.executable, r'E:\MyProduct\Python\WB\MakePrint\Moduls\chekUdatePhoto.py', path.replace(' ', '#'), token]
        # subprocess.Popen(args2, shell=True)


    def getNomFromWBOld(self):
        for vendorCode in self.listVendorCodeToGet:
            if vendorCode not in self.alredyGetVendorCode:
                jsonRequestsGetCard = {
                                    "vendorCodes": [vendorCode]
                                    }
                timeout = 10              
                while timeout < 60:
                    try:
                        response = requests.post(self.urlGetCards, headers=self.headersGetCard, json=jsonRequestsGetCard, timeout=timeout)
                        if response.status_code ==200:
                            break
                        else:
                            timeout+=5
                            continue    
                    except requests.exceptions.ReadTimeout:
                        timeout+=5
                        continue
                    except requests.exceptions.ConnectionError:
                        timeout+=5
                        continue
                data = response.json()['data']
                for card in data:
                    if card['vendorCode'] in self.listVendorCodeToGet:
                        self.alredyGetVendorCode.append(card['vendorCode'])
                        self.listCardToChange.append(card)
        self.listCardToChange


    def getNomFromWB(self):
        # "\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Манвел.txt"
        # dataFromDB = pandas.DataFrame(pandas.read_table(self.DBpath))
        # self.DBpath = r"F:\Маски силикон\карточки.txt"
        if self.dataFromDB.size == 0:
            self.dataFromDB = pandas.read_table(self.DBpath)
        # print(dataFromDB.shape)
        # dataFromDB.to_csv(r"F:\Маски силикон\карточки.txt",index=None,sep='\t')
        # dataFromDB = pandas.DataFrame(pandas.read_table(r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Манвел.txt"))
        # print(self.listVendorCodeToGet)
        for vendorCode in self.listVendorCodeToGet:
            # try:
                # if vendorCode not in self.alredyGetVendorCode:
                    line = self.dataFromDB.loc[self.dataFromDB['vendorCode'] == vendorCode]
                    # print(line)
                    # imtID = line['imtID'].values.tolist()[0]
                    nmID = line['nmID'].values.tolist()[0]
                    self.nmIdsList.append(nmID)
                    chrtID = line['chrtID'].values.tolist()[0]
                    # price = line['price'].values.tolist()[0]
                    # skus = line['Баркод'].values.tolist()[0].strip('[]\'\"').split(',')
                    skus = line['skus'].values.tolist()[0].strip('[]\'\"').split(',')
                    # print(skus)
                    sizes = [
                        {
                        # "techSize": "0",
                        "chrtID": chrtID,
                        # "wbSize": "",
                        # "price": 590,
                        "skus": skus
                        }
                        ]
                    # data = [{
                    #         "imtID": imtID,
                    #         "nmID": nmID,
                    #         "vendorCode": vendorCode,
                    #         "sizes": sizes,
                    #         "characteristics": []
                    #         }]
                    dataV2 = [{
                            # "imtID": imtID,
                            "nmID": nmID,
                            "vendorCode": vendorCode,
                            "sizes": sizes,
                            "brand": '',
                            "title": '',
                            "description": '',
                            "characteristics": [],
                            'dimensions':{
                                'length':19,
                                'width':12,
                                'height':2}
                            }]
                    
                    # data = response.json()['data']
                    # for card in data:
                    #     if card['vendorCode'] in self.listVendorCodeToGet:
                    #         self.alredyGetVendorCode.append(card['vendorCode'])
                    #         self.listCardToChange.append(card)
                    # for card in dataV2:
                        # print(1)
                        # if card['vendorCode'] in self.listVendorCodeToGet:
                            # print(2)
                            # self.alredyGetVendorCode.append(card['vendorCode'])
                    self.listCardToChange.append(dataV2[0])
        # return [self.listCardToChange, self.nmIdsList]
            # except:
                # f = open(r'E:\MyProduct\Python\WB\MakePrint\errors.txt', 'a', encoding='utf-8')
                # f.write(vendorCode + '\n')
                # f.close()
                # continue
        # print(self.listCardToChange)
                

    def multiReplace(self, string):
        # .replace('золотистный','золотистый').replace('серебристный','серебристый').replace('корчневый','коричневый').replace('орпнжевый','оранжевый')
        replaceList = [
            ('золотистный','золотистый'),
            ('серебристный','серебристый'),
            ('корчневый','коричневый'),
            ('орпнжевый','оранжевый'),
            ('фоилетовый','фиолетовый'),
            ('юежевый', 'бежевый'),
            ('серный', 'серый')
        ]
        for item in replaceList:
            string = string.replace(item[0], item[1])
        return string.strip()




    def changeCards(self):
        # chek = len(self.listCardToChange) == len(self.alredyGetVendorCode) == len(self.listVendorCodeToGet) == len(self.dataDict)
        if True:
            for i, card in enumerate(self.listCardToChange):
                # print(len(self.listCardToChange))
                for case in self.dataDict:
                    if case['Артикул товара'] == card['vendorCode']:
                        # char = {"characteristics": [
                        #         {'Рисунок': self.chekCountField('Рисунок', case['Рисунок'])},# case['Рисунок'].split(';')},
                        #         {'Тип чехлов': self.chekCountField('Тип чехлов', case['Тип чехлов'])},# case['Тип чехлов'].split(';')},
                        #         #{'Повод': case['Повод'].split(';')},
                        #         {'Особенности чехла': self.chekCountField('Особенности чехла', case['Особенности чехла'])},# case['Особенности чехла'].split(';')},
                        #         {'Комплектация': case['Комплектация'].split(';')},
                        #         {'Модель': self.chekCountField('Модель', case['Модель'])},# case['Модель'].split(';')},
                        #         {'Вид застежки': self.chekCountField('Вид застежки', case['Вид застежки'])},# case['Вид застежки'].split(';')},
                        #         {'Декоративные элементы': self.chekCountField('Декоративные элементы', case['Декоративные элементы'])},#case['Декоративные элементы']},
                        #         {'Совместимость': case['Совместимость'].split(';')},
                        #         #{'Назначение подарка': case['Назначение подарка'].split(';')},
                        #         {'Любимые герои': self.chekCountField('Любимые герои', case['Любимые герои'])},# case['Любимые герои'].split(';')},
                        #         {'Материал изделия': self.chekCountField('Вид застежки', case['Материал изделия'])},# case['Материал изделия'].split(';')},
                        #         {'Производитель телефона': case['Производитель телефона']},
                        #         # {'Бренд': case['Бренд']},
                        #         # {'Бренд': '2Case'},
                        #         {'Страна производства': case['Страна производства'].split(';')},
                        #         # {'Наименование': case['Наименование']},
                        #         {'Предмет':'Чехлы для телефонов'},
                        #         # {'Предмет':case['Предмет']},
                        #         {'Цвет': case['Цвет'].lower().replace('золотистный','золотистый').split(';')},
                        #         # {'Описание': case['Описание']},
                        #         # {'Высота упаковки': 19},
                        #         # {'Ширина упаковки': 12},
                        #         # {'Длина упаковки': 2},
                        #     ]}
                        charNew = {"characteristics": [
                                {
                                    'id':12,
                                    'name':'Рисунок',
                                    'value':self.chekCountField('Рисунок', case['Рисунок'])
                                },
                                {
                                    'id':760,
                                    'name':'Тип чехлов',
                                    'value':self.chekCountField('Тип чехлов', case['Тип чехлов'])
                                },
                                {
                                    'id':124080,
                                    'name':'Особенности чехла',
                                    'value':self.chekCountField('Особенности чехла', case['Особенности чехла'])
                                },
                                {
                                    'id':378533,
                                    'name':'Комплектация',
                                    'value':case['Комплектация'].split(';')
                                },
                                {
                                    'id':746,
                                    'name':'Совместимость',
                                    'value':case['Совместимость'].split(';')
                                },
                                {
                                    'id':4,
                                    'name':'Вид застежки',
                                    'value':self.chekCountField('Вид застежки', case['Вид застежки'])
                                },
                                {
                                    'id':50,
                                    'name':'Декоративные элементы',
                                    'value':self.chekCountField('Декоративные элементы', case['Декоративные элементы'])
                                },
                                {
                                    'id':51,
                                    'name':'Любимые герои',
                                    'value':self.chekCountField('Любимые герои', case['Любимые герои'])
                                },
                                {
                                    'id':17596,
                                    'name':'Материал изделия',
                                    'value':self.chekCountField('Вид застежки', case['Материал изделия'])
                                },
                                {
                                    'id':14177451,
                                    'name':'Страна производства',
                                    'value':case['Страна производства'].split(';')
                                },
                                {
                                    'id':14177449,
                                    'name':'Цвет',
                                    'value':[x.strip() for x in self.multiReplace(case['Цвет'].lower()).split(';')]
                                },
                            ]}
                        # tmp = [{'Артикул товара': case['Артикул товара'], 'Баркоды': [f'test{i}',f'test{i+1}']}]
                        tmp = [{'Артикул товара': case['Артикул товара'], 'Баркоды': card['sizes'][0]['skus'], 'nmID':card['nmID']}]
                        self.vendorCodesAndBarcodes = pandas.concat([self.vendorCodesAndBarcodes,pandas.DataFrame(tmp)])
                        card.update(charNew)
                        # card.update({'brand':case['Бренд']})
                        card.update({'brand':"2Case"})
                        card.update({'title':case['Наименование']})
                        card.update({'description': case['Описание']})
                        
                        self.listCardToChange
            self.listCardToChange
        else:
            print('Количество не совпадает, проверка не прошла')


    def pushChanges(self):
       # for card in self.listCardToChange:
       step = 100
       for i in range(0, len(self.listCardToChange), step):
            timeout = 20              
            jsonRequestsUpdateCard = self.listCardToChange[i:i+step]
            while timeout < 60:
                try:
                    # ref = pickle.load(open(r'E:\MyProduct\Python\WB\MakePrint\Class\jsonRequestsUpdateCard.pkl', 'rb'))
                    response = requests.post(self.urlUpdateCards, headers=self.headersGetCard, json=jsonRequestsUpdateCard, timeout=timeout)
                    if response.status_code ==200:
                        print(response.text)
                        break
                    else:
                        if 'Failed to update, nm' in response.text:
                            print('__Error__' +  ' ' +response.text)
                            nmError = int(response.json()['errorText'].replace('Failed to update, nm ','').replace(' can not be found', ''))
                            self.errorsList.append({'nmID':nmError,
                                                    'Файл':self.pathToFileForUpload}
                            )
                            for i, card in enumerate(jsonRequestsUpdateCard):
                                if card['nmID'] == nmError:
                                    jsonRequestsUpdateCard.pop(i)
                                    # print('Исправляю')
                                    break
                                continue
                            for i, card in enumerate(self.listCardToChange):
                                if card['nmID'] == nmError:
                                    self.listCardToChange.pop(i)
                                    print('Исправляю')
                                    break
                                continue
                        timeout+=5
                        time.sleep(2)
                        continue    
                except requests.exceptions.ReadTimeout:
                    time.sleep(2)
                    timeout+=5
                    continue
                except requests.exceptions.ConnectionError:
                    time.sleep(2)
                    timeout+=5
                    continue
            time.sleep(2)

    def splitNom(self):
        url = 'https://suppliers-api.wildberries.ru/content/v2/cards/moveNm'
        headers = {'Authorization': '{}'.format(self.token)} 
        for i in range(0,len(self.nmIdsList),30):
            x = self.nmIdsList[i:i+30]
            json = {
                'nmIDs':x
            }
            r = requests.post(url=url, json=json, headers=headers, timeout=30)
            if r.status_code == 200:
                print('объеденил успешно ' + str(x))
            elif r.status_code == 400 and "Все карточки находятся в одной группе" in r.text:
                time.sleep(1.2)
                print('уже вместе ' + str(x))
            else:
                time.sleep(1.2)
                print('ОШИБКА ' + str(x) + r.text)
            time.sleep(5)
    

    def splitNom2(self):
        url = 'https://suppliers-api.wildberries.ru/content/v2/cards/moveNm'
        headers = {'Authorization': '{}'.format(self.token)} 
        step = 30
        print('Начал объединять')
        for group in self.CategoryAndIDsByGroup:
            nmIDList = group['nmID_x'].values.tolist()
            for line in self.errorsList:
                for i in nmIDList:
                    if i == line['nmID']:
                        print('1')
            for i in range(0,len(nmIDList),step):
                x = nmIDList[i:i+step]
                json = {
                    'nmIDs':x
                }
                countTry = 0
                while countTry < 5:
                    r = requests.post(url=url, json=json, headers=headers, timeout=60)
                    if r.status_code == 200:
                        break
                        pass
                        # print('объеденил успешно ' + str(x))
                    elif r.status_code == 400 and "All cards are in the same group" in r.text:
                        break
                        pass
                        # print('уже вместе ' + str(x))
                    elif r.status_code == 500:
                        countTry+=1
                        continue

                    else:
                        print('ОШИБКА ' + str(x))
                        time.sleep(1.2)
                        countTry+=1
                        continue
                time.sleep(1.2)



# dataFromDB = pandas.read_table(r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Караханян.txt')
# df = pandas.read_excel(r"F:\Для загрузки\Готовые принты\Чехол Realme 11 4G силикон с зак.кам. проз. под карту.xlsx")
# dfNew = dataFromDB.loc[dataFromDB['vendorCode'] == df['Артикул товара']]
# dfNew
# df