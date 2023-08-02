import sys
from os.path import join as joinPath, basename
sys.path.insert(1, joinPath(sys.path[0], '../..'))
import requests
import pandas
import copy
import numpy
import asyncio
import aiohttp
from aiohttp import ClientConnectorError
import subprocess


class ExistsNomenclaturesCreater:    
    def __init__(self, data, mode, pathToFileForUpload):
        self.tokenAb = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM5NjgxZDkxLWVmYzctNGVjOC05NzIzLTgyN2JkZTY2NWFkYyJ9.j4gqyXEe0Guzr_CbKNmFRxf_zyqjjyJ6dODc4oQII2E'   
        self.tokenIvan = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImUyZTIyZGE1LTYxYWYtNDgyMi1hMDVkLTZiNzVlMTBiNzlmMiJ9.yDq9XasZjs-oB1PapNbD_NWIH8tgWEz_WyKLvVTNgBs'
        self.tokenKar = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImU4NjQ1YWI5LWFjM2UtNGFkOS1hYmIyLThkMTMzMGM1YTU3NyJ9.8nz9gIHurlCVKIhruG6hY8MRBtMLvLYggVzisxgKivY'
        self.tokenSam = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImQ3ZTJkN2I4LWVjZDEtNDNiNC04ODkxLTg2ZWZhNDA0ODI0YyJ9.6qCa4264GF5uv76laTgfnvKD7RXyBLDOk8U_cHPoDDU'
        self.urlGetCards = 'https://suppliers-api.wildberries.ru/content/v1/cards/filter'
        self.urlUpdateCards = 'https://suppliers-api.wildberries.ru/content/v1/cards/update'
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
        if mode =='Караханян':
            self.DBpath = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Караханян.txt'
            self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImU4NjQ1YWI5LWFjM2UtNGFkOS1hYmIyLThkMTMzMGM1YTU3NyJ9.8nz9gIHurlCVKIhruG6hY8MRBtMLvLYggVzisxgKivY'
        elif mode =='Абраамян':
            self.DBpath = r'\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Манвел.txt'
            self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM5NjgxZDkxLWVmYzctNGVjOC05NzIzLTgyN2JkZTY2NWFkYyJ9.j4gqyXEe0Guzr_CbKNmFRxf_zyqjjyJ6dODc4oQII2E'   
        elif mode =='Самвел':
            self.DBpath = r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Самвел2.txt"
            self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImQ3ZTJkN2I4LWVjZDEtNDNiNC04ODkxLTg2ZWZhNDA0ODI0YyJ9.6qCa4264GF5uv76laTgfnvKD7RXyBLDOk8U_cHPoDDU'
        elif mode =='Иван':
            self.DBpath = r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Федоров.txt"
            self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImUyZTIyZGE1LTYxYWYtNDgyMi1hMDVkLTZiNzVlMTBiNzlmMiJ9.yDq9XasZjs-oB1PapNbD_NWIH8tgWEz_WyKLvVTNgBs'
        self.headersGetCard = {'Authorization': '{}'.format(self.token)}


    def start(self):
        self.getNomFromWB()
        self.changeCards()
        self.pushChanges()
        self.updateFileForUpload()
        # self.createFileFor1C()


    
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
        self.dataDict = self.data.to_dict('records')
        self.dataDictNew = []
        for i, line in enumerate(self.dataDict):
            if len(line['Баркод товара']) > 1:
                for barcode in line['Баркод товара']:
                    lineNew = copy.deepcopy(line)
                    tmp = {'Баркод товара':barcode}
                    lineNew.update(tmp)
                    self.dataDictNew.append(lineNew)
            else:
                tmp = {'Баркод товара':''.join(line['Баркод товара'])}
                line.update(tmp)
                self.dataDictNew.append(line)
        df = pandas.DataFrame(self.dataDictNew)
        df.to_excel(self.pathToFileForUpload, index=False)

        # self.data['Баркод товара'] = 
        # for case in self.data:



    @staticmethod
    def uplaodImage(path, mode):
        if mode =='Караханян':
           token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjgxYjczNGVmLWI2OWUtNGRhMi1iNTBiLThkMTEyYWM4MjhkMCJ9.pU1YOOirgRe3Om-WRYT61AofToggCLbV3na7GbXKGqU'
        elif mode =='Абраамян':
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjNhZmUzMzMzLWFmYjEtNDI5Yi1hN2Q1LTE1Yjc4ODg4MmU5MSJ9.kWUDkHkGrtD8WxE9sQHto5B7L3bQh-XRDf7EeZQiw7A'   
        elif mode =='Самвел':
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImUxNGFmM2UxLTc0YTctNDlkOC1hNGIyLTI1Y2Q4ZDc2YmM4NSJ9.bCTyIoPVS3wpbzy7TdK-Gt8Sgz3iyPamzJjnA_EH3Iw'
        elif mode =='Иван':
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImIxYjQ3YjQzLTFhMTYtNGQ0Ni1iZTA1LWRlY2ExZTcxMTU0MSJ9.qTIJF6fEgbRux3Ps30ciMQ802UWqtAER-y94ALvE3PI'
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
        dataFromDB = pandas.DataFrame(pandas.read_table(self.DBpath))
        for vendorCode in self.listVendorCodeToGet:
            try:
                if vendorCode not in self.alredyGetVendorCode:
                    line = dataFromDB.loc[dataFromDB['vendorCode'] == vendorCode]
                    imtID = line['imtID'].values.tolist()[0]
                    nmID = line['nmID'].values.tolist()[0]
                    chrtID = line['chrtID'].values.tolist()[0]
                    price = line['price'].values.tolist()[0]
                    skus = line['skus'].values.tolist()[0].strip('[]\'\"').split(',')
                    sizes = [
                        {
                        "techSize": "0",
                        "chrtID": chrtID,
                        "wbSize": "",
                        "price": price,
                        "skus": skus
                        }
                        ]
                    data = [{
                            "imtID": imtID,
                            "nmID": nmID,
                            "vendorCode": vendorCode,
                            "sizes": sizes,
                            "characteristics": []
                            }]
                    
                    # data = response.json()['data']
                    for card in data:
                        if card['vendorCode'] in self.listVendorCodeToGet:
                            self.alredyGetVendorCode.append(card['vendorCode'])
                            self.listCardToChange.append(card)
            except:
                f = open(r'E:\MyProduct\Python\WB\MakePrint\errors.txt', 'a', encoding='utf-8')
                f.write(vendorCode + '\n')
                f.close()
                continue
        self.listCardToChange
                
    def changeCards(self):
        chek = len(self.listCardToChange) == len(self.alredyGetVendorCode) == len(self.listVendorCodeToGet) == len(self.dataDict)
        if True:
            for i, card in enumerate(self.listCardToChange):
                for case in self.dataDict:
                    if case['Артикул товара'] == card['vendorCode']:
                        char = {"characteristics": [
                                {'Рисунок': case['Рисунок'].split(';')},
                                {'Тип чехлов': case['Тип чехлов'].split(';')},
                                #{'Повод': case['Повод'].split(';')},
                                {'Особенности чехла': case['Особенности чехла'].split(';')},
                                {'Комплектация': case['Комплектация'].split(';')},
                                {'Модель': case['Модель'].split(';')},
                                {'Вид застежки': case['Вид застежки'].split(';')},
                                {'Декоративные элементы': case['Декоративные элементы']},
                                {'Совместимость': case['Совместимость'].split(';')},
                                #{'Назначение подарка': case['Назначение подарка'].split(';')},
                                {'Любимые герои': case['Любимые герои'].split(';')},
                                {'Материал изделия': case['Материал изделия'].split(';')},
                                {'Производитель телефона': case['Производитель телефона']},
                                {'Бренд': case['Бренд']},
                                {'Страна производства': case['Страна производства'].split(';')},
                                {'Наименование': case['Наименование']},
                                {'Предмет':'Чехлы для телефонов'},
                                # {'Предмет':case['Предмет']},
                                {'Цвет': case['Цвет'].split(';')},
                                {'Описание': case['Описание']},
                                {'Высота упаковки': 19},
                                {'Ширина упаковки': 12},
                                {'Длина упаковки': 2},
                            ]}
                        # tmp = [{'Артикул товара': case['Артикул товара'], 'Баркоды': [f'test{i}',f'test{i+1}']}]
                        tmp = [{'Артикул товара': case['Артикул товара'], 'Баркоды': card['sizes'][0]['skus']}]
                        self.vendorCodesAndBarcodes = pandas.concat([self.vendorCodesAndBarcodes,pandas.DataFrame(tmp)])
                        card.update(char)
                        
                        self.listCardToChange
            self.listCardToChange
        else:
            print('Количество не совпадает, проверка не прошла')


    def pushChanges(self):
       # for card in self.listCardToChange:
       step = 10
       for i in range(0, len(self.listCardToChange), step):
            timeout = 10              
            jsonRequestsUpdateCard = self.listCardToChange[i:i+step]
            while timeout < 60:
                try:
                    response = requests.post(self.urlUpdateCards, headers=self.headersGetCard, json=jsonRequestsUpdateCard, timeout=timeout)
                    if response.status_code ==200:
                        print(response.text)
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