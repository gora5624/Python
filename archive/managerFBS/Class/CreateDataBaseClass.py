if __name__ == '__main__':
    from NomenclaturaClass import Nomenclature
else:
    from Class.NomenclaturaClass import Nomenclature
import pandas
class CreateDataBase():
    def __init__(self, listCase) -> None:
        self.listCase = listCase
        self.brandList = ''
        self.modelList = ''
        self.colorList = ''
        self.cameraTypeList = ''
        self.categoryList = ''
        self.nomenclaturesList = []
        self.siliconCaseColorDict = {
                                    'белый': 'WHT',
                                    'светло-зеленый': 'L-GRN',
                                    'светло-розовый': 'L-PNK',
                                    'светло-фиолетовый': 'L-PPL',
                                    'бледно-розовый': 'L-PNK',
                                    'темно-синий': 'D-BLU',
                                    'темно-сиреневый': 'D-LLC',
                                    'бирюзовый': 'TRQ',
                                    'бордовый': 'VNS',
                                    'голубой': 'SKB',
                                    'желтый': 'YLW',
                                    'салатовый': 'L-GRN',
                                    'зеленый': 'GRN',
                                    'красный': 'RED',
                                    'пудра': 'PWD',
                                    'розовый': 'PNK',
                                    'серый': 'GRY',
                                    'синий': 'BLU',
                                    'фиолетовый': 'PPL',
                                    'хаки': 'HCK',
                                    'черный': 'BLC',
                                    'прозрачный': 'CLR',
                                    'проз': 'CLR'
                                    }
        self.bookCaseColorDict = {
                                'бордовый': 'VNS',
                                'бронзовый': 'BNZ',
                                'голубой': 'SKB',
                                'зеленый': 'GRN',
                                'розовое золото': 'P-GLD',
                                'золотой': 'GLD',
                                'красный': 'RED',
                                'серый': 'GRY',
                                'синий': 'BLU',
                                'черный': 'BLC'
                                }
        self.cameraTypeDict = {
                                'открытая': 'OCM',
                                'закрытая': 'CCM',
                                'не определено': 'UCM'
                                }
        self.caseTypeDict = {
                                'силикон': 'BP',
                                'книжка': 'BK'
                                }
        self.categoryDict = {
                            'Авто-мото': 'AUM',
                            'Аниме': 'ANI',
                            'Арты': 'ART',
                            'Бабочки': 'BTF',
                            'Города и страны': 'CAC',
                            'Девушки': 'GRL',
                            'Детские': 'CLD',
                            'Женские': 'WMN',
                            'Животные': 'ANM',
                            'Космос': 'SPC',
                            'Ловцы снов': 'COD',
                            'Надписи': 'TXT',
                            'Орнаменты, узоры, абстракция': 'PTT',
                            'Парные': 'DBL',
                            'Природа': 'NTR',
                            'Сердечки': 'HRT',
                            'Стикеры': 'STK',
                            'Фрукты-ягоды': 'FRT',
                            'Цветы': 'FLW',
                            '9 Мая': '9MY'
                            }
        self.getAddin()
        pass

    def getAddin(self):
        dataBaseTMPList = []
        for case in self.listCase:
            for nomenclature in case['nomenclatures']:
                brand = case['supplierVendorCode'].split('_')[0]
                model = case['supplierVendorCode'].split('_PRNT')[0].replace('_',' ') if '_PRNT' in case['supplierVendorCode'] else case['supplierVendorCode'].split('_WUPRNT')[0].replace('_',' ')
                color = self.getColor(nomenclature['vendorCode'])
                cameraType = self.getCameraType(case['supplierVendorCode'])
                category = self.getCategoty(nomenclature['vendorCode'])
                caseType = self.getCaseType(nomenclature['vendorCode'])
                for variat in nomenclature['variations']:
                    for barcod in variat['barcodes']:
                        dataBaseTMPDict = {
                            'brand': brand,
                            'model': model,
                            'color': color,
                            'cameraType': cameraType,
                            'category': category,
                            'caseType': caseType,
                            'barcod': barcod,
                            'nmId' : nomenclature['nmId']
                        }
                        dataBaseTMPList.append(dataBaseTMPDict)
        dataBaseTMPListdp = pandas.DataFrame(dataBaseTMPList)
        self.brandList = dataBaseTMPListdp['brand'].unique().tolist()
        self.brandList.sort()
        self.modelList = dataBaseTMPListdp['model'].unique().tolist()
        self.modelList.sort()
        self.colorList = dataBaseTMPListdp['color'].unique().tolist()
        self.colorList.sort()
        self.cameraTypeList = dataBaseTMPListdp['cameraType'].unique().tolist()
        self.cameraTypeList.sort()
        self.categoryList = dataBaseTMPListdp['category'].unique().tolist()
        self.categoryList.sort()
        self.nomenclaturesList = dataBaseTMPListdp
        # for brand in self.brandList:
        #     brandTMP = dataBaseTMPListdp[dataBaseTMPListdp.brand == brand]
        #     if brandTMP.size != 0:
        #         for model in self.modelList:
        #             modelTMP = brandTMP[brandTMP.model == model]
        #             if modelTMP.size != 0:
        #                 for camera in self.cameraTypeList:
        #                     cameraTMP = modelTMP[modelTMP.cameraType == camera]
        #                     if cameraTMP.size != 0:
        #                         for color in self.colorList:
        #                             colorTMP = cameraTMP[cameraTMP.color == color]
        #                             if colorTMP.size != 0:
        #                                 for category in self.categoryList:
        #                                     nomenclature = Nomenclature(brand, model, color, camera, category)
        #                                     nomenclature.barcodesList = colorTMP[colorTMP.category == category]['barcod'].to_list()
        #                                     # a = colorTMP[colorTMP.category == category]
        #                                     nomenclature.nmIdList = colorTMP[colorTMP.category == category]['nmId'].to_list()
        #                                     # b = colorTMP[colorTMP.category == category]
        #                                     if len(nomenclature.barcodesList) != 0:
        #                                         self.nomenclaturesList.append(nomenclature)

                    
        


    
    def getColor(self, supplierVendorCode):
        for colorCode in self.siliconCaseColorDict.items():
            if colorCode[1] in supplierVendorCode:
                return colorCode[0]
        for colorCode in self.bookCaseColorDict.items():
            if colorCode[1] in supplierVendorCode:
                return colorCode[0]
        return 'не определено'


    def getCameraType(self, supplierVendorCode):
        for cameraType in self.cameraTypeDict.items():
            if cameraType[1] in supplierVendorCode:
                return cameraType[0]
        return 'не определено'

    def getCategoty(self, supplierVendorCode):
        for category in self.categoryDict.items():
            if category[1] in supplierVendorCode:
                return category[0]
        return 'не определено'  


    def getCaseType(self, supplierVendorCode):
        for caseType in self.caseTypeDict.items():
            if caseType[1] in supplierVendorCode:
                return caseType[0]
        return 'не определено'  
