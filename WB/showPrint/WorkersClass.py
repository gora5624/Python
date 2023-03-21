import os
import pickle
from threading import Thread
import requests
from PyQt6.QtCore import QRunnable, pyqtSignal as Signal, pyqtSlot as Slot, QObject
import pandas as pd


class SignalsWorkerGetDataFrom1c(QObject):
    complete = Signal(list, pd.DataFrame)

class SignalsCheckDBImage(QObject):
    complete = Signal()

class SignalsRequestImageAPI(QObject):
    complete = Signal(bytes)
    fail = Signal(str, str)

class WorkerCheckDBImage(QRunnable):
    pathToPickleDB = os.path.join(a:=os.path.dirname(__file__), 'printPicle.pkl')
    pathToPrintImages = r'\\192.168.0.111\shared\_Общие документы_\Каталог принтов'
    def __init__(self, force = False) -> None:
        super().__init__()
        self.pickleDB = {}
        self.signal = SignalsCheckDBImage()
        self.force = force
        
    @Slot()
    def run(self):
        if self.force:
            self.createPicleWithImages()
            self.signal.complete.emit()
            return
        else:
            if os.path.exists(self.pathToPickleDB):
                with open(self.pathToPickleDB, 'rb') as f:
                    self.pickleDB = pickle.load(f)
                    f.close()
                for file in os.listdir(self.pathToPrintImages):
                    if file not in self.pickleDB:
                        self.createPicleWithImages()
                        break
                self.signal.complete.emit()
            else:
                self.createPicleWithImages()
                self.signal.complete.emit()
    
    def createPicleWithImages(self):
        for file in os.listdir(self.pathToPrintImages):
            b = open(os.path.join(self.pathToPrintImages, file), 'rb').read()
            self.pickleDB.update({file: b})
        with open(self.pathToPickleDB, 'wb') as f:
            pickle.dump(self.pickleDB, f)
            f.close()

class WorkerGetDataFrom1c(QRunnable):

    pathToBarcodeList1c = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\ШК.txt'

    def __init__(self) -> None:
        super().__init__()
        self.signal = SignalsWorkerGetDataFrom1c()

    # запрос данных из спика штрихкодов в 1С
    @Slot()
    def run(self):
        self.dataDF = pd.DataFrame(pd.read_table(self.pathToBarcodeList1c, sep='\t', encoding='utf-8', dtype=str))
        self.dataDF.fillna('', inplace=True)
        self.listBarcodesFrom1C = self.dataDF['Штрихкод'].values.tolist()
        self.signal.complete.emit(self.listBarcodesFrom1C, self.dataDF)
        return

class WorkerRequestImageAPI(QRunnable):
    tokens = [
                    {
                        'IPName': 'Караханян',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
                    },
                    {
                        'IPName': 'Самвел',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
                    },
                    
                    {
                        'IPName': 'Манвел',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
                    } ,
                    
                    {
                        'IPName': 'Федоров',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImIxYjQ3YjQzLTFhMTYtNGQ0Ni1iZTA1LWRlY2ExZTcxMTU0MSJ9.qTIJF6fEgbRux3Ps30ciMQ802UWqtAER-y94ALvE3PI'
                    }             
                ]
    urlGetImage = 'https://suppliers-api.wildberries.ru/content/v1/cards/cursor/list'

    def __init__(self, barcode) -> None:
        super().__init__()
        self.barcode = barcode
        self.urlImage = ''
        self.signal = SignalsRequestImageAPI()

    
    def run(self):
        for token in self.tokens:
            headersRequest = {'Authorization': '{}'.format(token['token'])}
            params = {
                "sort": {"cursor": {
                "limit": 1000
                },"filter": 
                {"textSearch": str(self.barcode),
                "withPhoto": -1}
                }
                }
            r = requests.post(self.urlGetImage, json=params, headers=headersRequest)
            if r.status_code != 200:
                continue
            if len(cards:=r.json()['data']['cards'])==0:
                continue
            else:
                if len(cards[0]['mediaFiles']) >0:
                    for url in cards[0]['mediaFiles']:
                        if  '1.jpg' in url:
                            self.urlImage = url
                            break
                    if self.urlImage == '':
                        self.urlImage = cards[0]['mediaFiles'][0]
        self.getImageFromUrl()

    @Slot()
    def getImageFromUrl(self):
        # запрос картинки по ссылке
        if self.urlImage != '':
            r = requests.get(self.urlImage)
            # self.content = r.content
            self.signal.complete.emit(r.content)
        else:
            self.signal.fail.emit('Ошибка при получении изображения из веб-сервиса', 'red')