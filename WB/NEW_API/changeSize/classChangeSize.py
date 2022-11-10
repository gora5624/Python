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
        self.responceGetCard=''
        self.cardVendorCode = ''

    def getCard(self):
        countTry = 0
        timeout=self.timeout
        while countTry < self.countTryMax:
            try:
                responce = requests.post(self.urlGetCard, json=self.jsonGetCard, headers=self.headersRequest, timeout=timeout)
                if responce.status_code == 200:
                    self.responceGetCard = responce
                    if len(cardList:=self.responceGetCard.json()['data']['cards']) != 0:
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
                    self.responceGetNomenclature = responce
                    if len(nomenclatures:=self.responceGetNomenclature.json()['data']) != 0:
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
    def __init__(self, nomenclature, token, size=(18,11,1.5), needCheckSize=True) -> None:
        self.nomenclature = nomenclature
        self.height = size[0]
        self.widht = size[1]
        self.long = size[2]
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
        for char in self.nomenclature[0]['characteristics']:
            if 'Высота упаковки' in char:
                height = char['Высота упаковки']
            if 'Ширина упаковки' in char:
                widht = char['Ширина упаковки']
            if 'Длина упаковки' in char:
                long = char['Длина упаковки']
        if '' in [height, widht, long]:
            self.isChange = True
        else:
            self.isChange = False


    def changeSize(self):
        if self.needCheckSize:
            if self.checkSize():
                self.changeSizeMain()
        else:
            self.changeSizeMain()
    

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