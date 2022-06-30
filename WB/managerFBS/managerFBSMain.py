import multiprocessing
import sys
from os import listdir
from os.path import join as joinPath, isdir, isfile, abspath, exists
sys.path.append(abspath(joinPath(__file__,'../../..')))
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from ui.managerFBSUi import Ui_Form
from Class.GetListCardClass import GetlistCard
from Class.CreateDataBaseClass import CreateDataBase
from Class.PushStocksClass import PushStocks
from Class.PushPriceClass import PushPrice
from Class.FilterNomenclaturesClass import FilterNomenclatures



# pyuic5 E:\MyProduct\Python\WB\managerFBS\ui\managerFBSUi.ui -o E:\MyProduct\Python\WB\managerFBS\ui\managerFBSUi.py


class managerUI(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(managerUI, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.dataBase = ''
        self.ui.UpdateData.clicked.connect(self.updateData)
        self.ui.PushPrice.clicked.connect(self.pushPrice)
        self.ui.PushStocks.clicked.connect(self.pushStocks)


    def createMSGError(self,text):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setText(text)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.exec_()


    def createMSGSuc(self,text):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Успешно")
        msg.setText(text)
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.exec_()


    def updateData(self):
        self.ui.UpdateData.setEnabled(False)
        self.ui.UpdateData.setText('Выполняю...')
        QApplication.processEvents()
        seller = self.ui.sellerSelector.currentText()
        getlistCard = GetlistCard(seller)
        ListCard = getlistCard.getListCard()
        self.dataBase = CreateDataBase(ListCard)
        self.dataBase.getAddin()
        self.ui.brandSelector.addItems(self.dataBase.brandList)
        self.ui.modelSelector.addItems(self.dataBase.modelList)
        self.ui.colorSelector.addItems(self.dataBase.colorList)
        self.ui.cameraSelector.addItems(self.dataBase.cameraTypeList)
        self.ui.printCategorySelector.addItems(self.dataBase.categoryList)
        self.ui.UpdateData.setEnabled(True)
        self.ui.UpdateData.setText('Обновить данные')
        

    def pushPrice(self):
        seller = self.ui.sellerSelector.currentText()
        price = self.ui.price.toPlainText()
        discount = self.ui.discount.toPlainText()
        brandFilter = self.ui.brandSelector.currentText()
        modelFilter = self.ui.modelSelector.currentText()
        colorFilter = self.ui.colorSelector.currentText()
        cameraFilter = self.ui.cameraSelector.currentText()
        categoryFilter = self.ui.printCategorySelector.currentText()
        filter = FilterNomenclatures(brandFilter, modelFilter, colorFilter, cameraFilter, categoryFilter, self.dataBase.nomenclaturesList)
        filter.getnmIdList()
        pirce = PushPrice(seller, price, discount, filter)
        pirce.pushPrice()



    def pushStocks(self):
        seller = self.ui.sellerSelector.currentText()
        availability = int(self.ui.availability.toPlainText())
        brandFilter = self.ui.brandSelector.currentText()
        modelFilter = self.ui.modelSelector.currentText()
        colorFilter = self.ui.colorSelector.currentText()
        cameraFilter = self.ui.cameraSelector.currentText()
        categoryFilter = self.ui.printCategorySelector.currentText()
        filter = FilterNomenclatures(brandFilter, modelFilter, colorFilter, cameraFilter, categoryFilter, self.dataBase.nomenclaturesList)
        filter.getBarcodsList()
        stocks = PushStocks(seller, availability, filter)
        stocks.pushStocks()



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
    application = managerUI()
    application.show()

    sys.exit(app.exec())


