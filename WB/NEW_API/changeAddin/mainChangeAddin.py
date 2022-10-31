from cmath import nan
from itertools import count
from os.path import abspath, join as joinPath, dirname
import pandas
import multiprocessing
import numpy
import requests
import random
import copy
import time
import sys


class AddinChanger():
    def __init__(self,ip, pathToNumenclatures = r'F:\Downloads\report_2022_10_26\tmp.xlsx') -> None:
        self.ip = ip
        self.pathToNumenclatures = pathToNumenclatures
        self.pathToSiliconAddin = joinPath(dirname(__file__),'db',r'ХарактеристикиСиликон.txt')
        self.pathToSiliconHolderAddin = joinPath(dirname(__file__),'db',r'ХарактеристикиКардхолдер.txt')
        self.pathToPrintAddin = joinPath(dirname(__file__),'db',r'ХарактеристикиПринтов.txt')
        self.pathToBarcodeList = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\ШК.txt'
        self.pathToCategories = r'E:\MyProduct\Python\WB\NEW_API\changeAddin\db\cat.txt'
        self.dfNomenclatures = pandas.DataFrame()
        self.dfSiliconAddin = pandas.DataFrame()
        self.dfSiliconHolderAddin = pandas.DataFrame()
        self.dfPrintAddin = pandas.DataFrame()
        self.dfBarcod = pandas.DataFrame()
        self.listForChange = pandas.DataFrame()
        self.dfCategories = pandas.DataFrame()
        self.barcodeForChange =[]
        self.listChangedCardsPath = joinPath(dirname(__file__),'listChangedCards.txt')
        self.listChangedCards = self.getlistChangedCardsFromFile()
        self.listChangedCardsForUploads = []
        self.createDataFrame()
        self.sortNomenclatures()
        self.urlGetCards = 'https://suppliers-api.wildberries.ru/content/v1/cards/filter'
        self.urlChangeCards = 'https://suppliers-api.wildberries.ru/content/v1/cards/update'
        if ip =='Караханян':
            self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
        elif ip =='Абраамян':
            self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'   
        elif ip =='Самвел':
            self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
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
                'Тип чехлов': 3,
                'Повод': 3,
                'Материал изделия': 3,
            }
    
    def stuffSotr(self):
        pass


    def getlistChangedCardsFromFile(self):
        # try:
            with open(self.listChangedCardsPath, 'r', encoding='utf-8') as listChangedCardsFile:
                return listChangedCardsFile.read().split('\n')
        # except:
        #     return []


    # def applySelf(self, addin):
    #     if addin == 'dfSiliconAddin':
    #         self.dfSiliconAddin = pandas.DataFrame(pandas.read_csv(self.pathToSiliconAddin,sep='\t'))
    #     if addin == 'dfSiliconHolderAddin':
    #         self.dfSiliconHolderAddin = pandas.DataFrame(pandas.read_csv(self.pathToSiliconHolderAddin,sep='\t'))
    #     if addin == 'dfPrintAddin':
    #         self.dfSilicdfPrintAddinonAddin = pandas.DataFrame(pandas.read_csv(self.pathToPrintAddin,sep='\t'))
    #     if addin == 'dfBarcod':
    #         self.dfBarcod = pandas.DataFrame(pandas.read_csv(self.pathToBarcodeList,sep='\t'))
    #     if addin == 'dfNomenclatures':
    #         self.dfBarcod = pandas.DataFrame(pandas.read_csv(self.pathToNumenclatures,sep='\t'))    


    def createDataFrame(self):
        # pool = multiprocessing.Pool(5)
        # for i in ['dfBarcod', 'dfPrintAddin', 'dfSiliconHolderAddin', 'dfSiliconAddin', 'dfNomenclatures']:
        #     pool.apply_async(self.applySelf, args=(i,))
        # pool.close()
        # pool.join()

        self.dfSiliconAddin = pandas.DataFrame(pandas.read_csv(self.pathToSiliconAddin,sep='\t',na_values=''))
        self.dfSiliconHolderAddin = pandas.DataFrame(pandas.read_csv(self.pathToSiliconHolderAddin,sep='\t',na_values=''))
        self.dfPrintAddin = pandas.DataFrame(pandas.read_csv(self.pathToPrintAddin,sep='\t',na_values=''))
        self.dfBarcod = pandas.DataFrame(pandas.read_csv(self.pathToBarcodeList,sep='\t',na_values=''))
        try:
            self.dfNomenclatures = pandas.DataFrame(pandas.read_csv(self.pathToNumenclatures,sep='\t',na_values=''))
        except:
            self.dfNomenclatures = pandas.DataFrame(pandas.read_excel(self.pathToNumenclatures,na_values=''))
        self.dfCategories = pandas.DataFrame(pandas.read_csv(self.pathToCategories,sep='\t',na_values=''))        


    def sortNomenclatures(self):
        # self.barcodeForChange = self.dfBarcod[self.dfBarcod['Характеристика'].str.contains("Принт", na = False)]['Штрихкод'].values.tolist()
        self.barcodeForChange = self.dfBarcod[self.dfBarcod['Характеристика'].str.contains("Принт", na = False)]
        self.barcodeForChange = self.barcodeForChange[self.barcodeForChange['Номенклатура'].str.contains("силикон ", na = False)]
        self.barcodeForChange = self.barcodeForChange[self.barcodeForChange['Характеристика'] != '(Принт 0)']
        self.dfNomenclatures['Баркод'] = self.dfNomenclatures['Баркод'].fillna(0.0).apply(numpy.int64)
        # self.listForChange = self.dfNomenclatures[self.dfNomenclatures['Баркод'].isin(self.barcodeForChange)]
        self.listForChange = pandas.merge(self.dfNomenclatures, self.barcodeForChange, how='inner',left_on='Баркод',right_on='Штрихкод')
        self.listForChange = pandas.merge(self.listForChange, self.dfPrintAddin, how='inner',left_on='Характеристика',right_on='Принт')
        self.listForChange = pandas.merge(self.listForChange, self.dfCategories, how='inner',left_on='Принт',right_on='Принт')
        # self.listForChange = pandas.merge(self.listForChange, self.dfPrintAddin, how='left',left_on='Категория',right_on='Категория')
        self.listForChange.sort_values('Номенклатура',inplace=True)
        self.listForChange.fillna('')
        # self.listForChange.to_excel(r'E:\listForChange.xlsx')
        


    def getCardsNumenclatures(self, listVendorCodeForGet):
        jsonRequest = {
          "vendorCodes": listVendorCodeForGet
        }
        headersRequest = {'Authorization': '{}'.format(self.token)}
        countTry = 0
        while True and countTry < 100:
            try:
                responce = requests.post(self.urlGetCards, json=jsonRequest, headers=headersRequest, timeout=30)
            except ConnectionError:
                countTry+=1
                continue
            except:
                countTry+=1
                continue
            if responce.status_code == 200:
                data = responce.json()['data']
                if len(data) ==0:
                    countTry +=1
                    continue
                return data
            else:
                countTry+=1
                continue
        print('errors getCard')
        with open(joinPath(dirname(__file__),'errors.txt'), 'a') as errorsFile:
                for i in listVendorCodeForGet:
                    errorsFile.write(i + '\n')


    def getRandomValue(self, category, field, caseName):
        valueList = []
        if 'под карту' in caseName:
            listVariation = self.dfSiliconHolderAddin[self.dfSiliconHolderAddin.Категория == category][field].values.tolist()[0].split(';')
        else:
            listVariation = self.dfSiliconAddin[self.dfSiliconAddin.Категория == category][field].values.tolist()[0].split(';')
        try:
            listVariation.remove('').remove(' ')
        except ValueError:
            pass
        countVariation = len(listVariation)
        if countVariation >= self.countValueInField[field]:
            while len(valueList) < self.countValueInField[field]:
                value = random.choice(listVariation).strip()
                if value not in valueList:
                    valueList.append(value)
        else:
            valueList.extend(listVariation)
        return valueList

    def getEquipmentCase(self, category, caseName, model):
        if 'под карту' in caseName:
            equipmentCasePrefix = random.choice(self.dfSiliconHolderAddin[self.dfSiliconHolderAddin.Категория == category]['Комплектация (префикс)'].values.tolist()[0].split(';')).strip()
        else:
            equipmentCasePrefix = random.choice(self.dfSiliconAddin[self.dfSiliconAddin.Категория == category]['Комплектация (префикс)'].values.tolist()[0].split(';')).strip()

        # equipmentCasePrefix = random.choice(self.dfAddinFromFile[self.dfAddinFromFile.Категория == category]['Комплектация (префикс)'].values.tolist()[0].split(';')).strip()
        if model != '':
            return equipmentCasePrefix + ' ' + random.choice(model) + ' 1 штука'
        else:
            return 'Чехол для телефона 1 штука'


    def getName(self, category, caseName, model, countTry=0):
        if 'под карту' in caseName:
            nameCasePrefix = random.choice(self.dfSiliconHolderAddin[self.dfSiliconHolderAddin.Категория == category]['Наименование (префикс)'].values.tolist()[0].split(';')[0:2]).strip()
        else:
            nameCasePrefix = random.choice(self.dfSiliconAddin[self.dfSiliconAddin.Категория == category]['Наименование (префикс)'].values.tolist()[0].split(';')[0:2]).strip()
        #nameCasePrefix = random.choice(self.dfAddinFromFile[self.dfAddinFromFile.Категория == category]['Наименование (префикс)'].values.tolist()[0].split(';')).strip()
        if model != '':
            nameCase = nameCasePrefix + ' ' + random.choice(model)
        else:
            return 'Чехол для телефона'
        if countTry > 10:
            return 'Чехол для телефона'
        if len(nameCase) > 40:
            countTry+=1
            return self.getName(category, caseName, model,countTry)
        else:
             return nameCase


    def getDescription(self, category, caseName, compatibility):
        if 'под карту' in caseName:
            description = random.choice(self.dfSiliconHolderAddin[self.dfSiliconHolderAddin.Категория == category]['Описание'].values.tolist()).strip()
        else:
            description = random.choice(self.dfSiliconAddin[self.dfSiliconAddin.Категория == category]['Описание'].values.tolist()).strip()
        # description = random.choice(self.dfAddinFromFile[self.dfAddinFromFile.Категория == category]['Описание'].values.tolist()).strip()
        countReplace = description.count('***')
        if compatibility != '':
            for i in range(countReplace):
                try:
                    description = description.replace('***',compatibility[i],1)
                except IndexError:
                    description = description.replace('***',compatibility[0],1)
            return description
        else:
            return description.replace('***',"смартфона")


    def changelistCard(self, listCardForCanges):
        for i, card in enumerate(listCardForCanges):
            print(card['vendorCode'])
            try:
                category = self.listForChange[self.listForChange['Артикул поставщика'] == card['vendorCode']]['Категория'].values.tolist()[0]
            except IndexError:
                continue
            caseName = self.listForChange[self.listForChange['Артикул поставщика'] == card['vendorCode']]['Номенклатура'].values.tolist()[0]
            # characteristicsOld = copy.deepcopy(card['characteristics'])
            model = ''
            compatibility = ''
            fabric = ''
            # for char in card['characteristics']:
            #     if 'Модель' in char:
            #         model = char['Модель']
            #     if 'Совместимость' in char:
            #         compatibility = char['Совместимость']
            # if model != '':
            #     fabric = model[0].split(' ')[0]
            model = 'Tecno Camon 19 Neo;Camon 19 Neo;Техно Камон 19 Нео'.split(';')
            compatibility = 'Tecno Camon 19 Neo;Camon 19 Neo;Техно Камон 19 Нео;Камон 19 Нео'.split(';')
            fabric = 'Tecno'
            # for char in card['characteristics']:
            #     if 'Модель' in char:
            #         model = char['Модель']
            #     if 'Совместимость' in char:
            #         compatibility = char['Совместимость']
            # if model != '':
            #     fabric = model[0].split(' ')[0]
            card['characteristics'] =[
                            {'Рисунок': [self.listForChange[self.listForChange['Артикул поставщика'] == card['vendorCode']]['Рисунок'].values.tolist()[0]]},
                            {'Цвет': [self.listForChange[self.listForChange['Артикул поставщика'] == card['vendorCode']]['Цвет'].values.tolist()[0]]},
                            {'Тип чехлов': self.getRandomValue(category, 'Тип чехлов', caseName)},
                            {'Повод': [self.listForChange[self.listForChange['Артикул поставщика'] == card['vendorCode']]['Повод'].values.tolist()[0]]},
                            {'Особенности чехла': self.getRandomValue(category, 'Особенности чехла', caseName)},
                            {'Комплектация': self.getEquipmentCase(category, caseName, model)},
                            {'Модель': model},
                            {'Вид застежки': self.getRandomValue(category, 'Вид застежки', caseName)},
                            {'Декоративные элементы': [self.listForChange[self.listForChange['Артикул поставщика'] == card['vendorCode']]['Декоративные элементы'].values.tolist()[0]]},
                            {'Совместимость': compatibility},
                            {'Назначение подарка': [self.listForChange[self.listForChange['Артикул поставщика'] == card['vendorCode']]['Назначение подарка'].values.tolist()[0]]},
                            {'Любимые герои': [self.listForChange[self.listForChange['Артикул поставщика'] == card['vendorCode']]['Любимые герои'].values.tolist()[0]]},
                            {'Материал изделия': self.getRandomValue(category, 'Материал изделия', caseName)},
                            {'Производитель телефона': fabric},
                            {'Бренд': 'Mobi711'},
                            {'Страна производства': 'Китай'},
                            {'Наименование': self.getName(category, caseName, model)},
                            {'Предмет':'Чехлы для телефонов'},
                            {'Описание': self.getDescription(category, caseName, compatibility)},
                            {'Высота упаковки': 18.5},
                            {'Ширина упаковки': 11},
                            {'Длина упаковки': 1.5}
                        ]
            card
        self.listChangedCardsForUploads = listCardForCanges


    def pushChanges(self):
        headersRequest = {'Authorization': '{}'.format(self.token)}
        countTry = 0
        
        while True and countTry < 10:
            try:
                responce = requests.post(self.urlChangeCards, json=self.listChangedCardsForUploads, headers=headersRequest, timeout=50)
                if responce.status_code == 200:
                    break
                else:
                    countTry+=1
                    continue
            except ConnectionError:
                time.sleep(5)
                responce = requests.post(self.urlChangeCards, json=self.listChangedCardsForUploads, headers=headersRequest, timeout=3)
            except requests.exceptions.InvalidJSONError:
                print('ValeuError')
                pd = pandas.DataFrame(self.listChangedCardsForUploads)
                pd.to_excel(joinPath(dirname(__file__),'errors.xlsx'))
            except:
                time.sleep(5)
                countTry+=1
                continue
        # except:
        #     with open(joinPath(dirname(__file__),'erreos.txt'), 'a') as errorsFile:
        #         for i in self.listChangedCardsForUploads:
        #             errorsFile.write(i['vendorCode'] + '\n')
        # self.listChangedCards.extend(listVendorCodeForCanges)
        with open(self.listChangedCardsPath, 'a', encoding='utf-8') as listChangedCardsFile:
            for card in self.listChangedCardsForUploads:
                listChangedCardsFile.write(card['vendorCode'] + '\n')
                self.listChangedCards.append(card['vendorCode'])
            listChangedCardsFile.close()
        # a = responce.json()
        # a



    def cangeCardsNumenclatures(self):
        listForChange = self.listForChange['Артикул поставщика'].values.tolist()
        listVendorCodeForCanges = []
        for vendorCode in listForChange:
            if vendorCode not in self.listChangedCards:
                listVendorCodeForCanges.append(vendorCode)
                if len(listVendorCodeForCanges)>90:
                    listCardForCanges = self.getCardsNumenclatures(listVendorCodeForCanges)
                    listCardForCangesNew = []
                    for card in listCardForCanges:
                        if card['vendorCode'] not in self.listChangedCards:
                            listCardForCangesNew.append(card)
                    for i in range(0,len(listCardForCangesNew), 100):
                        start_time = time.time()
                        self.changelistCard(listCardForCangesNew[i:i+100])
                        self.pushChanges()
                        print("--- %s seconds ---" % (time.time() - start_time))
                    listVendorCodeForCanges = []
                    
            #listCardForCanges = self.getCardsNumenclatures(self.listForChange['Артикул поставщика'].values.tolist()[i:i+100])
            # start_time = time.time()
        listCardForCanges = self.getCardsNumenclatures(listVendorCodeForCanges)
        self.changelistCard(listCardForCanges)
        self.pushChanges()
        print("--- %s seconds ---" % (time.time() - start_time))






if __name__=='__main__':
    ip = 'Абраамян' #sys.argv[1]
    path = r'F:\Downloads\report_2022_10_26\Tecno_Camon_19_Neo.xlsx'#sys.argv[2]
    changer = AddinChanger(ip, path)
    changer.cangeCardsNumenclatures()