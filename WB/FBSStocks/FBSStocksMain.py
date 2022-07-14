import sys
import pandas
from os import listdir
from os.path import join as joinPath, isdir, isfile, abspath, exists
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication
from ChangeAvailabilityClass import ChangeAvailability
from ui.FBSStocks import Ui_Form
from itertools import product
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


    def selectFile(self):
        self.fileUpdateStokcsName = QFileDialog.getOpenFileName(self, ("Выберите файл со списком номенклатуры"), "", ("Excel Files (*.xlsx)"))[0]
        if self.fileUpdateStokcsName == '':
            self.createMSGError("Вы не выбрали файл номенклатурой для загрузки.")
            return 0
        self.ui.selectFileButton.setText(self.fileUpdateStokcsName)
        self.ui.selectNomenclatureComboBox.setDisabled(True)


    def disenableFileSelectButt(self):
        self.ui.selectFileButton.setDisabled(True)


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
        listBarcods = self.data[self.data.Номенклатура == self.ui.selectNomenclatureComboBox.currentText()]['Штрихкод'].values.tolist()
        return listBarcods


    def getSeller(self):
        self.sellerList = []
        if self.ui.karahanaynChek.isChecked():
            self.sellerList.append('Э.С. Караханян')
        if self.ui.manvelChek.isChecked():
            self.sellerList.append('М.С. Абраамян')
        if self.ui.samvelChek.isChecked():
            self.sellerList.append('С.М. Абраамян')


    def getListBarcodForFile(self, nom):
        listBarcods = self.data[self.data.Номенклатура == nom]['Штрихкод'].values.tolist()
        return listBarcods


    def pushFullStocks(self):
        listBarcods = []
        if not self.ui.selectNomenclatureComboBox.isEnabled():
            self.dataForUpdateStocks = pandas.DataFrame(pandas.read_excel(self.fileUpdateStokcsName))
            if 'Номенклатура' in self.dataForUpdateStocks.columns:
                for nom in self.dataForUpdateStocks.Номенклатура:
                    listBarcods.extend(self.getListBarcodForFile(nom))
            elif 'Баркод' in self.dataForUpdateStocks.columns:
                listBarcods.extend(self.dataForUpdateStocks.Баркод.values.tolist())
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
            if self.sellerList == []:
                self.createMSGError("Не выбран ни один поставщик")
                return 0
            for seller in self.sellerList:
                pusher = ChangeAvailability(seller, self.getListBarcodForComboBox())
                resp = pusher.takeOn()
                if resp == 0:
                    self.ui.pushFullStocks.setStyleSheet('background: rgb(0,255,0);')
                    #self.createMSGSuc("{}".format(self.ui.selectNomenclatureComboBox.currentText()))
                else:
                    self.ui.pushFullStocks.setStyleSheet('background: rgb(255,0,0);')
                    #self.createMSGError("{}".format(self.ui.selectNomenclatureComboBox.currentText()))


    def pushEmptyStocks(self):
        listBarcods = []
        if not self.ui.selectNomenclatureComboBox.isEnabled():
            self.dataForUpdateStocks = pandas.DataFrame(pandas.read_excel(self.fileUpdateStokcsName))
            if 'Номенклатура' in self.dataForUpdateStocks.columns:
                for nom in self.dataForUpdateStocks.Номенклатура:
                    listBarcods.extend(self.getListBarcodForFile(nom))
            elif 'Баркод' in self.dataForUpdateStocks.columns:
                listBarcods.extend(self.dataForUpdateStocks.Баркод.values.tolist())
            else:
                self.createMSGError("Некорректный файл со списком номенклатуры или ШК.")
                return 0
            if listBarcods == []:
                self.createMSGError("Список ШК пуст.")
                return 0
            self.getSeller()
            for seller in self.sellerList:
                pusher = ChangeAvailability(seller, listBarcods)
                resp = pusher.takeOff()
                if resp == 0:
                    self.ui.pushEmptyStocks.setStyleSheet('background: rgb(0,255,0);') 
                    #self.createMSGSuc("{}".format(self.fileUpdateStokcsName))
                else: 
                    self.ui.pushEmptyStocks.setStyleSheet('background: rgb(255,0,0);')
                    #self.createMSGError("{}".format(self.fileUpdateStokcsName))
        else:
            self.getSeller()
            if self.sellerList == []:
                self.createMSGError("Не выбран ни один поставщик")
                return 0
            for seller in self.sellerList:
                pusher = ChangeAvailability(seller, self.getListBarcodForComboBox())
                resp = pusher.takeOff()
                if resp == 0:
                    self.ui.pushEmptyStocks.setStyleSheet('background: rgb(0,255,0);') 
                    #self.createMSGSuc("{}".format(self.ui.selectNomenclatureComboBox.currentText()))
                else: 
                    self.ui.pushEmptyStocks.setStyleSheet('background: rgb(255,0,0);')
                    #self.createMSGError("{}".format(self.ui.selectNomenclatureComboBox.currentText()))


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
