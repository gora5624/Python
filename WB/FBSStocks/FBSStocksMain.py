import sys
import pandas
from os.path import join as joinPath, abspath
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication
from ChangeAvailabilityClass import ChangeAvailability
from ui.FBSStocks import Ui_Form
import telebot
from datetime import datetime
# pyuic5 E:\MyProduct\Python\WB\FBSStocks\ui\FBSStocks.ui -o E:\MyProduct\Python\WB\FBSStocks\ui\FBSStocks.py

class FBSStoks(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(FBSStoks, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.selectFileButton.clicked.connect(self.selectFile)
        self.ui.pushEmptyStocks.clicked.connect(self.pushEmptyStocks)
        self.ui.pushFullStocks.clicked.connect(self.pushFullStocks)
        self.ui.getNomList.clicked.connect(self.getListNom)
        self.ui.selectNomenclatureComboBox.setDisabled(True)
        self.ui.selectNomenclatureComboBox.currentTextChanged.connect(self.disenableFileSelectButt)
        self.ui.pushEmptyStocks.setDisabled(True)
        self.ui.pushFullStocks.setDisabled(True)
        self.ui.selectFileButton.setDisabled(True)
        self.fileUpdateStokcsName = ''
        self.nomenclature = ''
        self.sellerList = []
        self.cameraTypeList = ['зак.', 'отк.']
        self.ui.exampleFileToUploadBtn.clicked.connect(self.getExampleFile)
        self.botToken = open(abspath(joinPath(__file__,'..', 'token')), 'r').read()
        self.bot = telebot.TeleBot(self.botToken)

    def selectFile(self):
        self.fileUpdateStokcsName = QFileDialog.getOpenFileName(self, ("Выберите файл со списком номенклатуры"), "", ("Excel Files (*.xlsx)"))[0]
        if self.fileUpdateStokcsName == '':
            self.createMSGError("Вы не выбрали файл номенклатурой для загрузки.")
            return 0
        self.ui.selectFileButton.setText(self.fileUpdateStokcsName)
        self.ui.selectNomenclatureComboBox.setDisabled(True)


    def disenableFileSelectButt(self):
        self.ui.selectFileButton.setDisabled(True)


    def getExampleFile(self):
        flag = self.ui.exampleFileToUploadComboBox.currentText()
        fileExamplePath = QFileDialog.getExistingDirectory(self, ("Выберите место для сохранения образца"))
        fileName = flag + '.xlsx'
        if fileExamplePath == '':
            self.createMSGError('Вы не выбрали папку')
            return 0
        if flag == 'Образец файла по наименованию номенклатуры':
            df = pandas.DataFrame([{'Номенклатура':'Введите название номенклатуры сюда'}, {'Номенклатура':'Введите название номенклатуры сюда'}, {'Номенклатура':'Введите название номенклатуры сюда'}])
            df.to_excel(joinPath(fileExamplePath, fileName), index=False)
            self.createMSGSuc('{} создан по пути {}!'.format(fileName, fileExamplePath))
        elif flag =='Образец файла по наименованию номенклатуры с количеством':
            df = pandas.DataFrame([{
                'Номенклатура':'Введите название номенклатуры сюда',
                'Количество': 'Введите количество сюда, целым числом'
            },
            {
                'Номенклатура':'Введите название номенклатуры сюда',
                'Количество': 'Введите количество сюда, целым числом'
            },
            {
                'Номенклатура':'Введите название номенклатуры сюда',
                'Количество': 'Введите количество сюда, целым числом'
            }])
            df.to_excel(joinPath(fileExamplePath, fileName), index=False)
            self.createMSGSuc('{} создан по пути {}!'.format(fileName, fileExamplePath))
        elif flag =='Образец файла по баркоду':
            df = pandas.DataFrame([{
                'Баркод':'Введите баркод номенклатуры сюда'
            },
            {
                'Баркод':'Введите баркод номенклатуры сюда'
            },
            {
                'Баркод':'Введите баркод номенклатуры сюда'
            }])
            df.to_excel(joinPath(fileExamplePath, fileName), index=False)
            self.createMSGSuc('{} создан по пути {}!'.format(fileName, fileExamplePath))
        elif flag =='Образец файла по баркоду с количеством':
            df = pandas.DataFrame([{
                'Баркод':'Введите баркод номенклатуры сюда',
                'Количество': 'Введите количество сюда, целым числом'
            }, 
            {
                'Баркод':'Введите баркод номенклатуры сюда',
                'Количество': 'Введите количество сюда, целым числом'
            },
            {
                'Баркод':'Введите баркод номенклатуры сюда',
                'Количество': 'Введите количество сюда, целым числом'
            }])
            df.to_excel(joinPath(fileExamplePath, fileName), index=False)
            self.createMSGSuc('{} создан по пути {}!'.format(fileName, fileExamplePath))
        else:
            pass


    def getListNom(self):
        self.nomenclature = QFileDialog.getOpenFileName(self, ("Выберите список ШК"), "", ("Excel Files (*.xlsx)"))[0]
        self.ui.getNomList.setText("Идёт получение списка номенклатур...")
        #self.ui.getNomList.setDisabled(True)
        QApplication.processEvents()
        if self.nomenclature == '':
            self.createMSGError("Вы не выбрали файл с базой, работа невозможна.")
            return 0
        self.ui.getNomList.setText(self.nomenclature)
        self.data = pandas.DataFrame(pandas.read_excel(self.nomenclature)).sort_values(by='Номенклатура')
        self.ui.selectNomenclatureComboBox.addItems(self.data['Номенклатура'].unique())
        self.ui.selectFileButton.setText("Выберите файл с номенклатурой")
        self.ui.selectNomenclatureComboBox.setDisabled(False)
        self.ui.selectNomenclatureComboBox.setEditable(True)
        self.ui.pushEmptyStocks.setDisabled(False)
        self.ui.pushFullStocks.setDisabled(False)
        self.ui.selectFileButton.setDisabled(False)
        self.ui.selectNomenclatureComboBox.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.ui.selectNomenclatureComboBox.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.ui.pushEmptyStocks.setStyleSheet('background: #e3e3e3;')
        self.ui.pushFullStocks.setStyleSheet('background: #e3e3e3;')
        QApplication.processEvents()


    def getListBarcodForComboBox(self):
        if self.ui.glassCheck.isChecked() and ('Бронепленка' in self.ui.selectNomenclatureComboBox.currentText() or 'стекло 3D' in self.ui.selectNomenclatureComboBox.currentText()):
            try:
                listBarcods = self.data[self.data.Номенклатура.str.contains(self.ui.selectNomenclatureComboBox.currentText().split(':')[1], regex=False)]['Штрихкод'].values.tolist()
            except:
                return self.data[self.data.Номенклатура == self.ui.selectNomenclatureComboBox.currentText()]['Штрихкод'].values.tolist()
            return listBarcods
        if self.ui.cameraTypeCheck.isChecked():
            listBarcods = []
            for i, cameraType in enumerate(self.cameraTypeList):
                listBarcods.extend(self.data[self.data.Номенклатура == self.ui.selectNomenclatureComboBox.currentText().replace(self.cameraTypeList[i],self.cameraTypeList[i-1])]['Штрихкод'].values.tolist())
            return listBarcods
        else:
            return self.data[self.data.Номенклатура == self.ui.selectNomenclatureComboBox.currentText()]['Штрихкод'].values.tolist()



    def getSeller(self):
        self.sellerList = []
        if self.ui.karahanaynChek.isChecked():
            self.sellerList.append('Э.С. Караханян')
        if self.ui.manvelChek.isChecked():
            self.sellerList.append('М.С. Абраамян')
        if self.ui.samvelChek.isChecked():
            self.sellerList.append('С.М. Абраамян')


    def getListBarcodForFile(self, nom, count= 0):
        if not self.ui.cameraTypeCheck.isChecked():
            listBarcods = []
            listBarcodsTMP = self.data[self.data.Номенклатура == nom]['Штрихкод'].values.tolist()
            for barcod in listBarcodsTMP:
                listBarcods.append({
                    'barcod':barcod,
                    'count':count 
                })
            return listBarcods
        else: 
            listBarcods = []
            for i, cameraType in enumerate(self.cameraTypeList):
                listBarcodsTMP = self.data[self.data.Номенклатура == nom.replace(self.cameraTypeList[i],self.cameraTypeList[i-1])]['Штрихкод'].values.tolist()
                for barcod in listBarcodsTMP:
                    listBarcods.append({
                        'barcod':barcod,
                        'count':count 
                    })
            return listBarcods



    def pushFullStocks(self):
        listBarcods = []
        if not self.ui.selectNomenclatureComboBox.isEnabled():
            self.dataForUpdateStocks = pandas.DataFrame(pandas.read_excel(self.fileUpdateStokcsName))
            if 'Номенклатура' in self.dataForUpdateStocks.columns:
                for line in self.dataForUpdateStocks.to_dict('records'):
                    nom = line['Номенклатура']
                    try:
                        count = line['Количество']
                    except:
                        count = 10000
                    listBarcods.extend(self.getListBarcodForFile(nom, count))
            elif 'Баркод' in self.dataForUpdateStocks.columns:
                listBarcods = self.dataForUpdateStocks.rename(columns={'Баркод':'barcod', 'Количество':'stock'}).to_dict('records')
                #listBarcods.extend(self.dataForUpdateStocks.Баркод.values.tolist())
            else:
                self.createMSGError("Некорректный файл со списком номенклатуры или ШК.")
                return 0
            if listBarcods == []:
                self.createMSGError("Список ШК пуст.")
                return 0
            self.getSeller()
            for seller in self.sellerList:
                pusher = ChangeAvailability(seller, listBarcods)
                resp = pusher.takeOn()
                if resp == 0:
                    self.ui.pushFullStocks.setStyleSheet('background: rgb(0,255,0);') 
                    #self.createMSGSuc("{}".format(self.fileUpdateStokcsName))
                else: 
                    self.ui.pushFullStocks.setStyleSheet('background: rgb(255,0,0);')
                    #self.createMSGError("{}".format(self.fileUpdateStokcsName))                
        else:
            self.getSeller()
            listBarcods = self.getListBarcodForComboBox()
            if self.sellerList == []:
                self.createMSGError("Не выбран ни один поставщик")
                return 0
            for seller in self.sellerList:
                pusher = ChangeAvailability(seller, listBarcods)
                resp = pusher.takeOn()
                if resp == 0:
                    self.ui.pushFullStocks.setStyleSheet('background: rgb(0,255,0);')
                    #self.createMSGSuc("{}".format(self.ui.selectNomenclatureComboBox.currentText()))
                else:
                    self.ui.pushFullStocks.setStyleSheet('background: rgb(255,0,0);')
                    #self.createMSGError("{}".format(self.ui.selectNomenclatureComboBox.currentText()))
        action = 'поставили в наличие'
        self.sendMassageToTelegram(action, listBarcods)


    def getnomenclaturesListForBot(self, listBarcods):
        if type(listBarcods[0]) != dict:
            return self.data.loc[self.data['Штрихкод'].isin(listBarcods)].Номенклатура.unique().tolist()
        else:
            listTMP = []
            for line in listBarcods:
                listTMP.append(line['barcod'])
            return self.data.loc[self.data['Штрихкод'].isin(listTMP)].Номенклатура.unique().tolist()


    def sendMassageToTelegram(self, action, listBarcods):
        nomenclaturesListForBot = self.getnomenclaturesListForBot(listBarcods)
        curData = datetime.today().date().strftime(r"%d.%m.%Y")
        curTime = datetime.today().time().strftime(r"%H.%M.%S")
        if len(nomenclaturesListForBot) ==0:
            text = 'В {} {} {} неизвестно что('.format(curData, curTime, action)
        elif len(nomenclaturesListForBot) >1:
            text = 'В {} {} {} следующие позиции: {}'.format(curData, curTime, action,','.join(nomenclaturesListForBot))
        elif len(nomenclaturesListForBot) ==1:
            text = 'В {} {} {} следующую позицию: {}'.format(curData, curTime, action,','.join(nomenclaturesListForBot))
        self.bot.send_message(-1001550015840, text)


    def pushEmptyStocks(self):
        listBarcods = []
        if not self.ui.selectNomenclatureComboBox.isEnabled():
            self.dataForUpdateStocks = pandas.DataFrame(pandas.read_excel(self.fileUpdateStokcsName))
            if 'Номенклатура' in self.dataForUpdateStocks.columns:
                for nom in self.dataForUpdateStocks.Номенклатура:
                    listBarcods.extend(self.getListBarcodForFile(nom))
            elif 'Баркод' in self.dataForUpdateStocks.columns:

                listBarcods = self.dataForUpdateStocks.rename(columns={'Баркод':'barcod', 'Количество':'stock'}).to_dict('records')
                #listBarcods.extend(self.dataForUpdateStocks.Баркод.values.tolist())
            else:
                self.createMSGError("Некорректный файл со списком номенклатуры или ШК.")
                return 0
            if listBarcods == []:
                self.createMSGError("Список ШК пуст.")
                return 0
            self.getSeller()
            for seller in self.sellerList:
                pusher = ChangeAvailability(seller, listBarcods)
                #Тестовый метод
                resp = pusher.takeOffDelet()
                # resp = pusher.takeOff()
                if resp == 0:
                    # self.ui.pushEmptyStocks.setStyleSheet('background: rgb(0,255,0);') 
                    self.createMSGSuc("{}".format(self.fileUpdateStokcsName))
                else: 
                    # self.ui.pushEmptyStocks.setStyleSheet('background: rgb(255,0,0);')
                    self.createMSGError("{}".format(self.fileUpdateStokcsName))
        else:
            self.getSeller()
            listBarcods = self.getListBarcodForComboBox()
            if self.sellerList == []:
                self.createMSGError("Не выбран ни один поставщик")
                return 0
            for seller in self.sellerList:
                pusher = ChangeAvailability(seller, listBarcods)
                #Тестовый метод
                resp = pusher.takeOffDelet()
                # resp = pusher.takeOff()
                if resp == 0:
                    # self.ui.pushEmptyStocks.setStyleSheet('background: rgb(0,255,0);') 
                    self.createMSGSuc("{}".format(self.ui.selectNomenclatureComboBox.currentText()))
                else: 
                    # self.ui.pushEmptyStocks.setStyleSheet('background: rgb(255,0,0);')
                    self.createMSGError("{}".format(self.ui.selectNomenclatureComboBox.currentText()))
        action = 'сняли с наличия'
        self.sendMassageToTelegram(action, listBarcods)

    def createMSGError(self,text):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setText(text)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.exec_()


    def createMSGSuc(self,text):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Внимание")
        msg.setText(text)
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.exec_()


    def closeEvent(self, event):
            close = QtWidgets.QMessageBox.question(self,
                                                "Выход",
                                                "Вы уверенны что хотите закрыть программу?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if close == QtWidgets.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()


    def acceptEvent(self, text):
            close = QtWidgets.QMessageBox.question(self,
                                                "Вопрос",
                                                text,
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if close == QtWidgets.QMessageBox.Yes:
                return True
            else:
                return False


if __name__ =='__main__':
    app = QtWidgets.QApplication([])
    application = FBSStoks()
    application.show()
    sys.exit(app.exec())
