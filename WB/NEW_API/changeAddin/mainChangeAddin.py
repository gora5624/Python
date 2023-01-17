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
        self.pathToSiliconCLRAddin = joinPath(dirname(__file__),'db',r'ХарактеристикиСиликонПроз.txt')
        self.pathToSiliconMTAddin = joinPath(dirname(__file__),'db',r'ХарактеристикиСиликонМат.txt')
        self.pathToBookAddin = joinPath(dirname(__file__),'db',r'ХарактеристикиКнижки.txt')
        self.pathToSiliconHolderAddin = joinPath(dirname(__file__),'db',r'ХарактеристикиКардхолдер.txt')
        self.pathToPrintAddin = joinPath(dirname(__file__),'db',r'ХарактеристикиПринтов.txt')
        self.pathToBarcodeList = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\ШК.txt'
        self.pathToCategories = joinPath(dirname(__file__),'db' r'\cat.txt')
        self.dfNomenclatures = pandas.DataFrame()
        self.dfSiliconCLRAddin = pandas.DataFrame()
        self.dfSiliconMTAddin = pandas.DataFrame()
        self.dfSiliconHolderAddin = pandas.DataFrame()
        self.dfPrintAddin = pandas.DataFrame()
        self.dfBarcod = pandas.DataFrame()
        self.listForChange = pandas.DataFrame()
        self.dfCategories = pandas.DataFrame()
        self.barcodeForChange =[]
        self.listChangedCardsPath = joinPath(dirname(__file__),'listChangedCards.txt')
        self.listChangedCards = self.getlistChangedCardsFromFile()
        self.listChangedCardsForUploads = []
        self.listForChangeDict = {}
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

        self.dfSiliconCLRAddin = pandas.DataFrame(pandas.read_csv(self.pathToSiliconCLRAddin,sep='\t',na_values=''))
        self.dfSiliconMTAddin = pandas.DataFrame(pandas.read_csv(self.pathToSiliconMTAddin,sep='\t',na_values=''))
        self.dfSiliconCLRAddinDict = self.dfSiliconCLRAddin.to_dict('records')
        self.dfSiliconMTAddinDict = self.dfSiliconMTAddin.to_dict('records')
        self.dfBookAddin = pandas.DataFrame(pandas.read_csv(self.pathToBookAddin,sep='\t',na_values=''))
        self.dfBookAddinDict = self.dfBookAddin.to_dict('records')
        self.dfSiliconHolderAddin = pandas.DataFrame(pandas.read_csv(self.pathToSiliconHolderAddin,sep='\t',na_values=''))
        self.dfSiliconHolderAddinDict = self.dfSiliconHolderAddin.to_dict('records')
        self.dfPrintAddin = pandas.DataFrame(pandas.read_csv(self.pathToPrintAddin,sep='\t',na_values=''))
        self.dfBarcod = pandas.DataFrame(pandas.read_csv(self.pathToBarcodeList,sep='\t',na_values=''))
        if '.xlsx' not in self.pathToNumenclatures:
            self.dfNomenclatures = pandas.DataFrame(pandas.read_csv(self.pathToNumenclatures,sep='\t',na_values=''))
        else:
            self.dfNomenclatures = pandas.DataFrame(pandas.read_excel(self.pathToNumenclatures,na_values=''))
        self.dfCategories = pandas.DataFrame(pandas.read_csv(self.pathToCategories,sep='\t',na_values=''))        


    def sortNomenclatures(self):
        # self.barcodeForChange = self.dfBarcod[self.dfBarcod['Характеристика'].str.contains("Принт", na = False)]['Штрихкод'].values.tolist()
        # self.barcodeForChange = self.dfBarcod[self.dfBarcod['Характеристика'].str.contains("Принт", na = False)]
        # self.barcodeForChange = self.barcodeForChange[self.barcodeForChange['Номенклатура'].str.contains("силикон", na = False)]
        # self.barcodeForChange = self.barcodeForChange[self.barcodeForChange['Характеристика'] != '(Принт 0)']
        self.barcodeForChange = self.dfBarcod
        self.dfNomenclatures['sku'] = self.dfNomenclatures['sku'].fillna(0.0).apply(numpy.int64)
        # self.listForChange = self.dfNomenclatures[self.dfNomenclatures['Баркод'].isin(self.barcodeForChange)]
        self.listForChange = pandas.merge(self.dfNomenclatures, self.barcodeForChange, how='inner',left_on='sku',right_on='Штрихкод')
        self.listForChange = pandas.merge(self.listForChange, self.dfPrintAddin, how='inner',left_on='Характеристика_x',right_on='Принт')
        self.listForChange = pandas.merge(self.listForChange, self.dfCategories, how='inner',left_on='Принт',right_on='Принт')
        # self.listForChange = pandas.merge(self.listForChange, self.dfPrintAddin, how='left',left_on='Категория',right_on='Категория')
        self.listForChange = self.dfNomenclatures
        self.listForChange.sort_values('vendorCode',inplace=True)
        self.listForChange.fillna('')
        self.listForChangeDictTMP = self.listForChange.to_dict('records')
        for line in self.listForChangeDictTMP:
            #if line['Артикул поставщика'] not in self.listChangedCards:
                tmp = {line['vendorCode']:line}
                self.listForChangeDict.update(tmp)
        self.listForChange
        # i = 0
        # for j in numpy.array_split(self.listForChange, len(self.listForChange)//500000):
        #     j.to_excel(joinPath(r'E:\\','listForChangeSplit_{}.xlsx'.format(i)), index=False)
        #     i+=1
        # self.listForChange.to_excel(r'E:\listForChange.xlsx')
        # self.listForChange = pandas.DataFrame(pandas.read_excel(r'E:\listForChangeКар.xlsx'))
        # self.listForChangeDictTMP = self.listForChange.to_dict('records')
        # for line in self.listForChangeDictTMP:
        #     #if line['Артикул поставщика'] not in self.listChangedCards:
        #         tmp = {line['Артикул поставщика']:line}
        #         self.listForChangeDict.update(tmp)

        self.listForChangeDict
        i = 0
        # filepath = input('Введите пусть к файлу: ')
        # df = pandas.DataFrame(pandas.read_excel(filepath))
        # for j in numpy.array_split(self.listForChange, len(self.listForChange)//500000):
        #     j.to_excel('E:\listForChange{}.xlsx'.format(i), index=False)
        #     i+=1
        self.listForChange.to_excel(r'E:\listForChange.xlsx')

        self.listForChange
        


    def getCardsNumenclatures(self, listVendorCodeForGet):
        jsonRequest = {
          "vendorCodes": listVendorCodeForGet
        }
        headersRequest = {'Authorization': '{}'.format(self.token)}
        countTry = 0
        while True and countTry < 100:
            try:
                responce = requests.post(self.urlGetCards, json=jsonRequest, headers=headersRequest, timeout=120)
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
            for line in self.dfSiliconHolderAddinDict:
                if line['Категория'] == category:
                    listVariation = line[field].split(';')
            # listVariation = self.dfSiliconHolderAddin[self.dfSiliconHolderAddin.Категория == category][field].values.tolist()[0].split(';')
        elif 'книга' in caseName:
            for line in self.dfBookAddinDict:
                if line['Категория'] == category:
                    listVariation = line[field].split(';')
        elif 'силикон ' in caseName and 'проз' in caseName:
            for line in self.dfSiliconCLRAddinDict:
                if line['Категория'] == category:
                    listVariation = line[field].split(';')
        elif 'силикон ' in caseName and 'блестки' in caseName:
            for line in self.dfSiliconCLRAddinDict:
                if line['Категория'] == category:
                    listVariation = line[field].split(';')
        elif 'силикон ' in caseName and 'Skin' in caseName:
            for line in self.dfSiliconCLRAddinDict:
                if line['Категория'] == category:
                    listVariation = line[field].split(';')
        elif 'силикон ' in caseName and 'мат' in caseName:
            for line in self.dfSiliconMTAddinDict:
                if line['Категория'] == category:
                    listVariation = line[field].split(';')
        elif 'силикон ' in caseName and 'блестки' in caseName:
             for line in self.dfSiliconCLRAddinDict:
                if line['Категория'] == category:
                    listVariation = line[field].split(';')
           #  listVariation = self.dfSiliconAddin[self.dfSiliconAddin.Категория == category][field].values.tolist()[0].split(';')
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
            for line in self.dfSiliconHolderAddinDict:
                if line['Категория'] == category:
                    equipmentCasePrefix = random.choice(line['Комплектация (префикс)'].split(';')).strip()
            # equipmentCasePrefix = random.choice(self.dfSiliconHolderAddin[self.dfSiliconHolderAddin.Категория == category]['Комплектация (префикс)'].values.tolist()[0].split(';')).strip()
        elif 'книга' in caseName:
            for line in self.dfBookAddinDict:
                if line['Категория'] == category:
                    equipmentCasePrefix = random.choice(line['Комплектация (префикс)'].split(';')).strip()
        elif 'силикон ' in caseName and 'проз' in caseName:
            for line in self.dfSiliconCLRAddinDict:
                if line['Категория'] == category:
                    equipmentCasePrefix = random.choice(line['Комплектация (префикс)'].split(';')).strip()
        elif 'силикон ' in caseName and 'блестки' in caseName:
            for line in self.dfSiliconCLRAddinDict:
                if line['Категория'] == category:
                    equipmentCasePrefix = random.choice(line['Комплектация (префикс)'].split(';')).strip()
        elif 'силикон ' in caseName and 'Skin' in caseName:
            for line in self.dfSiliconCLRAddinDict:
                if line['Категория'] == category:
                    equipmentCasePrefix = random.choice(line['Комплектация (префикс)'].split(';')).strip()
        elif 'силикон ' in caseName and 'мат' in caseName:
            for line in self.dfSiliconMTAddinDict:
                if line['Категория'] == category:
                    equipmentCasePrefix = random.choice(line['Комплектация (префикс)'].split(';')).strip()
            # equipmentCasePrefix = random.choice(self.dfSiliconAddin[self.dfSiliconAddin.Категория == category]['Комплектация (префикс)'].values.tolist()[0].split(';')).strip()

        # equipmentCasePrefix = random.choice(self.dfAddinFromFile[self.dfAddinFromFile.Категория == category]['Комплектация (префикс)'].values.tolist()[0].split(';')).strip()
        if model != '':
            return equipmentCasePrefix + ' ' + random.choice(model) + ' 1 штука'
        else:
            return 'Чехол для телефона 1 штука'


    def getName(self, category, caseName, modelList, countTry=0):
        if 'под карту' in caseName:
            for line in self.dfSiliconHolderAddinDict:
                if line['Категория'] == category:
                    nameCasePrefix = random.choice(line['Наименование (префикс)'].split(';')).strip()
            # nameCasePrefix = random.choice(self.dfSiliconHolderAddin[self.dfSiliconHolderAddin.Категория == category]['Наименование (префикс)'].values.tolist()[0].split(';')[0:2]).strip()
        if 'книга' in caseName:
            for line in self.dfBookAddinDict:
                if line['Категория'] == category:
                    nameCasePrefix = random.choice(line['Наименование (префикс)'].split(';')).strip()
        elif 'силикон ' in caseName and 'проз' in caseName:
            for line in self.dfSiliconCLRAddinDict:
                if line['Категория'] == category:
                    nameCasePrefix = random.choice(line['Наименование (префикс)'].split(';')).strip()
        elif 'силикон ' in caseName and 'блестки' in caseName:
            for line in self.dfSiliconCLRAddinDict:
                if line['Категория'] == category:
                    nameCasePrefix = random.choice(line['Наименование (префикс)'].split(';')).strip()
        elif 'силикон ' in caseName and 'Skin' in caseName:
            for line in self.dfSiliconCLRAddinDict:
                if line['Категория'] == category:
                    nameCasePrefix = random.choice(line['Наименование (префикс)'].split(';')).strip()
        elif 'силикон ' in caseName and 'мат' in caseName:
            for line in self.dfSiliconMTAddinDict:
                if line['Категория'] == category:
                    nameCasePrefix = random.choice(line['Наименование (префикс)'].split(';')).strip()
            # nameCasePrefix = random.choice(self.dfSiliconAddin[self.dfSiliconAddin.Категория == category]['Наименование (префикс)'].values.tolist()[0].split(';')[0:2]).strip()
        #nameCasePrefix = random.choice(self.dfAddinFromFile[self.dfAddinFromFile.Категория == category]['Наименование (префикс)'].values.tolist()[0].split(';')).strip()
        if modelList != '':
            for model in modelList:
                nameCase = nameCasePrefix + ' ' + model
                if len(nameCase) <= 60:
                    return nameCase
                else:
                    continue
            # nameCase = nameCasePrefix + ' ' + random.choice(model)
        else:
            return 'Чехол для телефона'
        # if countTry > 10:
        #     return 'Чехол для телефона'
        # if len(nameCase) > 40:
        #     countTry+=1
        #     return self.getName(category, caseName, model,countTry)
        # else:
        #      return nameCase


    def getDescription(self, category, caseName, compatibility):
        if 'под карту' in caseName:
            for line in self.dfSiliconHolderAddinDict:
                if line['Категория'] == category:
                    description = random.choice(line['Описание'].split(';')).strip()
            # description = random.choice(self.dfSiliconHolderAddin[self.dfSiliconHolderAddin.Категория == category]['Описание'].values.tolist()).strip()
        if 'книга' in caseName:
            for line in self.dfBookAddinDict:
                if line['Категория'] == category:
                    description = random.choice(line['Описание'].split(';')).strip()
        elif 'силикон ' in caseName and 'проз' in caseName:
            for line in self.dfSiliconCLRAddinDict:
                if line['Категория'] == category:
                    description = random.choice(line['Описание'].split(';')).strip()
        elif 'силикон ' in caseName and 'блестки' in caseName:
            for line in self.dfSiliconCLRAddinDict:
                if line['Категория'] == category:
                    description = random.choice(line['Описание'].split(';')).strip()
        elif 'силикон ' in caseName and 'Skin' in caseName:
            for line in self.dfSiliconCLRAddinDict:
                if line['Категория'] == category:
                    description = random.choice(line['Описание'].split(';')).strip()
        elif 'силикон ' in caseName and 'мат' in caseName:
            for line in self.dfSiliconMTAddinDict:
                if line['Категория'] == category:
                    description = random.choice(line['Описание'].split(';')).strip()
            # description = random.choice(self.dfSiliconAddin[self.dfSiliconAddin.Категория == category]['Описание'].values.tolist()).strip()
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


    def getCharForlistCardForCangesDict(self, vendorCode):
        line = self.listForChangeDict[vendorCode]
        image = line['Рисунок']
        color = line['Цвет']
        reason = line['Повод'].split(';')
        dekor = line['Декоративные элементы']
        reasonGift = line['Назначение подарка'].split(';')
        heroes = line['Любимые герои']
        return {
            'Рисунок':[image + ' ' + color],
            'Цвет':[color],
            'Повод':reason  ,
            'Декоративные элементы':[dekor],
            'Назначение подарка':reasonGift,
            'Любимые герои':[heroes],
            # 'Совместимость' : line['Модель'].split(';')
            # 'Совместимость' : ['Vivo Y16', 'Y16', "Виво У16", "У16",'Y 16']# line['Модель'].split(';')
        }
        


    def changelistCard(self, listCardForCanges):
        for i, card in enumerate(listCardForCanges):
            print(card['vendorCode'])
            try:
                line = self.listForChangeDict[card['vendorCode']]
            except KeyError:
                continue
            category = line['Категория']
            caseName = line['Номенклатура']

            try: 
                category = self.listForChange[self.listForChange['Артикул поставщика'] == card['vendorCode']]['Категория'].values.tolist()[0]
            except IndexError:
                continue
            caseName = self.listForChange[self.listForChange['Артикул поставщика'] == card['vendorCode']]['Номенклатура'].values.tolist()[0]
            characteristicsOld = copy.deepcopy(card['characteristics'])
            model = ''
            compatibility = ''
            fabric = ''
            for char in card['characteristics']:
                if 'Модель' in char:
                    model = char['Модель']
                if 'Совместимость' in char:
                    compatibility = char['Совместимость']
            if model != '':
                fabric = model[0].split(' ')[0]
            model = 'Realme C30; Реалми С30; Реалме ц30'.split(';')
            compatibility = 'Realme c30; Реалми ц30; Реалме ц30; Realme С30;Реалми с30;Реалми С 30;Реалме С30;Реалме С 30'.split(';')
            fabric = 'Realme'
            for char in card['characteristics']:
                if 'Модель' in char:
                    model = char['Модель']
                if 'Совместимость' in char:
                    compatibility = char['Совместимость']
            if model == '' and compatibility != '':
                model = compatibility[0:3]
            if compatibility == '' and model != '':
                compatibility = model[0:3]
            if model != '':
                fabric = model[0].split(' ')[0]
            addChar = self.getCharForlistCardForCangesDict(card['vendorCode'])
            if 'чехол' in caseName:
                stuff = 'Чехлы для телефонов'
                # stuff = 'Чехлы-книжки для телефонов'
            else:
                stuff = 'Защитные стекла'
            
            compatibility = ['Realmi 8i',"Реалми 8и","Реалме 8и","Realme 8 i"]# addChar['Совместимость']
            model = ['Realmi 8i',"Реалми 8и","Реалме 8и"]# addChar['Совместимость'][0:3]
            fabric = ['Realme']# addChar['Совместимость'][0].split(' ')[0]
            for j in card['characteristics']:
                if 'Предмет' in j:
                    stuff = j['Предмет']
            card['characteristics'] =[
                            {'Рисунок': addChar['Рисунок']},
                            {'Цвет': addChar['Цвет']},
                            {'Тип чехлов': self.getRandomValue(category, 'Тип чехлов', caseName)},
                            {'Повод': addChar['Повод']},
                            {'Особенности чехла': self.getRandomValue(category, 'Особенности чехла', caseName)},
                            {'Комплектация': []},# [self.getEquipmentCase(category, caseName, model)]},
                            {'Модель': []},#model},
                            {'Вид застежки': self.getRandomValue(category, 'Вид застежки', caseName)},
                            {'Декоративные элементы': addChar['Декоративные элементы']},
                            {'Совместимость': []},#compatibility},
                            {'Назначение подарка': addChar['Назначение подарка']},
                            {'Любимые герои': addChar['Любимые герои']},
                            {'Материал изделия': self.getRandomValue(category, 'Материал изделия', caseName)},
                            {'Производитель телефона': fabric},
                            {'Бренд': 'Mobi711'},
                            {'Страна производства': 'Китай'},
                            {'Наименование': 'Товар'},#self.getName(category, caseName, model)},
                            {'Предмет':stuff},
                            {'Описание': 'Товар'},
                            {'Высота упаковки': 19},
                            {'Ширина упаковки': 12},
                            {'Длина упаковки': 2}
                        ]
            card
        return listCardForCanges
        # self.listChangedCardsForUploads = listCardForCanges


    def pushChanges(self, listChangedCardsForUploads):
        headersRequest = {'Authorization': '{}'.format(self.token)}
        countTry = 0
        
        while True and countTry < 10:
            try:
                responce = requests.post(self.urlChangeCards, json=listChangedCardsForUploads, headers=headersRequest, timeout=60)
                if responce.status_code == 200:
                    break
                else:
                    countTry+=1
                    continue
            except ConnectionError:
                time.sleep(5)
                responce = requests.post(self.urlChangeCards, json=listChangedCardsForUploads, headers=headersRequest, timeout=60)
            except requests.exceptions.InvalidJSONError:
                print('ValeuError')
                pd = pandas.DataFrame(listChangedCardsForUploads)
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
            for card in listChangedCardsForUploads:
                listChangedCardsFile.write(card['vendorCode'] + '\n')
                self.listChangedCards.append(card['vendorCode'])
            listChangedCardsFile.close()
        a = responce.json()
        a


    def changelistCardProcess(self, listCardForCangesNew):
        tmp = self.changelistCard(listCardForCangesNew)
        self.pushChanges(tmp)



    def cangeCardsNumenclatures(self):
        start_time = time.time()
        listForChange = self.listForChange['vendorCode'].values.tolist()
        listVendorCodeForCanges = []

        for vendorCode in listForChange:
            listProcess = []
            if vendorCode not in self.listChangedCards:
                listVendorCodeForCanges.append(vendorCode)
                if len(listVendorCodeForCanges)>90:
                    listCardForCanges = self.getCardsNumenclatures(listVendorCodeForCanges)
                    listCardForCangesNew = []
                    for card in listCardForCanges:
                        if card['vendorCode'] not in self.listChangedCards:
                            listCardForCangesNew.append(card)
                    # pool = multiprocessing.Pool()
                    # start_time = time.time()
                    
                    for i in range(0,len(listCardForCangesNew), 100):
                        # start_time = time.time()
                        p = multiprocessing.Process(target=self.changelistCardProcess, args=(listCardForCangesNew[i:i+100],))
                        p.start()
                        listProcess.append(p)
                        # pool.apply_async(self.changelistCardProcess, args=(listCardForCangesNew[i:i+100],))
                        #self.changelistCard(listCardForCangesNew[i:i+100])
                        #self.pushChanges()
                        # print("--- %s seconds ---" % (time.time() - start_time))
                    # pool.close()
                    # pool.join()
                    
                    for card in listCardForCangesNew:
                        if card['vendorCode'] not in self.listChangedCards:
                            self.listChangedCards.append(card['vendorCode'])
                    listVendorCodeForCanges = []
                    
            #listCardForCanges = self.getCardsNumenclatures(self.listForChange['Артикул поставщика'].values.tolist()[i:i+100])
            # start_time = time.time()
        for p in listProcess:
            p.join()
        listCardForCanges = self.getCardsNumenclatures(listVendorCodeForCanges)
        tmp = self.changelistCard(listCardForCanges)
        self.pushChanges(tmp)
        print("--- %s seconds ---" % (time.time() - start_time))






if __name__=='__main__':
    # ip = 'Абраамян'# sys.argv[1]
    # path = r'E:\Downloads\camon_19_neo.xlsx' # sys.argv[2]
    # changer = AddinChanger(ip, path)
    # changer.cangeCardsNumenclatures()
    for item in [('Абраамян', r'C:\Users\Георгий\Desktop\listCardsFromFilter.xlsx')]:
        ip = item[0]
        path = item[1]
        changer = AddinChanger(ip, path)
        changer.cangeCardsNumenclatures()