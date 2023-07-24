from os.path import join as joinPath, abspath,exists
from os import listdir
import requests
import time
from sqlitedict import SqliteDict
import pandas
import multiprocessing
import random


class ModelWithAddin:
    def __init__(self, brand, compatibility, modelAddin, price, maskFolderName, pathToDoneSiliconImageSilicon, siliconCaseColorDict, existsFlag=False, listDataVendorCode='') -> None:
        # self.colorList = []
        # self.cameraType = cameraType
        # self.model = model
        self.brand = brand
        self.vendorCodeList = listDataVendorCode
        self.existsFlag = existsFlag
        self.compatibility = compatibility
        # self.name = name
        self.modelAddin = modelAddin
        self.price = price
        self.TNVED = '3926909709'
        self.pathSiliconImage = joinPath(pathToDoneSiliconImageSilicon, maskFolderName)
        # self.caseType = caseType
        self.listJsonForUpdateToWB = []
        self.siliconCaseColorDict = siliconCaseColorDict
        self.maskFolderName = maskFolderName
        self.pathToSiliconMTAddin = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиСиликонМат.txt'
        self.pathToSiliconCLRAddin = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиСиликонПроз.txt'
        self.pathToPlasticAddin = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиПластик.txt'
        self.pathToBookAddin = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиКнижки.txt'
        self.pathToCardhonlderAddin = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиКардхолдер.txt'
        self.pathToSkinShellAddin = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиSkinShell.txt'
        self.pathToSkinShellAddin = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиSkinShellNew.txt'
        self.pathToPrintAddin = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиПринтов.txt'
        self.pathToCategoryPrint = r'E:\MyProduct\Python\WB\MakePrint\cat.txt'
        if 'под карту' in maskFolderName:
            self.dfAddinFromFile = pandas.DataFrame(pandas.read_csv(self.pathToCardhonlderAddin,sep='\t'))
        elif 'книга' in maskFolderName:
            self.dfAddinFromFile = pandas.DataFrame(pandas.read_csv(self.pathToBookAddin,sep='\t'))
        elif 'SkinShell' in maskFolderName and 'черный' in maskFolderName:
            self.dfAddinFromFile = pandas.DataFrame(pandas.read_csv(self.pathToSkinShellAddin,sep='\t'))
        elif 'силикон ' in maskFolderName and 'мат' in maskFolderName:
            self.dfAddinFromFile = pandas.DataFrame(pandas.read_csv(self.pathToSiliconMTAddin,sep='\t'))
        elif 'силикон ' in maskFolderName and 'проз' in maskFolderName:
            self.dfAddinFromFile = pandas.DataFrame(pandas.read_csv(self.pathToSiliconCLRAddin,sep='\t'))
        elif 'пластик ' in maskFolderName and 'проз' in maskFolderName:
            self.dfAddinFromFile = pandas.DataFrame(pandas.read_csv(self.pathToPlasticAddin,sep='\t'))
        self.dfAddinFromFileDict = self.dfAddinFromFile.to_dict('records')
        self.dfAddinForPrint = pandas.DataFrame(pandas.read_csv(self.pathToPrintAddin,sep='\t'))
        self.dfAddinForPrintDict = self.dfAddinForPrint.to_dict('records')
        self.dfCategoryPrint = pandas.DataFrame(pandas.read_csv(self.pathToCategoryPrint,sep='\t'))
        self.dfCategoryPrintDict = self.dfCategoryPrint.to_dict('records')
        self.data = []
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

        self.applyAddin(price)

    def chekDB(self):
        listChek = [self.pathToSiliconAddin, self.pathToCardhonlderAddin, self.pathToPrintAddin, self.pathToCategory ]
        for i in listChek:
             if not exists(i):
                self.crateDB()
                break

    def crateDB(self):
        pdSilsiconCLRAddin = pandas.DataFrame(pandas.read_excel(self.pathToSiliconCLRAddin.replace('txt','xlsx')))
        pdSilsiconMTAddin = pandas.DataFrame(pandas.read_excel(self.pathToSiliconMTAddin.replace('txt','xlsx')))
        pdBookAddin = pandas.DataFrame(pandas.read_excel(self.pathToBookAddin.replace('txt','xlsx')))
        pdCardhonlderAddin = pandas.DataFrame(pandas.read_excel(self.pathToCardhonlderAddin.replace('txt','xlsx')))
        pdSkinShellAddin = pandas.DataFrame(pandas.read_excel(self.pathToSkinShellAddin.replace('txt','xlsx')))
        pdPrintAddin = pandas.DataFrame(pandas.read_excel(self.pathToPrintAddin.replace('txt','xlsx')))
        pdCategoryPrint = pandas.DataFrame(pandas.read_excel(self.pathToCategoryPrint.replace('txt','xlsx')))
        pdSilsiconCLRAddin.to_csv(self.pathToSiliconCLRAddin,index=None,sep='\t')
        pdBookAddin.to_csv(self.pathToBookAddin,index=None,sep='\t')
        pdSilsiconMTAddin.to_csv(self.pathToSiliconMTAddin,index=None,sep='\t')
        pdCardhonlderAddin.to_csv(self.pathToCardhonlderAddin,index=None,sep='\t')
        pdSkinShellAddin.to_csv(self.pathToSkinShellAddin,index=None,sep='\t')
        pdPrintAddin.to_csv(self.pathToPrintAddin,index=None,sep='\t')
        pdCategoryPrint.to_csv(self.pathToCategoryPrint,index=None,sep='\t')


    @staticmethod
    def generate_bar_WB(count):
        listBarcode = []
        countTry = 0
        url = "https://suppliers-api.wildberries.ru/content/v1/barcodes"
        headers = {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImIxYjQ3YjQzLTFhMTYtNGQ0Ni1iZTA1LWRlY2ExZTcxMTU0MSJ9.qTIJF6fEgbRux3Ps30ciMQ802UWqtAER-y94ALvE3PI'}

        while count > 5000:
            
            while True and countTry < 10:
                json = {
                        "count": 5000
                        }
                try:
                    r = requests.post(url, json=json, headers=headers)
                    listBarcode.extend(r.json()['data'])
                    if not r.json()['error']:
                        count -= 5000
                        break
                except:
                    print(
                        'Ошибка получения ШК. count = {}, пытаюсь повторно получить.'.format(count))
                    print(r.rext)
                    countTry += 1
                    time.sleep(10)
                    continue
        while True and countTry < 10:
            json = {
                        "count": count
                        }
            try:
                r = requests.post(url, json=json, headers=headers)
                listBarcode.extend(r.json()['data'])
                if not r.json()['error']:
                    break
            except:
                print(
                    'Ошибка получения ШК. count = {}, пытаюсь повторно получить.'.format(count))
                countTry += 1
                time.sleep(10)
                continue

        return listBarcode


    def getColor(self):
        for color, code in self.siliconCaseColorDict.items():
            if color in self.maskFolderName:
                if color == 'проз':
                    return 'прозрачный'
                return color


    def getName(self, category):
        for line in self.dfAddinFromFileDict:
            if line['Категория'] == category:
                nameCasePrefix = random.choice(line['Наименование (префикс)'].split(';')).strip()
                break
        # nameCasePrefix = random.choice(self.dfAddinFromFile[self.dfAddinFromFile.Категория == category]['Наименование (префикс)'].values.tolist()[0].split(';')).strip()
        for model in self.modelAddin.split(';'):
            nameCase = nameCasePrefix + ' ' + model
            if len(nameCase) <= 60:
                return nameCase
            else:
                continue
        return 'Чехол для телефона'


    def getVendorCode(self, colorCase, printName):
        vendorCode2 = ''
        if 'силикон с' in self.maskFolderName:
            vendorCode1 = self.maskFolderName.replace('Чехол','').split('силикон')[0].strip().replace(' ','_') + '_BP'
            # if 'с зак.кам.' in self.maskFolderName:
            #     vendorCode2 = 'CCM'
            # elif 'с отк.кам.' in self.maskFolderName:
            #     vendorCode2 = 'OCM'
            # else:
            #     vendorCode2 = 'UCM'
            for color, codeColor in self.siliconCaseColorDict.items():
                if color == colorCase:
                    vendorCode3 = codeColor
                    break
            else:
                vendorCode3 = 'UNKNOW_COLOR'
            if 'под карту' in self.maskFolderName:
                vendorCode3 += '_HLD'
            # return '_'.join([vendorCode1, vendorCode3,#.join([vendorCode1, vendorCode2, vendorCode3,
            #             categoryCode, 'PRNT',printName.replace('(Принт ','').replace(')','')])
            return '_'.join([vendorCode1, vendorCode3,#.join([vendorCode1, vendorCode2, vendorCode3,
                        'PRNT',printName.replace('(Принт ','').replace(')','')])
        elif 'пластик с' in self.maskFolderName:
            vendorCode1 = self.maskFolderName.replace('Чехол','').split('пластик')[0].strip().replace(' ','_') + '_BPP'
            # if 'с зак.кам.' in self.maskFolderName:
            #     vendorCode2 = 'CCM'
            # elif 'с отк.кам.' in self.maskFolderName:
            #     vendorCode2 = 'OCM'
            # else:
            #     vendorCode2 = 'UCM'
            for color, codeColor in self.siliconCaseColorDict.items():
                if color == colorCase:
                    vendorCode3 = codeColor
                    break
            else:
                vendorCode3 = 'UNKNOW_COLOR'
            if 'под карту' in self.maskFolderName:
                vendorCode3 += '_HLD'
            # return '_'.join([vendorCode1, vendorCode3,#.join([vendorCode1, vendorCode2, vendorCode3,
            #             categoryCode, 'PRNT',printName.replace('(Принт ','').replace(')','')])
            return '_'.join([vendorCode1, vendorCode3,#.join([vendorCode1, vendorCode2, vendorCode3,
                        'PRNT',printName.replace('(Принт ','').replace(')','')])
        elif 'книга' in self.maskFolderName:
            vendorCode1 = self.maskFolderName.replace('Чехол книга','').split('черный')[0].strip().replace(' ','_') + '_BK'
            if 'fashion' in self.maskFolderName.lower():
                vendorCode2 = 'FSN'
            # if 'с зак.кам.' in self.maskFolderName:
            #     vendorCode2 = 'CCM'
            # elif 'с отк.кам.' in self.maskFolderName:
            #     vendorCode2 = 'OCM'
            # else:
            #     vendorCode2 = 'UCM'
            for color, codeColor in self.siliconCaseColorDict.items():
                if color == colorCase:
                    vendorCode3 = codeColor
                    break
            else:
                vendorCode3 = 'UNKNOW_COLOR'
            if 'под карту' in self.maskFolderName:
                vendorCode3 += '_HLD'
            # return '_'.join([vendorCode1, vendorCode3,#.join([vendorCode1, vendorCode2, vendorCode3,
            #             categoryCode, 'PRNT',printName.replace('(Принт ','').replace(')','')])
            if vendorCode2 == '':
                return '_'.join([vendorCode1, vendorCode3,
                        'PRNT',printName.replace('(Принт ','').replace(')','')])
            else:        
                return '_'.join([vendorCode1,vendorCode2, vendorCode3,
                            'PRNT',printName.replace('(Принт ','').replace(')','')])

    def getDescription(self, category):
        for line in self.dfAddinFromFileDict:
            if line['Категория'] == category:
                description = random.choice(line['Описание'].split(';')).strip()
                break
        # description = random.choice(self.dfAddinFromFile[self.dfAddinFromFile.Категория == category]['Описание'].values.tolist()).strip()
        countReplace = description.count('***')
        listcompatibility=self.compatibility.split(';')
        for i in range(countReplace):
            try:
                if len(listcompatibility)>i:
                    description = description.replace('***',self.compatibility.split(';')[i],1)
                else:
                    description = description.replace('***',self.compatibility.split(';')[0],1)
            except IndexError:
                description = description.replace('***',self.compatibility.split(';')[0],1)
        return description

    def getDescriptionNew(self, printNameRus):
        description = self.dfAddinFromFile[self.dfAddinFromFile['Принт номер']==printNameRus]['Описание'].values[0]
        countReplace = description.count('***')
        listcompatibility=self.compatibility.split(';')
        for i in range(countReplace):
            try:
                if len(listcompatibility)>i:
                    description = description.replace('***',self.compatibility.split(';')[i],1)
                else:
                    description = description.replace('***',self.compatibility.split(';')[0],1)
            except IndexError:
                description = description.replace('***',self.compatibility.split(';')[0],1)
        return description


    def getEquipmentCase(self, category):
        for line in self.dfAddinFromFileDict:
            if line['Категория'] == category:
                equipmentCasePrefix = random.choice(line['Комплектация (префикс)'].split(';')).strip()
                break
        # equipmentCasePrefix = random.choice(self.dfAddinFromFile[self.dfAddinFromFile.Категория == category]['Комплектация (префикс)'].values.tolist()[0].split(';')).strip()
        return equipmentCasePrefix + ' ' + self.modelAddin.split(';')[0] + ' 1 штука'


    def getRandomValue(self, category, field):
        valueList = []
        for line in self.dfAddinFromFileDict:    
        # listVariation = self.dfAddinFromFile[self.dfAddinFromFile.Категория == category][field].values.tolist()[0].split(';')
            if line['Категория'] == category:
                listVariation = line[field].split(';')
                break
        try:
            if '' in listVariation:
                listVariation.remove('')
            if ' ' in listVariation:
                listVariation.remove(' ')
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


    def getPrintAddin(self, printName, field, category):
        try:
            #a = self.dfAddinForPrint[self.dfAddinForPrint.Принт == printName][field].values.tolist()[0]
            for line in self.dfAddinForPrintDict:
                if line['Принт'] == printName:
                   return self.chekCountField(field, line[field])
            # return self.chekCountField(field, self.dfAddinForPrint[self.dfAddinForPrint.Принт == printName][field].values.tolist()[0])
        except:
            try:
                return self.getRandomValue(category, field)
            except:
                return 0


    def chekCountField(self, field, values):
        maxCount = self.countValueInField[field]
        return ';'.join(values.split(';')[0:maxCount])


    def applyAddin(self, price):
        start_time = time.time()
        # def getAddinFromFile():
        #     dfAddinFromFile = multiprocessing.Process(target=pandas.read_excel, args=(r'E:\MyProduct\Python\WB\MakePrint\Характеристики.xlsx',))

        # def getCategory():
        #     dfCategoryPrint = pandas.read_excel(r'E:\MyProduct\Python\WB\MakePrint\cat.xlsx')

        # dfAddinFromFile = pandas.DataFrame(pandas.read_excel(r'E:\MyProduct\Python\WB\MakePrint\Характеристики.xlsx'))
        # dfCategoryPrint = pandas.DataFrame(pandas.read_excel(r'E:\MyProduct\Python\WB\MakePrint\cat.xlsx'))
        # data = []
        # listCategory = self.dfCategoryPrint['Категория'].unique().tolist()
        if 'книга' in self.maskFolderName:
            stuff = 'Чехлы-книжки для телефонов'

        else:
            stuff = 'Чехлы для телефонов' 
        for i, pictures in enumerate(listdir(self.pathSiliconImage)):
            # start_time = time.time()
            printName = pictures[0:-4]
            if 'print' in pictures:
                printNameRus = pictures.replace('.jpg', ')').replace('print ','(Принт ')
            else:
                printNameRus = pictures.replace('.jpg', '')
            # for line in self.dfCategoryPrintDict:
            #     if line['Принт'] == printName:
            #         category = line['Категория']
            #         categoryCode = line['Код категории']
            #for categoryData in currentPictureCategoryList.values:
            # category = categoryData[1]
            # categoryCode = categoryData[2]
            # categoryCode = currentPictureCategoryList[0][2]
            color = self.getColor()
            if not self.existsFlag:
                vendorCode = self.getVendorCode(color, printName)
            else:
                vendorCode = self.vendorCodeList[i]
            if 'skinshell' in self.maskFolderName.lower():
                # a = self.dfAddinFromFile[self.dfAddinFromFile['Принт номер']==printNameRus]['Комплектация (префикс)'].values[0].replace('***',random.choice(self.modelAddin.split(';')).strip())
                datapicture={
                    'Номер карточки': 1,
                    'Принт': printNameRus,
                    'Категория': 'None',
                    'Цвет': ';'.join(self.dfAddinFromFile[self.dfAddinFromFile['Принт номер']==printNameRus]['Цвет'].values.tolist()),
                    'Баркод товара': '',
                    'Бренд': self.brand,
                    'Наименование': self.dfAddinFromFile[self.dfAddinFromFile['Принт номер']==printNameRus]['Наименование (префикс)'].values[0].replace('***',random.choice(self.modelAddin.split(';')).strip()),
                    'Цена': price,
                    'Артикул товара': vendorCode,
                    'Описание': self.getDescriptionNew(printNameRus),
                    'Производитель телефона': self.modelAddin.split(' ')[0],
                    'Комплектация': self.dfAddinFromFile[self.dfAddinFromFile['Принт номер']==printNameRus]['Комплектация (префикс)'].values[0].replace('***',random.choice(self.modelAddin.split(';')).strip()),
                    'Особенности чехла': ';'.join(self.dfAddinFromFile[self.dfAddinFromFile['Принт номер']==printNameRus]['Особенности чехла'].values.tolist()),
                    'Вид застежки': ';'.join(self.dfAddinFromFile[self.dfAddinFromFile['Принт номер']==printNameRus]['Вид застежки'].values.tolist()),
                    'Рисунок': ';'.join(self.dfAddinFromFile[self.dfAddinFromFile['Принт номер']==printNameRus]['Рисунок'].values.tolist()),
                    'Любимые герои': ';'.join(self.dfAddinFromFile[self.dfAddinFromFile['Принт номер']==printNameRus]['Любимые герои'].values.tolist()),
                    'Совместимость': self.chekCountField('Совместимость',self.compatibility),
                    'Тип чехлов': 'Противоударный чехол',
                    'Модель': self.chekCountField('Модель',self.modelAddin),
                    'Страна производства': 'Китай',
                    'Декоративные элементы': ';'.join(self.dfAddinFromFile[self.dfAddinFromFile['Принт номер']==printNameRus]['Декоративные элементы'].values.tolist()),
                    'Материал изделия': ';'.join(self.dfAddinFromFile[self.dfAddinFromFile['Принт номер']==printNameRus]['Материал изделия'].values.tolist()),
                    'Высота упаковки': 19,
                    'Ширина упаковки': 12,
                    'Глубина упаковки': 2,
                    'Предмет': stuff,
                    'Медиафайлы': r'http://95.78.233.163:8001/wp-content/uploads/Готовые принты/Силикон/{0}/{1};http://95.78.233.163:8001/wp-content/uploads/Вторые картинки/{0}/1.jpg;http://95.78.233.163:8001/wp-content/uploads/Вторые картинки/{0}/2.jpg;http://95.78.233.163:8001/wp-content/uploads/Вторые картинки/{0}/3.jpg;http://95.78.233.163:8001/wp-content/uploads/Вторые картинки/{0}/4.jpg;http://95.78.233.163:8001/wp-content/uploads/Вторые картинки/{0}/5.jpg;http://95.78.233.163:8001/wp-content/uploads/Вторые картинки/{0}/6.jpg'.format(self.maskFolderName, pictures)
                }
            else:
                currentPictureCategoryList = self.dfCategoryPrint[self.dfCategoryPrint.Принт == printNameRus].values.tolist()
                category = currentPictureCategoryList[0][1]
                datapicture = {
                        # 'Номер карточки': listCategory.index(category),
                        'Номер карточки': 1,
                        'Принт': printNameRus,
                        'Категория': category,
                        'Цвет': color if (colorAddin:=self.getPrintAddin(printNameRus, 'Цвет', category)) == 0 else colorAddin,# color,
                        'Баркод товара': '',
                        'Бренд': self.brand,
                        'Наименование': self.getName(category),
                        'Цена': price,
                        'Артикул товара': vendorCode,
                        'Описание': self.getDescription(category),
                        'Производитель телефона': self.modelAddin.split(' ')[0],
                        'Назначение подарка': self.getPrintAddin(printNameRus, 'Назначение подарка', category), # self.getRandomValue(category, 'Назначение подарка'),
                        'Комплектация': self.getEquipmentCase(category),
                        'Особенности чехла': self.getRandomValue(category, 'Особенности чехла'),
                        'Вид застежки': self.getRandomValue(category, 'Вид застежки'),
                        'Рисунок': self.getPrintAddin(printNameRus, 'Рисунок', category), # self.getRandomValue(category, 'Рисунок'),
                        'Любимые герои': self.getPrintAddin(printNameRus, 'Любимые герои', category), # self.getRandomValue(category, 'Любимые герои'),
                        'Совместимость': self.chekCountField('Совместимость',self.compatibility),
                        'Тип чехлов': self.getRandomValue(category, 'Тип чехлов'),
                        'Модель': self.chekCountField('Модель',self.modelAddin),
                        'Повод': self.getPrintAddin(printNameRus, 'Повод', category), # self.getRandomValue(category, 'Повод'),
                        'Страна производства': 'Китай',
                        'Декоративные элементы': self.getPrintAddin(printNameRus, 'Декоративные элементы', category), # self.getRandomValue(category, 'Декоративные элементы'),
                        'Материал изделия': self.getRandomValue(category, 'Материал изделия'),
                        'Высота упаковки': 19,
                        'Ширина упаковки': 12,
                        'Глубина упаковки': 2,
                        'Предмет': stuff,
                        'Медиафайлы': r'http://95.78.233.163:8001/wp-content/uploads/Готовые принты/Силикон/{0}/{1};http://95.78.233.163:8001/wp-content/uploads/Вторые картинки/{0}/1.jpg;http://95.78.233.163:8001/wp-content/uploads/Вторые картинки/{0}/2.jpg;http://95.78.233.163:8001/wp-content/uploads/Вторые картинки/{0}/3.jpg;http://95.78.233.163:8001/wp-content/uploads/Вторые картинки/{0}/4.jpg;http://95.78.233.163:8001/wp-content/uploads/Вторые картинки/{0}/5.jpg'.format(self.maskFolderName, pictures)
                    }
            self.data.append(datapicture)
                # print("--- %s seconds 1 ---" % (time.time() - start_time))
        countBarcods = len(self.data)
        print("--- %s seconds 2 ---" % (time.time() - start_time))
        if not self.existsFlag:
            listBarcods = self.generate_bar_WB(countBarcods)
            for i, case in enumerate(self.data):
                self.data[i]['Баркод товара'] = listBarcods[i]
        self.data


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
    pd = pandas.DataFrame(ModelWithAddin.generate_bar_WB(12135))
    pd.to_excel(r'E:\barcodes.xlsx')

    # ModelWithAddin.pushToDB(r'C:\Users\Георгий\Downloads\Характеристики.xlsx')