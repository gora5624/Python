from cProfile import label
from unicodedata import category
from Class.CardBodyClass import CardCase, Nomenclature
import sys
from os.path import join as joinPath
sys.path.insert(1, joinPath(sys.path[0], '../..'))
from my_mod.my_lib import read_xlsx
import requests
import pandas
import time
import multiprocessing
import asyncio
import aiohttp


class WBnomenclaturesCreater:
    def __init__(self):
        self.tokenAb = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'   
        self.tokenKar = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
        self.tokenSam = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
        self.urlCreate = 'https://suppliers-api.wildberries.ru/content/v1/cards/upload'
        self.urlAdd = 'https://suppliers-api.wildberries.ru/content/v1/cards/upload/add'
        self.pathToFileForUpload = ''
        self.modelForUploads = []


    @staticmethod
    def uploadsImage(mode, fileName):
        # Загрузить фото
        if mode =='Караханян':
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
        elif mode =='Абраамян':
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
        elif mode =='Самвел':
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
        requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/media/save'
        nomenclatureList = pandas.read_excel(fileName).to_dict('records')
        for nomenclature in nomenclatureList:
            jsonRequest = {
            "vendorCode": nomenclature['Артикул товара'],
            "data": nomenclature['Медиафайлы'].split(';')
            }
            headersRequest = {'Authorization': '{}'.format(token), 'X-Vendor-Code': nomenclature['Артикул товара']}
            responce = requests.post(requestUrl, json=jsonRequest, headers=headersRequest)
            responce

    def createNomenclaturesMultiporocessing(self, mode):
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
                        'mediaFiles': case['Медиафайлы'].split(';'),
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
        pool = multiprocessing.Pool()
        for model in self.modelForUploads:
            pool.apply_async(self.createNomenclatureSingleProcess, args=(model, headersRequest,))
        pool.close()
        pool.join()

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


    def createNomenclatureSingleProcess(self, modelListCard, headersRequest):
        vendorCodeMain = modelListCard[0]['vendorCode']
        jsonCard = [[modelListCard[0]]]
        responce = requests.post(self.urlCreate, json=jsonCard, headers=headersRequest)
        if responce.status_code == 200:
            print(vendorCodeMain + ' успешно создана')
        else:
            print(responce.text)
            print(vendorCodeMain + ' ошибка при создании, проверь ВБ')
        # for i in range(1,len(modelListCard),1):
        #     jsonNomenclature = {
        #         'vendorCode': vendorCodeMain,
        #         'cards': modelListCard[i:i+10]
        #     }
        self.startCeateNomenclaturesAsyncio(modelListCard[1:], headersRequest, vendorCodeMain)
            #responce = requests.post(self.urlAdd, json=jsonNomenclature, headers=headersRequest)
            # if responce.status_code == 200:
            #     print(vendorCodeMain + ' успешно создана')
            # else:
            #     print(responce.text)
            #     print(vendorCodeMain + ' ошибка при создании, проверь ВБ')



    async def createNomenclaturesGetRequests(self, session, jsonNomenclature, headersRequest):
        async with session.post(self.urlAdd, headers=headersRequest, json=jsonNomenclature) as response: 
                            if response.status != 200:
                                print(response.status)
                                print(await response.text())
                            else:
                                print(await response.text())
                                #await asyncio.sleep(5)
                                #continue



    async def createNomenclaturesAsyncioCreateTasks(self, modelListCard, headersRequest, vendorCodeMain):
        tasks = []
        async with aiohttp.ClientSession() as session:
            #for offset in range(0,totalCards,10):
            for i in range(len(modelListCard)):
                jsonNomenclature = {
                'vendorCode': vendorCodeMain,
                'cards': [modelListCard[i]]
            }
                tasks.append(asyncio.create_task(self.createNomenclaturesGetRequests(session, jsonNomenclature, headersRequest)))
            await asyncio.wait(tasks)
        #return self.cardslist


    def startCeateNomenclaturesAsyncio(self, modelListCard, headersRequest, vendorCodeMain):
        loop = asyncio.get_event_loop()
        result =  loop.run_until_complete(self.createNomenclaturesAsyncioCreateTasks(modelListCard, headersRequest, vendorCodeMain))
        #return result

    