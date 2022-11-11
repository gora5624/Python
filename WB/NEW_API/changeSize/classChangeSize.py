import requests
import pandas
import numpy

class filterNomenclatures1CForChange():
    def __init__(self) -> None:
        self.pathToNomenclaturesListFrom1C = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\ШК.txt'
        self.listNomenclaturesFrom1CDF = ''
        self.listNomenclaturesFromChangeSizeDF = ''
        self.listNomenclaturesFromChangeSizeDict = {}
        

    def getListNomenclatures(self):
        self.listNomenclaturesFrom1CDF = pandas.DataFrame(pandas.read_table(self.pathToNomenclaturesListFrom1C, sep='\t'))

    
    def filterNomenclatures(self, wordsForSearch, wordsForFilter='', delimiter=';'):
        listWordsForSearch = wordsForSearch.split(delimiter)
        if wordsForFilter != '':
            listWordsForFilter= wordsForFilter.split(delimiter)
        self.listNomenclaturesFromChangeSizeDF = self.listNomenclaturesFrom1CDF
        for word in listWordsForSearch:
            # self.barcodeForChange = self.dfBarcod[self.dfBarcod['Характеристика'].str.contains("Принт", na = False)]
            self.listNomenclaturesFromChangeSizeDF = self.listNomenclaturesFromChangeSizeDF[self.listNomenclaturesFromChangeSizeDF['Номенклатура'].str.contains(word, na = False)]
        if wordsForFilter != '':
            for word in listWordsForFilter:
                # self.barcodeForChange = self.dfBarcod[self.dfBarcod['Характеристика'].str.contains("Принт", na = False)]
                self.listNomenclaturesFromChangeSizeDF = self.listNomenclaturesFromChangeSizeDF[~self.listNomenclaturesFromChangeSizeDF['Номенклатура'].str.contains(word, na = False)]
        self.listNomenclaturesFromChangeSizeDict = self.listNomenclaturesFromChangeSizeDF.to_dict('records')
        

    def getNom(self):
        return self.listNomenclaturesFromChangeSizeDict



class getNomenclaturesFromWB():
    def __init__(self, barcode, token) -> None:
        self.barcode = barcode
        self.urlGetCard = 'https://suppliers-api.wildberries.ru/content/v1/cards/cursor/list'
        self.jsonGetCard = {
  "sort": {
    "cursor": {
      "limit": 1000
    },
    "filter": {
      "textSearch": str(barcode),
      "withPhoto": -1
    },
    "sort": {
      "sortColumn": "updateAt",
      "ascending": False
    }
  }
}
        self.urlGetNomenclature = 'https://suppliers-api.wildberries.ru/content/v1/cards/filter'
        self.jsonGetNomenclature = {
            'vendorCode':[

            ]
        }
        self.card = {}
        self.timeout = 5
        self.headersRequest = {'Authorization': '{}'.format(token)}
        self.countTryMax = 10
        # self.responceGetCard=''
        self.cardVendorCode = ''

    def getCard(self):
        countTry = 0
        timeout=self.timeout
        while countTry < self.countTryMax:
            try:
                responce = requests.post(self.urlGetCard, json=self.jsonGetCard, headers=self.headersRequest, timeout=timeout)
                if responce.status_code == 200:
                    # self.responceGetCard = responce
                    if len(cardList:=responce.json()['data']['cards']) != 0:
                        for i, card in enumerate(cardList):
                            if str(self.barcode) in card['sizes'][0]['skus']:
                                self.card = cardList[i]
                                self.cardVendorCode = cardList[i]['vendorCode']
                                self.jsonGetNomenclature = {
                                    'vendorCodes':[
                                        self.cardVendorCode
                                    ]
                                }
                                break
                    else:
                        break
                    break
                else:
                    countTry+=1
                    continue
            except:
                timeout+=2
                countTry+=1
                continue


    def getNomenclature(self):
        countTry = 0
        timeout=self.timeout
        while countTry < self.countTryMax:
            try:
                responce = requests.post(self.urlGetNomenclature, json=self.jsonGetNomenclature, headers=self.headersRequest, timeout=timeout)
                if responce.status_code == 200:
                    # self.responceGetNomenclature = responce
                    if len(nomenclatures:=responce.json()['data']) != 0:
                        for nomenclature in nomenclatures:
                            if str(self.barcode) in nomenclature['sizes'][0]['skus']:
                                return [nomenclature]
                    else:
                        break
                else:
                    countTry+=1
                    continue
            except:
                timeout+=2
                countTry+=1
                continue


class changeSize():
    def __init__(self, nomenclature, token, size=(18,11,1.5), needCheckSize=True, prefixName='Чехол для {}', nameDef='телефона') -> None:
        self.nomenclature = nomenclature
        self.height = size[0]
        self.widht = size[1]
        self.long = size[2]
        self.prefixName = prefixName
        self.nameDef = nameDef
        self.isChange = True
        self.urlChangeSize = 'https://suppliers-api.wildberries.ru/content/v1/cards/update'
        self.jsonChangeSize = nomenclature
        self.headersRequest = {'Authorization': '{}'.format(token)}
        self.needCheckSize = needCheckSize
        self.sizeData = [{'Высота упаковки': self.height},
                        {'Ширина упаковки': self.widht},
                        {'Длина упаковки': self.long}]
        self.timeout = 5
        self.countTryMax = 5


    def checkSize(self):
        height = ''
        widht = ''
        long = ''
        comp = 'телефона'
        for i, char in enumerate(self.nomenclature[0]['characteristics']):
            if 'Высота упаковки' in char:
                height = char['Высота упаковки']
            if 'Ширина упаковки' in char:
                widht = char['Ширина упаковки']
            if 'Длина упаковки' in char:
                long = char['Длина упаковки']
            if 'Рисунок' in char:
                self.nomenclature[0]['characteristics'][i] = {
                    'Рисунок': char['Рисунок'][0:1]
                }
            if 'Совместимость' in char:
                self.nomenclature[0]['characteristics'][i] = {
                    'Совместимость': char['Совместимость'][0:10]
                }
                comp = char['Совместимость'][0]
            if 'Назначение подарка' in char:
                self.nomenclature[0]['characteristics'][i] = {
                    'Назначение подарка': char['Назначение подарка'][0:3]
                }
            if 'Повод' in char:
                self.nomenclature[0]['characteristics'][i] = {
                    'Повод': char['Повод'][0:3]
                }
            if 'Вид застежки' in char:
                self.nomenclature[0]['characteristics'][i] = {
                    'Вид застежки': char['Вид застежки'][0:2]
                }
            if 'Любимые герои' in char:
                self.nomenclature[0]['characteristics'][i] = {
                    'Любимые герои': char['Любимые герои'][0:1]
                }
            if 'Декоративные элементы' in char:
                self.nomenclature[0]['characteristics'][i] = {
                    'Декоративные элементы': char['Декоративные элементы'][0:1]
                }
            if 'Особенности чехла' in char:
                self.nomenclature[0]['characteristics'][i] = {
                    'Особенности чехла': char['Особенности чехла'][0:3]
                }
            if 'Материал изделия' in char:
                self.nomenclature[0]['characteristics'][i] = {
                    'Материал изделия': char['Материал изделия'][0:3]
                }
            if 'Тип чехлов' in char:
                self.nomenclature[0]['characteristics'][i] = {
                    'Тип чехлов': char['Тип чехлов'][0:3]
                }
        for i, char in enumerate(self.nomenclature[0]['characteristics']):    
            if 'Наименование' in char:
                if len(self.nomenclature[0]['characteristics'][i]['Наименование']) > 60:
                    self.nomenclature[0]['characteristics'][i] = {
                        'Наименование': self.prefixName.format(comp) if len(self.prefixName.format(comp)) < 60 else self.prefixName.format(self.nameDef)
                    }
        if '' in [height, widht, long]:
            self.isChange = True
            return True
        else:
            self.isChange = True
            return True


    def changeSize(self):
        if self.needCheckSize:
            if self.checkSize():
                self.changeSizeMain()
        else:
            self.changeSizeMain()
        # return 0
    

    def changeSizeMain(self):
        self.nomenclature[0]['characteristics'].extend(self.sizeData)
        countTry = 0
        timeout=self.timeout
        while countTry < self.countTryMax:
            try:
                responce = requests.post(self.urlChangeSize, json=self.nomenclature, headers=self.headersRequest, timeout=timeout)
                if responce.status_code == 200:
                    print(self.nomenclature[0]['vendorCode'])
                    break
                else:
                    countTry+=1
                    continue
            except:
                timeout+=2
                countTry+=1
                continue
        # return 0