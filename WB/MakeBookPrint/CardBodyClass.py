from AddSkriptForMakeSiliconImage import pathToSecondImagesFolder
pathToUpload = r'http://80.237.77.44/joomla/images/mobi/Готовые принты/Силикон'
pathToReplace = r'F:\\Для загрузки\\Готовые принты\\Силикон'

class CardCase:

    def __init__(self, uuid) -> None:
        self.id = uuid
        self.brand = []
        self.name = []
        self.description = []
        self.TNVED = []
        self.equipment = []
        self.reason = []
        self.special = []
        self.lock = []
        self.paint = []
        self.heroes = []
        self.compatibility = []
        self.type = []
        self.model = []
        self.supplCode = ''
        self.struct = {
                "id": self.id,
                "jsonrpc": "2.0",
                "params": {
                    "card":                         
                    [{   "addin": [
                        {
                            "type": "Бренд",
                            "params": [
                            {
                                "value": ''
                            }
                            ]
                        },
                        {
                            "type": 'Наименование',
                            "params": [
                            {
                                "value": ''
                            }
                            ]
                        },
                        {
                            "type": "Описание",
                            "params": [
                            {
                                "value": ''
                            }
                            ]
                        },
                        {
                            "type": "Тнвэд",
                            "params": [
                            {
                                "value": ""
                            }
                            ]
                        },
                        {
                            "type": "Комплектация",
                            "params": [
                            ]
                        },
                        {
                            "type": "Повод",
                            "params": [
                            {
                                "value": ''
                            }
                            ]
                        },
                        {
                            "type": "Особенности чехла",
                            "params": [
                            ]
                        },
                        {
                            "type": "Вид застежки",
                            "params": [
                            ]
                        },
                        {
                            "type": "Рисунок",
                            "params": [
                            ]
                        },
                        {
                            "type": "Любимые герои",
                            "params": [
                            ]
                        },
                        {
                            "type": "Совместимость",
                            "params": [
                            ]
                        },
                        {
                            "type": "Тип чехлов",
                            "params": [
                            ]
                        },
                        {
                            "type": "Модель",
                            "params": [
                            ]
                        }
                        ],
                        "countryProduction": 'Китай',
                        "id":self.id,
                        "nomenclatures": [
                        ],
                        "object": 'Чехлы для телефонов',
                        "parent": 'Смартфоны и аксессуары',
                        "supplierVendorCode": '',
                        
                    }]
                }
                }


    def SetAddin(self, dictWithAddint=dict):
        for key, value in dictWithAddint.items():
            if key == 'Бренд':
                self.brand = value
                continue
            elif key == 'Наименование':
                self.name = value
                continue
            elif key == 'Артикул поставщика':
                self.supplCode = value
                continue
            elif key == 'Описание':
                self.description = value
                continue
            elif key == 'Тнвэд':
                self.TNVED = value
                continue
            elif key == 'Комплектация':
                self.equipment = value
                continue
            elif key == 'Повод':
                self.reason = value
                continue
            elif key == 'Особенности чехла':
                self.special = value
                continue
            elif key == 'Вид застежки':
                self.lock = value
                continue
            elif key == 'Рисунок':
                self.paint = value
                continue
            elif key == 'Любимые герои':
                self.heroes = value
                continue
            elif key == 'Совместимость':
                self.compatibility = value
                continue
            elif key == 'Тип чехлов':
                self.type = value
                continue
            elif key == 'Модель':
                self.model = value
                continue

    def AddNomenklatures(self, nomenklaturesList):
        self.struct['params']['card'][0]['nomenclatures'].append(nomenklaturesList)


    def SetStruct(self):
        self.struct['params']['card'][0]['supplierVendorCode'] = self.supplCode
        for i, addin in enumerate(self.struct['params']['card'][0]['addin']):
            if addin['type'] == 'Бренд':
                self.struct['params']['card'][0]['addin'][i]['params'] = [{'value': self.brand}]
                continue
            elif addin['type'] == 'Наименование':
                self.struct['params']['card'][0]['addin'][i]['params'] = [{'value': self.name}]
                continue
            elif addin['type'] == 'Описание':
                self.struct['params']['card'][0]['addin'][i]['params'] = [{'value': self.description}]
                continue
            elif addin['type'] == 'Тнвэд':
                if type(self.TNVED) == str:
                    tnved = self.TNVED
                elif type(self.TNVED) == float:
                    tnved = str(self.TNVED)[0:-2]
                elif type(self.TNVED) == int:
                    tnved = str(self.TNVED)
                self.struct['params']['card'][0]['addin'][i]['params'] = [{'value': tnved}]
                continue
            elif addin['type'] == 'Комплектация':
                paramsList = []
                for value in self.equipment.split('#'):
                    paramData = {'value': value}
                    paramsList.append(paramData)
                self.struct['params']['card'][0]['addin'][i]['params'] = paramsList[0:3]
                continue
            elif addin['type'] == 'Повод':
                paramsList = []
                for value in self.reason.split('#'):
                    paramData = {'value': value}
                    paramsList.append(paramData)
                self.struct['params']['card'][0]['addin'][i]['params'] = paramsList[0:3]
                continue
            elif addin['type'] == 'Особенности чехла':
                paramsList = []
                for value in self.special.split('#'):
                    paramData = {'value': value}
                    paramsList.append(paramData)
                self.struct['params']['card'][0]['addin'][i]['params'] = paramsList[0:3]
                continue
            elif addin['type'] == 'Вид застежки':
                paramsList = []
                for value in self.lock.split('#'):
                    paramData = {'value': value}
                    paramsList.append(paramData)
                self.struct['params']['card'][0]['addin'][i]['params'] = paramsList[0:3]
                continue
            elif addin['type'] == 'Рисунок':
                paramsList = []
                for value in self.paint.split('#'):
                    paramData = {'value': value}
                    paramsList.append(paramData)
                self.struct['params']['card'][0]['addin'][i]['params'] = [paramsList[0]]
                continue
            elif addin['type'] == 'Любимые герои':
                paramsList = []
                for value in self.heroes.split('#'):
                    paramData = {'value': value}
                    paramsList.append(paramData)
                self.struct['params']['card'][0]['addin'][i]['params'] = [paramsList[0]]
                continue
            elif addin['type'] == 'Совместимость':
                paramsList = []
                for value in self.compatibility.split('#'):
                    paramData = {'value': value}
                    paramsList.append(paramData)
                self.struct['params']['card'][0]['addin'][i]['params'] = paramsList
                continue
            elif addin['type'] == 'Тип чехлов':
                paramsList = []
                for value in self.type.split('#'):
                    paramData = {'value': value}
                    paramsList.append(paramData)
                self.struct['params']['card'][0]['addin'][i]['params'] = paramsList[0:3]
                continue
            elif addin['type'] == 'Модель':
                paramsList = []
                for value in self.model.split('#'):
                    paramData = {'value': value}
                    paramsList.append(paramData)
                self.struct['params']['card'][0]['addin'][i]['params'] = paramsList[0:3]
                continue

    def GetStruct(self):
        return self.struct


class Nomenclature:
    
    def __init__(self, colorCode='', barcode='', price=int, photoURLs=[]) -> None:
        self.colorCode = colorCode
        photoURLs = photoURLs.replace(pathToReplace, pathToUpload).replace('\\', '/')
        self.photoURLs = photoURLs.split('#')
        self.barcode = barcode
        self.price = price if type(price)==int else int(price)
        self.id = ''
        self.structNomenclature = {"addin": [
                            {
                                "type": "Фото",
                                "params": []
                            }
                            ],
                            "concatVendorCode":'',
                            "id":'',
                            "variations": [
                            {
                                "addin": [
                                {
                                    "type": "Розничная цена",
                                    "params": [
                                    {
                                        "count": int
                                    }
                                    ]
                                }
                                ],
                                "barcode": "",
                                "barcodes": [],
                                "id":''
                            }
                            ],
                            "vendorCode": "",
                            
                        }
        if colorCode!='' and barcode!=''and price!=int and photoURLs!=[]:
            self.SetStruct()


    def SetUUID(self, uuid):
        self.id = uuid
        self.structNomenclature['id'] = self.id
        for i, variation in enumerate(self.structNomenclature['variations']):
            self.structNomenclature['variations'][i]['id'] = self.id


    def SetStruct(self):
        # Записываем ссылки на фото
        if self.photoURLs == []:
            print('Ссылки на фото не установенны!')
        else:
            for photoURL in self.photoURLs:
                data = {'value':photoURL}
                self.structNomenclature['addin'][0]['params'].append(data)
        # записываем цену
        if self.price == int:
            print('Цена не установенна!')
        else:
            if type(self.price) == int:
                price = self.price
            elif type(self.price) == str or type(self.price) ==float:
                price = int(self.price)
            self.structNomenclature['variations'][0]['addin'][0]['params'][0]['count'] = price
        # записываем штрихкод
        if self.barcode == "":
            print('Штрихкод не установенн!')
        else:
            self.structNomenclature['variations'][0]['barcode'] = self.barcode
            self.structNomenclature['variations'][0]['barcodes'].append(self.barcode)
        # записываем цвет поставщика
        if self.colorCode == "":
            print('Цвет поставщика не установенн!')
        else:
            self.structNomenclature['vendorCode'] = self.colorCode


    def GetStruct(self):
        return self.structNomenclature