from cProfile import label
import imp
from unicodedata import category
from urllib import response
from Class.CardBodyClass import CardCase, Nomenclature
import sys
from os.path import join as joinPath
from os import system
sys.path.insert(1, joinPath(sys.path[0], '../..'))
from my_mod.my_lib import read_xlsx
import requests
import pandas
import time
import multiprocessing
import asyncio
import aiohttp
from aiohttp import ClientConnectorError
import subprocess
# from requests import ConnectionError



class WBnomenclaturesCreater:    
    def __init__(self):
        self.tokenAb = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'   
        self.tokenKar = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
        self.tokenSam = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
        self.urlCreate = 'https://suppliers-api.wildberries.ru/content/v1/cards/upload'
        self.urlAdd = 'https://suppliers-api.wildberries.ru/content/v1/cards/upload/add'
        self.pathToFileForUpload = ''
        self.modelForUploads = []


    # @staticmethod
    # def uploadsImage(mode, fileName):
    #     # Загрузить фото
    #     if mode =='Караханян':
    #         token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
    #     elif mode =='Абраамян':
    #         token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
    #     elif mode =='Самвел':
    #         token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
    #     requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/media/save'
    #     nomenclatureList = pandas.read_excel(fileName).to_dict('records')
    #     for nomenclature in nomenclatureList:
    #         jsonRequest = {
    #         "vendorCode": nomenclature['Артикул товара'],
    #         "data": nomenclature['Медиафайлы'].split(';')
    #         }
    #         headersRequest = {'Authorization': '{}'.format(token), 'X-Vendor-Code': nomenclature['Артикул товара']}
    #         responce = requests.post(requestUrl, json=jsonRequest, headers=headersRequest)
    #         responce

    @staticmethod
    def uplaodImage(path, token):
        args = [sys.executable, r'E:\MyProduct\Python\WB\MakePrint\Moduls\udatePhoto.py', path.replace(' ', '#'), token]
        subprocess.Popen(args, shell=True)


    def createNomenclaturesMultiporocessing(self, mode):
        listDoneVendorCode = []
        start_time = time.time()
        nomenclature = []
        if mode =='Караханян':
            token = self.tokenKar
        elif mode =='Абраамян':
            token = self.tokenAb
        elif mode =='Самвел':
            token = self.tokenSam
        if self.pathToFileForUpload =='':
            print('Путь к файлу не указан')
            return 0
        data = pandas.DataFrame(pandas.read_excel(self.pathToFileForUpload))
        categoryList = data['Категория'].unique().tolist()
        for category in categoryList:
            nomenclature = []
            dataCategory = data[data.Категория == category].to_dict('records')
            for case in dataCategory:
                card = {
                        "vendorCode": case['Артикул товара'],
                        #'mediaFiles': case['Медиафайлы'].split(';'),
                        "characteristics": [
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
                            {'Предмет':'Чехлы для телефонов'},
                            {'Цвет': case['Цвет'].split(';')},
                            {'Описание': case['Описание']},
                            {'Высота упаковки': 18.5},
                            {'Ширина упаковки': 11},
                            {'Глубина упаковки': 1.5},
                            {'Медиафайлы': case['Медиафайлы'].split(';')}
                        ],
                        "sizes": [
                            {
                            'techSize': '0',
                            "price": case['Цена'],
                            "skus": [
                                str(case['Баркод товара'])
                            ]
                            }
                        ]
                        }
                nomenclature.append(card)
            self.modelForUploads.append(nomenclature)
        headersRequest = {'Authorization': '{}'.format(token)}
        # self.modelForUploads
        for i in range(5):
            pool = multiprocessing.Pool()
            for model in self.modelForUploads:
                # if model[''] not in listDoneVendorCode:
                pool.apply_async(self.createNomenclatureSingleProcess, args=(model, headersRequest,token,listDoneVendorCode, ))
            pool.close()
            pool.join()
            listDoneVendorCode = self.getListNomenclatures(token, self.modelForUploads)
            self.uplaodImage(self.pathToFileForUpload, token)
            # time.sleep(20)
        print("--- %s seconds ---" % (time.time() - start_time))

            # vendorCodeMain = model[0]['vendorCode']
            # jsonCard = [[model[0]]]
            # responce = requests.post(self.urlCreate, json=jsonCard, headers=headersRequest)
            # if responce.status_code == 200:
            #     print(vendorCodeMain + ' успешно создана')
            # else:
            #     print(responce.text)
            #     print(vendorCodeMain + ' ошибка при создании, проверь ВБ')
            # for i in range(1,len(model),50):
            #     jsonNomenclature = {
            #         'vendorCode': vendorCodeMain,
            #         'cards': model[i:i+50]
            #     }
            #     responce = requests.post(self.urlAdd, json=jsonNomenclature, headers=headersRequest)
            #     if responce.status_code == 200:
            #         print(vendorCodeMain + ' успешно создана')
            #     else:
            #         print(responce.text)
            #         print(vendorCodeMain + ' ошибка при создании, проверь ВБ')


    def createNomenclatureSingleProcess(self, modelListCard, headersRequest,token, listDoneVendorCode):
        vendorCodeMain = modelListCard[0]['vendorCode']
        jsonCard = [[modelListCard[0]]]
        for i in jsonCard[0][0]['characteristics']:
                j = list(i.items())[0]
                if j[0] == 'Медиафайлы':
                    urlsList = j[1]
                    break
        if vendorCodeMain not in listDoneVendorCode:
            try:
                responce = requests.post(self.urlCreate, json=jsonCard, headers=headersRequest)
            except requests.ConnectionError:
                responce = requests.post(self.urlCreate, json=jsonCard, headers=headersRequest)
            if responce.status_code == 200:
                print(vendorCodeMain + ' успешно создана')
                #time.sleep(1)
                # p = multiprocessing.Process(target=self.uplaodImage, args=(vendorCodeMain, urlsList, token,))
                # p.start()
            # else:
            #     print(responce.text)
            #     print(vendorCodeMain + ' ошибка при создании, проверь ВБ')
        for i in range(1,len(modelListCard),1):
            jsonNomenclature = {
                'vendorCode': vendorCodeMain,
                'cards': modelListCard[i:i+1]
                
            }
        # self.startCeateNomenclaturesAsyncio(modelListCard[1:], headersRequest, vendorCodeMain)
            if modelListCard[i]['vendorCode'] not in listDoneVendorCode:
                try:
                    responce = requests.post(self.urlAdd, json=jsonNomenclature, headers=headersRequest)
                except requests.ConnectionError:
                    responce = requests.post(self.urlAdd, json=jsonNomenclature, headers=headersRequest)
                vendorCode = jsonNomenclature['cards'][0]['vendorCode']
                for i in jsonNomenclature['cards'][0]['characteristics']:
                    j = list(i.items())[0]
                    if j[0] == 'Медиафайлы':
                        urlsList = j[1]
                        break
                if responce.status_code == 200:
                    print(vendorCodeMain + ' успешно создана')
                else:
                    print(responce.text)
                    # print(vendorCodeMain + ' ошибка при создании, проверь ВБ')
        

    def getListNomenclatures(self, token, modelListCard):
        requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/cards/list'
        headersRequest = {'Authorization': '{}'.format(token)}
        dataCard = []
        for i in range(0,len(modelListCard)*20,1000):
            jsonRequest = {
                    "sort": {
                    "limit": 1000,
                    "offset": i,
                    "sortColumn": "updateAt",
                    "ascending": False
                    }
                }
            response = requests.post(requestUrl, headers=headersRequest, json=jsonRequest).json()
            for i in response['data']['cards']:
                dataCard.append(i['vendorCode'])
            # dataCard.extend(response['data']['cards'])
        return(dataCard)






    async def createNomenclaturesGetRequests(self, jsonNomenclature, headersRequest):
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(self.urlAdd, headers=headersRequest, json=jsonNomenclature) as response: 
                        if response.status == 429:
                            print(response.status)
                            print(await response.text())
                            await asyncio.sleep(5)
                            await session.close()
                            continue
                        elif response.status == 200:
                            print('Успешно' + await response.text())
                            await session.close()
                            break
                        else:
                            #print(await response.text())
                            await session.close()
                            break
                            #await asyncio.sleep(5)
                            #continue
            except ClientConnectorError:
                continue




    async def createNomenclaturesAsyncioCreateTasks(self, modelListCard, headersRequest, vendorCodeMain):
        tasks = []
        #for offset in range(0,totalCards,10):
        try:
            for i in range(len(modelListCard)):
                jsonNomenclature = {
                'vendorCode': vendorCodeMain,
                'cards': [modelListCard[i]]
            }
                tasks.append(asyncio.create_task(self.createNomenclaturesGetRequests(jsonNomenclature, headersRequest)))
            await asyncio.wait(tasks)
        except ValueError:
            print('Ошибка')
    #return self.cardslist


    def startCeateNomenclaturesAsyncio(self, modelListCard, headersRequest, vendorCodeMain):
        loop = asyncio.get_event_loop()
        result =  loop.run_until_complete(self.createNomenclaturesAsyncioCreateTasks(modelListCard, headersRequest, vendorCodeMain))
        #return result

    