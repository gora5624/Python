from operator import imod
from os.path import join as joinPath, abspath
from os import listdir
import re
from sqlitedict import SqliteDict
import pandas
import multiprocessing
import random


class ModelWithAddin:
    def __init__(self, brand, compatibility, modelAddin, price, maskFolderName, pathToDoneSiliconImageSilicon, siliconCaseColorDict) -> None:
        # self.colorList = []
        # self.cameraType = cameraType
        # self.model = model
        self.brand = brand
        self.compatibility = compatibility
        # self.name = name
        self.modelAddin = modelAddin
        self.price = price
        self.TNVED = '3926909709'
        self.pathToMask = joinPath(pathToDoneSiliconImageSilicon, maskFolderName)
        # self.caseType = caseType
        self.listJsonForUpdateToWB = []
        self.siliconCaseColorDict = siliconCaseColorDict
        self.maskFolderName = maskFolderName
        self.dfAddinFromFile = pandas.DataFrame(pandas.read_excel(r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиКардхолдер.xlsx'))
        self.dfCategoryPrint = pandas.DataFrame(pandas.read_excel(r'E:\MyProduct\Python\WB\MakePrint\cat.xlsx'))
        self.data = []
        self.countValueInField ={
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
            }

        self.applyAddin()


    def getColor(self):
        for color, code in self.siliconCaseColorDict.items():
            if color in self.maskFolderName:
                if color == 'проз':
                    return 'прозрачный'
                return color


    def getName(self, category, countTry=0):
        nameCasePrefix = random.choice(self.dfAddinFromFile[self.dfAddinFromFile.Категория == category]['Наименование (префикс)'].values.tolist()[0].split(';')).strip()
        nameCase = nameCasePrefix + ' ' + random.choice(self.modelAddin.split(';'))
        if countTry > 50:
            return 'Невозможно сгенерить имя для {}'.format(self.modelAddin)
        if len(nameCase) > 40:
            countTry+=1
            return self.getName(category, countTry)
        else:
             return nameCase


    def getVendorCode(self, colorCase, categoryCode, printName):
        if 'силикон с' in self.maskFolderName:
            vendorCode1 = self.maskFolderName.replace('Чехол','').split('силикон')[0].strip().replace(' ','_') + '_BP'
            if 'с зак.кам.' in self.maskFolderName:
                vendorCode2 = 'CCM'
            elif 'с отк.кам.' in self.maskFolderName:
                vendorCode2 = 'OCM'
            else:
                vendorCode2 = 'UCM'
            for color, codeColor in self.siliconCaseColorDict.items():
                if color == colorCase:
                    vendorCode3 = codeColor
                    break
            else:
                vendorCode3 = 'UNKNOW_COLOR'
            if 'под карту' in self.maskFolderName:
                vendorCode3 += '_HLD'
            return '_'.join([vendorCode1, vendorCode2, vendorCode3,
                        categoryCode, 'PRNT',printName.replace('(Принт ','').replace(')','')])


    def getDescription(self, category):
        description = random.choice(self.dfAddinFromFile[self.dfAddinFromFile.Категория == category]['Описание'].values.tolist()).strip()
        countReplace = description.count('***')
        for i in range(countReplace):
            try:
                description = description.replace('***',self.compatibility.split(';')[i],1)
            except IndexError:
                description = description.replace('***',self.compatibility.split(';')[0],1)
        return description


    def getEquipmentCase(self, category):
        equipmentCasePrefix = random.choice(self.dfAddinFromFile[self.dfAddinFromFile.Категория == category]['Комплектация (префикс)'].values.tolist()[0].split(';')).strip()
        return equipmentCasePrefix + ' ' + random.choice(self.modelAddin.split(';')) + ' 1 штука'


    def getRandomValue(self, category, field):
        valueList = []
        listVariation = self.dfAddinFromFile[self.dfAddinFromFile.Категория == category][field].values.tolist()[0].split(';')
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
        return ';'.join(valueList)


    def chekCountField(self, field, values):
        maxCount = self.countValueInField[field]
        return ';'.join(values.split(';')[0:maxCount])





    def applyAddin(self):
        # def getAddinFromFile():
        #     dfAddinFromFile = multiprocessing.Process(target=pandas.read_excel, args=(r'E:\MyProduct\Python\WB\MakePrint\Характеристики.xlsx',))

        # def getCategory():
        #     dfCategoryPrint = pandas.read_excel(r'E:\MyProduct\Python\WB\MakePrint\cat.xlsx')

        # dfAddinFromFile = pandas.DataFrame(pandas.read_excel(r'E:\MyProduct\Python\WB\MakePrint\Характеристики.xlsx'))
        # dfCategoryPrint = pandas.DataFrame(pandas.read_excel(r'E:\MyProduct\Python\WB\MakePrint\cat.xlsx'))
        # data = []
        listCategory = self.dfCategoryPrint['Категория'].unique().tolist()
        for pictures in listdir(self.pathToMask):
            printName = pictures[0:-4]
            currentPictureCategoryList = self.dfCategoryPrint[self.dfCategoryPrint.Принт == printName]#['Категория'].values.tolist()
            for categoryData in currentPictureCategoryList.values:
                category = categoryData[1]
                categoryCode = categoryData[2]
                color = self.getColor()
                datapicture = {
                            'Номер карточки': listCategory.index(category),
                            'Категория': category,
                            'Цвет': color,
                            'Баркод товара': '',
                            'Бренд': 'Mobi711',
                            'Наименование': self.getName(category),
                            'Цена': '399',
                            'Артикул товара': self.getVendorCode(color, categoryCode, printName),
                            'Описание': self.getDescription(category),
                            'Производитель телефона': 'Apple',
                            'Назначение подарка': self.getRandomValue(category, 'Назначение подарка'),
                            'Комплектация': self.getEquipmentCase(category),
                            'Особенности чехла': self.getRandomValue(category, 'Особенности чехла'),
                            'Вид застежки': self.getRandomValue(category, 'Вид застежки'),
                            'Рисунок': self.getRandomValue(category, 'Рисунок'),
                            'Любимые герои': self.getRandomValue(category, 'Любимые герои'),
                            'Совместимость': self.chekCountField('Совместимость',self.compatibility),
                            'Тип чехлов': self.getRandomValue(category, 'Тип чехлов'),
                            'Модель': self.chekCountField('Модель',self.modelAddin),
                            'Повод': self.getRandomValue(category, 'Повод'),
                            'Страна производства': 'Китай',
                            'Декоративные элементы': self.getRandomValue(category, 'Декоративные элементы'),
                            'Материал изделия': 'Силикон; ТПУ; Полиуретан',
                            'Высота упаковки': 18.5,
                            'Ширина упаковки': 11,
                            'Глубина упаковки': 1.5,
                            'Медиафайлы': r'http://95.78.233.163:8001/wp-content/uploads/Готовые принты/Силикон/{}/{}'.format(self.maskFolderName, pictures)
                        }
                

                self.data.append(datapicture)


    # def setDescriptionCase(seft, dfAddinFromFile):
    #     pass


    @staticmethod
    def pushToDB(pathToFileWithAddin, sqlFile=joinPath(abspath(__file__),'..',"cache.sqlite3")):
        # try:
        #     with SqliteDict(cache_file) as mydict:
        #         mydict[key] = value
        #         mydict.commit()
        # except Exception as ex:
        #     print("Error during storing data (Possibly unsupported):", ex)         

        addinCategory = SqliteDict(sqlFile, tablename=addinCategory, autocommit=True)   
        df = pandas.read_excel(pathToFileWithAddin)
        for data in df:
            data

    @staticmethod
    def readFromDB():
        pass


            # data = {
            #     'Номер карточки': cardNumber,
            #     'Категория': categoryCase,
            #     'Цвет': colorCase,
            #     'Баркод товара': barcodeCase,
            #     'Бренд': brandCase,
            #     'Наименование': nameCaseCase,
            #     'Цена': priceCase,
            #     'Артикул товара': articleCase,
            #     'Описание': descriptionCase,
            #     'Производитель телефона': madeByCase,
            #     'Назначение подарка': destenitionGiftCase,
            #     'Комплектация': equipmentCase,
            #     'Особенности чехла': specialCase,
            #     'Вид застежки': claspCase,
            #     'Рисунок': pictureCase,
            #     'Любимые герои': heroesCase,
            #     'Совместимость': compatibilityCase,
            #     'Тип чехлов': typeCase,
            #     'Модель': modelCase,
            #     'Повод': occasinCase,
            #     'Страна производства': countryManufactureCase,
            #     'Декоративные элементы': decorationCase,
            #     'Материал изделия': materialsCase,
            #     'Медиафайлы': pictureURLCase
            # }
if __name__ == '__main__':
    pass
    # ModelWithAddin.pushToDB(r'C:\Users\Георгий\Downloads\Характеристики.xlsx')