import pandas
import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication
from ui_untitled import Ui_Form
import requests
import multiprocessing


class filter(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(filter, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.pathToBarcode = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\ШК.txt'
        self.df = pandas.DataFrame()
        self.ui.saveButton.clicked.connect(self.main)
        self.timeout = 2
        self.getListNom()
        self.tokens = [
                {
                    'IPName': 'Караханян',
                    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
                },
                {
                    'IPName': 'Манвел',
                    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
                },
                {
                    'IPName': 'Самвел',
                    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
                }

            ]
        

    def getListNom(self):
        self.df = pandas.DataFrame(pandas.read_table(self.pathToBarcode, sep='\t').sort_values(by='Номенклатура'))
        self.ui.selector.addItems(self.df['Номенклатура'].unique())
        self.ui.selector.setEditable(True)
        self.ui.selector.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.ui.selector.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)

    def main(self):
        nom = self.ui.selector.currentText()
        userPath = QFileDialog.getExistingDirectory(self, ("Выберите место для сохранения"))
        if self.ui.vendorCodeChek.isChecked():
            self.filterBarcodeAndVendorCode(nom, userPath)
        else:
            self.filterBarcodeOnly(nom, userPath)


    def getListVendorCodes(self, listBarcode):
        
        ip = self.ui.ipSelector.currentText()
        if ip == 'Искать по всем':
            manager = multiprocessing.Manager()
            listVendorCode = manager.list()
            for tokenLine in self.tokens:
                token = tokenLine['token']
                pool = multiprocessing.Pool()
                # listProc = []
                for barcode in listBarcode:
                    pool.apply_async(getCards, args=(token, barcode, listVendorCode))
                    # self.getCards(token, barcode, listVendorCode)
                    # p = multiprocessing.Process(target=getCards, args=(token, barcode, listVendorCode,))
                    # p.start()
                    # listProc.append(p)
                # for p in listProc:
                #     p.join()
                pool.close()
                pool.join()
            a=list(listVendorCode)
            return pandas.DataFrame(list(listVendorCode))
                
        else:
            for tokenLine in self.tokens:
                manager = multiprocessing.Manager()
                listVendorCode = manager.list()
                if tokenLine['IPName'] == ip:
                    # token = tokenLine['token']
                    pool = multiprocessing.Pool()
                    for barcode in listBarcode:
                        pool.apply_async(getCards, args=(tokenLine, barcode, listVendorCode))
                    pool.close()
                    pool.join()
            a=list(listVendorCode)
            return pandas.DataFrame(list(listVendorCode))






    def filterBarcodeAndVendorCode(self, nom, userPath):
        df2 =  self.df[self.df['Номенклатура'] == nom].sort_values(by=['Номенклатура','Характеристика'])
        listBarcode = df2['Штрихкод'].values.tolist()
        listBarcode = self.getListVendorCodes(listBarcode)
        df2 = pandas.merge(df2, listBarcode, how='left',left_on='Штрихкод',right_on='Штрихкод')
        df2.to_excel(os.path.join(userPath, nom + '.xlsx'), index=False)


    def filterBarcodeOnly(self, nom, userPath):
        df2 =  self.df[self.df['Номенклатура'] == nom].sort_values(by=['Номенклатура','Характеристика'])
        df2.to_excel(os.path.join(userPath, nom + '.xlsx'), index=False)
        


def getCards(tokenLine, barcode, listVendorCode):
        urlGetCard = 'https://suppliers-api.wildberries.ru/content/v1/cards/cursor/list'
        headersRequest = {'Authorization': '{}'.format(tokenLine['token'])}
        jsonGetCard = {
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
        countTry = 0
        timeout=5
        while countTry < 5:
            try:
                responce = requests.post(urlGetCard, json=jsonGetCard, headers=headersRequest, timeout=timeout)
                if responce.status_code == 200:
                    # self.responceGetCard = responce
                    if len(cardList:=responce.json()['data']['cards']) != 0:
                        for i, card in enumerate(cardList):
                            if str(barcode) in card['sizes'][0]['skus']:
                                listVendorCode.append({'Штрихкод': barcode, 'Артикул поставщика': cardList[i]['vendorCode'],'ИП':tokenLine['IPName']})
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

if __name__ =='__main__':
    app = QtWidgets.QApplication([])
    application = filter()
    application.show()

    sys.exit(app.exec())