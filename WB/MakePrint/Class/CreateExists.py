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
        self.tokenAb = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'   
        self.tokenKar = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
        self.tokenIvan = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImIxYjQ3YjQzLTFhMTYtNGQ0Ni1iZTA1LWRlY2ExZTcxMTU0MSJ9.qTIJF6fEgbRux3Ps30ciMQ802UWqtAER-y94ALvE3PI'
        self.tokenSam = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
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
           self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
        elif mode =='Абраамян':
            self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'   
        elif mode =='Самвел':
            self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
        elif mode =='Иван':
            self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImIxYjQ3YjQzLTFhMTYtNGQ0Ni1iZTA1LWRlY2ExZTcxMTU0MSJ9.qTIJF6fEgbRux3Ps30ciMQ802UWqtAER-y94ALvE3PI'
        self.headersGetCard = {'Authorization': '{}'.format(self.token)}


    def start(self):
        self.getNomFromWB()
        self.changeCards()
        # self.pushChanges()
        self.updateFileForUpload()
        self.createFileFor1C()


    
    def createFileFor1C(self):
        dataFor1C = []
        Nom1CData = pandas.DataFrame(pandas.read_table(self.pathTo1CNom, sep='\t'))
        nameFile = basename(self.pathToFileForUpload)
        nameCase = nameFile.replace('.xlsx', '')
        nameCaseFull = Nom1CData[Nom1CData['Наименование']==nameCase]['Наименование для печати'].values[0]
        size = Nom1CData[Nom1CData['Наименование']==nameCase]['Размер чехла'].values[0]
        if pandas.isnull(size) and 'книга' in nameCase:
                size = 'Книга'
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
           token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
        elif mode =='Абраамян':
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'   
        elif mode =='Самвел':
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
        elif mode =='Иван':
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImIxYjQ3YjQzLTFhMTYtNGQ0Ni1iZTA1LWRlY2ExZTcxMTU0MSJ9.qTIJF6fEgbRux3Ps30ciMQ802UWqtAER-y94ALvE3PI'
        args = [sys.executable, r'E:\MyProduct\Python\WB\MakePrint\Moduls\udatePhoto.py', path.replace(' ', '#'), token]
        subprocess.Popen(args, shell=True).wait()
        # args2 = [sys.executable, r'E:\MyProduct\Python\WB\MakePrint\Moduls\chekUdatePhoto.py', path.replace(' ', '#'), token]
        # subprocess.Popen(args2, shell=True)


    def getNomFromWB(self):
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
                
    def changeCards(self):
        chek = len(self.listCardToChange) == len(self.alredyGetVendorCode) == len(self.listVendorCodeToGet) == len(self.dataDict)
        if chek:
            for i, card in enumerate(self.listCardToChange):
                for case in self.dataDict:
                    if case['Артикул товара'] == card['vendorCode']:
                        char = {"characteristics": [
                                {'Рисунок': case['Рисунок'].split(';')},
                                {'Тип чехлов': case['Тип чехлов'].split(';')},
                                {'Повод': case['Повод'].split(';')},
                                {'Особенности чехла': case['Особенности чехла'].split(';')},
                                {'Комплектация': case['Комплектация'].split(';')},
                                {'Модель': case['Модель'].split(';')},
                                {'Вид застежки': case['Вид застежки'].split(';')},
                                {'Декоративные элементы': case['Декоративные элементы']},
                                {'Совместимость': case['Совместимость'].split(';')},
                                {'Назначение подарка': case['Назначение подарка'].split(';')},
                                {'Любимые герои': case['Любимые герои'].split(';')},
                                {'Материал изделия': case['Материал изделия'].split(';')},
                                {'Производитель телефона': case['Производитель телефона']},
                                {'Бренд': case['Бренд']},
                                {'Страна производства': case['Страна производства'].split(';')},
                                {'Наименование': case['Наименование']},
                                {'Предмет':case['Предмет']},
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
                        print('done')
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