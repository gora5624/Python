
import sys
from os.path import join as joinPath, abspath
import requests
import pandas
import time
import multiprocessing
import asyncio
import aiohttp
from aiohttp import ClientConnectorError
import subprocess
sys.path.append(abspath(joinPath(__file__, '...')))
from Moduls.udatePhoto import updatePhotoMain
from Moduls.udatePhotoSkinShell import udatePhotoSkinShellMain


class WBnomenclaturesCreater:    
    def __init__(self):
        self.tokenAb = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM5NjgxZDkxLWVmYzctNGVjOC05NzIzLTgyN2JkZTY2NWFkYyJ9.j4gqyXEe0Guzr_CbKNmFRxf_zyqjjyJ6dODc4oQII2E'   
        self.tokenIvan = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImUyZTIyZGE1LTYxYWYtNDgyMi1hMDVkLTZiNzVlMTBiNzlmMiJ9.yDq9XasZjs-oB1PapNbD_NWIH8tgWEz_WyKLvVTNgBs'
        self.tokenKar = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImU4NjQ1YWI5LWFjM2UtNGFkOS1hYmIyLThkMTMzMGM1YTU3NyJ9.8nz9gIHurlCVKIhruG6hY8MRBtMLvLYggVzisxgKivY'
        self.tokenSam = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImQ3ZTJkN2I4LWVjZDEtNDNiNC04ODkxLTg2ZWZhNDA0ODI0YyJ9.6qCa4264GF5uv76laTgfnvKD7RXyBLDOk8U_cHPoDDU'
        self.urlCreate = 'https://suppliers-api.wildberries.ru/content/v1/cards/upload'
        self.urlAdd = 'https://suppliers-api.wildberries.ru/content/v1/cards/upload/add'
        self.pathToFileForUpload = ''
        self.modelForUploads = []
        self.listDoneVendorCode = []
        self.timeout = 10


    @staticmethod
    def uplaodImage(path, token):
        if "skinshell" in path.lower():
            udatePhotoSkinShellMain(path, token)
        else:
            try:
                updatePhotoMain(path, token)
                # p = multiprocessing.Process(target=updatePhotoMain, args=(path, token))
                # p.start()
                # p.join()
            except:
                print('_______ERROR________' + path)
            #args = [sys.executable, r'E:\MyProduct\Python\WB\MakePrint\Moduls\udatePhoto.py', path.replace(' ', '#'), token]
            #subprocess.Popen(args, shell=True).wait()            
        # args2 = [sys.executable, r'E:\MyProduct\Python\WB\MakePrint\Moduls\chekUdatePhoto.py', path.replace(' ', '#'), token]
        # subprocess.Popen(args2, shell=True)

    def createNomenclaturesMultiporocessing(self, mode):
        # LogMaker.metodStart('createNomenclaturesMultiporocessing', {'mode':'str(mode)'})
        start_time = time.time()
        nomenclature = []
        if mode =='Караханян':
            token = self.tokenKar
        elif mode =='Абраамян':
            token = self.tokenAb
        elif mode =='Самвел':
            token = self.tokenSam
        elif mode =='Иван':
            token = self.tokenIvan
        if self.pathToFileForUpload =='':
            print('Путь к файлу не указан')
            return 0
        data = pandas.DataFrame(pandas.read_excel(self.pathToFileForUpload))
        nomenclature = []
        for case in data.to_dict('records'):
            card = {
                    "vendorCode": case['Артикул товара'],
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
                        {'Предмет':case['Предмет']},
                        {'Цвет': case['Цвет'].split(';')},
                        {'Описание': case['Описание']},
                        {'Высота упаковки': 19},
                        {'Ширина упаковки': 12},
                        {'Длина упаковки': 2},
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
        # try:
        #     self.getListNomenclaturesMulti(token, self.modelForUploads)
        # except:
        #     pass
        for i in range(3):
            # pool = multiprocessing.Pool()
            for model in self.modelForUploads:
                # if model[''] not in listDoneVendorCode:
            #     pool.apply_async(self.createNomenclatureSingleProcess, args=(model, headersRequest,token, ))
                    self.createNomenclatureSingleProcess(model, headersRequest,token)
            # pool.close()
            # pool.join()
            # try:
            #     self.getListNomenclaturesMulti(token, self.modelForUploads)
            # except:
            #     pass
        print("--- %s seconds ---" % (time.time() - start_time))



    def createNomenclatureSingleProcess(self, modelListCard, headersRequest,token):
        vendorCodeMain = modelListCard[0]['vendorCode']
        jsonCard = [[modelListCard[0]]]
        if vendorCodeMain not in self.listDoneVendorCode:
            countTry = 0
            delta = 0
            while True and countTry <10:
                try:
                    # print("TRY1")
                    responce = requests.post(self.urlCreate, json=jsonCard, headers=headersRequest, timeout=self.timeout+delta)
                    # print("responce = requests.post(self.urlCreate, json=jsonCard, headers=headersRequest)4")
                    if responce.status_code == 200:
                        # print("responce.status_code == 200:")
                        # LogMaker.logAction('createNomenclatureSingleProcess', vendorCodeMain +'  успешно создана')
                            print(vendorCodeMain + ' успешно создана')
                            time.sleep(2)
                            break
                        #time.sleep(1)
                        # p = multiprocessing.Process(target=self.uplaodImage, args=(vendorCodeMain, urlsList, token,))
                        # p.start()
                    else:
                        if 'Внутренняя ошибка' in responce.text:
                            time.sleep(5)
                        delta+=5
                        countTry+=1
                        continue
                except requests.ConnectionError:
                    time.sleep(5)
                    # print("except requests.ConnectionError:1")
                    countTry+=1
                    # print("responce = requests.post(self.urlCreate, json=jsonCard, headers=headersRequest)6")
                    continue
                except:
                    time.sleep(5)
                    countTry+=1
                    # print('Timeout')
                    continue
            
            # else:
            #     print(responce.text)
            #     print(vendorCodeMain + ' ошибка при создании, проверь ВБ')
        for i,value in enumerate(modelListCard):
            # print("for i in range(1,len(modelListCard),1):")
            if i == 0:
                continue
            if i%200 == 0:
                self.createNomenclatureSingleProcess(modelListCard[i:], headersRequest,token)
                return
            jsonNomenclature = {
                'vendorCode': vendorCodeMain,
                'cards': modelListCard[i:i+1]
                
            }
        # self.startCeateNomenclaturesAsyncio(modelListCard[1:], headersRequest, vendorCodeMain)
            if modelListCard[i]['vendorCode'] not in self.listDoneVendorCode:
                # print("modelListCard[i]['vendorCode']")
                countTry = 0
                delta =0
                while True and countTry <10:
                    # print("while True and countTry <10:")
                    try:
                        # print('requests.post(self.urlAdd, json=jsonNomenclature, headers=headersRequest)')
                        responce = requests.post(self.urlAdd, json=jsonNomenclature, headers=headersRequest, timeout=self.timeout+delta)
                        # time.sleep(5)
                        if responce.status_code == 200:
                            # print("responce.status_code == 200:2")
                            # LogMaker.logAction('createNomenclatureSingleProcess', vendorCodeMain +'  успешно создана')
                            vendorCodeMain = modelListCard[i]['vendorCode']
                            print(modelListCard[i]['vendorCode'] + ' успешно создана')
                            time.sleep(2)
                            break
                        else:
                            if 'Внутренняя ошибка' in responce.text:
                                time.sleep(5)
                                delta+=2
                                countTry+=1
                                continue
                            # print("responce.text123")
                            # LogMaker.logAction('createNomenclatureSingleProcess', responce.text)
                            if 'Указанные Артикулы товара используются в других карточках' in responce.text:
                                if modelListCard[i]['vendorCode'] in responce.text:
                                    self.listDoneVendorCode.append(modelListCard[i]['vendorCode'])
                                break
                            elif 'Недопустимо отправлять дублирующиеся запросы!' in responce.text:
                                time.sleep(5)
                                delta+=2
                                countTry+=1
                                continue
                            print(responce.text)
                            delta+=2
                            countTry+=1
                            continue
                    # print(vendorCodeMain + ' ошибка при создании, проверь ВБ')
                    except requests.ConnectionError:
                        time.sleep(5)
                        # print('requests.ConnectionError')
                        countTry+=1
                        print(str(countTry))
                        continue
                    except:
                        time.sleep(5)
                        # print('Timeuot')
                        countTry+=1
                        print(str(countTry))
                        continue
                if countTry >=10:
                    # print("countTry >=10:")
                    continue
                # vendorCode = jsonNomenclature['cards'][0]['vendorCode']
                # for i in jsonNomenclature['cards'][0]['characteristics']:
                #     j = list(i.items())[0]
                #     if j[0] == 'Медиафайлы':
                #         urlsList = j[1]
                #         break
                
        # LogMaker.metodEnd('createNomenclatureSingleProcess', '')
        

    def getListNomenclaturesMulti(self, token, modelListCard):
        # LogMaker.metodStart('getListNomenclatures', {'token': token, 'modelListCard': 'str(modelListCard)'})
        headersRequest = {'Authorization': '{}'.format(token)}
        listToGet =[]
        countToRequests = 50
        manager = multiprocessing.Manager()
        listDoneVendorCode = manager.list()
        pList = []
        pool = multiprocessing.Pool()
        for cards in modelListCard:
            #listToGet =[]
            #for card in cards:
            # listToGet = [cards[0]['vendorCode']]
            jsonRequest = {
                    "vendorCodes": [cards[0]['vendorCode']]
                    }
            pool.apply_async(self.getListNomenclaturesProcess, args=(jsonRequest, headersRequest, listDoneVendorCode, ))
        pool.close()
        pool.join()
        #     p = multiprocessing.Process(target=self.getListNomenclaturesProcess, args=(jsonRequest, headersRequest, listDoneVendorCode, ))
        #     p.start()
        #     pList.append(p)
        # for p in pList:
        #     p.join()
        self.listDoneVendorCode = list(listDoneVendorCode)

            # while True and countTry <2:
            #     try:
            #         response = requests.post(requestUrl, headers=headersRequest, json=jsonRequest, timeout=30)
            #         break
            #     except:
            #         countTry+=1
            #         continue
            # if response.status_code ==200:
            #     if len(data:=response.json()['data']) !=0:
            #         for card in data: 
            #             self.listDoneVendorCode.append(card['vendorCode'])
            # LogMaker.logAction('getListNomenclatures', 'Получает {} карточек из {}'.format(str(i),len(modelListCard)*2))


    def getListNomenclaturesProcess(self, jsonRequest, headersRequest, listDoneVendorCode):
        requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/cards/filter'
        countTry = 0
        while True and countTry <5:
                try:
                    response = requests.post(requestUrl, headers=headersRequest, json=jsonRequest, timeout=90)
                    break
                except:
                    countTry+=1
                    continue
        if response.status_code ==200:
            if len(data:=response.json()['data']) !=0:
                for card in data: 
                    # if card['vendorCode'] not in list(listDoneVendorCode):
                        listDoneVendorCode.append(card['vendorCode'])
                    # a = list(listDoneVendorCode)
                    # a



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
            except aiohttp.ClientConnectorError:
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

    