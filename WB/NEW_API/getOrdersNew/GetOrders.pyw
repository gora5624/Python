from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtCore import QDate#, QThread, QDir
from ui.ui_GetOrders import Ui_GetOrders
import sys
from  datetime import datetime
# import time
import os
# from queue import Queue
# from threading import Thread
# from multiprocessing import Process
from my_class import OrdersGetter, WorkerQueue
#sys.path.append(r'D:\\Python')
# from my_mod.autorz import token
from autorz import token
import pandas as pd
from os.path import join as joinPath
import gc


class GetOrdersMainWindows(QMainWindow):
    def __init__(self, parent=None) -> None:
        super(GetOrdersMainWindows, self).__init__(parent)
        self.ui = Ui_GetOrders()
        self.ui.setupUi(self)
        # Установить в dateEditTo текущую дату
        self.ui.dateEditTo.setDate(QDate.currentDate())
        # Установить в dateEditFrom дату 2 дня назад
        self.ui.dateEditFrom.setDate(QDate.currentDate().addDays(-2))
        self.deactiveCheck()
        self.ui.pushButtonSaveToExcel.clicked.connect(self.getOrders)
        self.ui.checkBoxSaveSKU.stateChanged.connect(self.deactiveCheck)
        self.ui.checkBoxRAW.stateChanged.connect(self.deactiveCheck)
        self.ui.checkBoxAllSellers.stateChanged.connect(self.deactiveCheck)
        self.ui.checkBoxInsertNom.stateChanged.connect(self.deactiveCheck)
        self.ordersData = pd.DataFrame()
        # сделать фон главного окна белый
        # self.setStyleSheet("background-color: rgb(255, 255, 255);")
        # сделать скругления на кнопке 10 px
        # self.ui.pushButtonSaveToExcel.setStyleSheet("border-radius: 10px;")

        #self.ui.pushButtonSaveToExcel.setStyleSheet("border-radius: 10px;background-color: red; ")
        # self.ui.pushButtonSaveToExcel.setStyleSheet("border-width: 10px;")



    def deactiveCheck(self):
        if self.ui.checkBoxSaveSKU.isChecked():
            self.ui.checkBoxRAW.setEnabled(False)
            self.ui.checkBoxRAW.setChecked(False)
        else:
            self.ui.checkBoxRAW.setEnabled(True)
        if self.ui.checkBoxRAW.isChecked():
            self.ui.checkBoxSaveSKU.setEnabled(False)
            self.ui.checkBoxSaveSKU.setChecked(False)
        else:
            self.ui.checkBoxSaveSKU.setEnabled(True)
        if  self.ui.checkBoxAllSellers.isChecked():
            self.ui.checkBoxKar.setEnabled(False)
            self.ui.checkBoxKar.setChecked(False)
            self.ui.checkBoxMan.setEnabled(False)
            self.ui.checkBoxMan.setChecked(False)
            self.ui.checkBoxSam.setEnabled(False)
            self.ui.checkBoxSam.setChecked(False)
            self.ui.checkBoxFed.setEnabled(False)
            self.ui.checkBoxFed.setChecked(False)
        else:
            self.ui.checkBoxKar.setEnabled(True)
            self.ui.checkBoxMan.setEnabled(True)
            self.ui.checkBoxSam.setEnabled(True)
            self.ui.checkBoxFed.setEnabled(True)
        if not self.ui.checkBoxInsertNom.isChecked():
            self.ui.checkBoxConsolid.setEnabled(False)
            self.ui.checkBoxConsolid.setChecked(False)
        else:
            self.ui.checkBoxConsolid.setEnabled(True)


    def getSellers(self):
        sellers = []
        if self.ui.checkBoxAllSellers.isChecked():
            sellers.extend(["Караханян", "Манвел", "Самвел", "Федоров"])
        if self.ui.checkBoxKar.isChecked():
            sellers.append("Караханян")
        if self.ui.checkBoxMan.isChecked():
            sellers.append("Манвел")    
        if self.ui.checkBoxSam.isChecked():
            sellers.append("Самвел")
        if self.ui.checkBoxFed.isChecked():
            sellers.append("Федоров")
        return sellers
        # sellers = Queue()
        # if self.ui.checkBoxAllSellers.isChecked():
        #     for seller in ["Караханян", "Манвел", "Самвел", "Федоров"]:
        #         sellers.put(seller)
        #     #sellers.put(x for x in ["Караханян", "Манвел", "Самвел", "Федоров"])
        # if self.ui.checkBoxKar.isChecked():
        #     sellers.put("Караханян")
        # if self.ui.checkBoxMan.isChecked():
        #     sellers.put("Манвел")    
        # if self.ui.checkBoxSam.isChecked():
        #     sellers.put("Самвел")
        # if self.ui.checkBoxFed.isChecked():
        #     sellers.put("Федоров")
        # return sellers
    

    def getOrders(self):
        # Если checkBoxAllSellerInOne активен, то собираем заказы всех продавцов в один файл, иначе разбиваем на разные файлы с названием продавца:
        self.sellers = self.getSellers()
        if self.sellers == []:
            QMessageBox.warning(self, 'Ошибка', 'Не выбрано ни одно ИП')
            self.ui.statusBar.setStyleSheet("color: red")
            self.ui.statusBar.showMessage('Не выбрано ни одно ИП')
            return
        listThreads = []
        # спрашиваем путь у пользователя для сохранения файла, по умолчанию на рабочий стол, имя файла по умолчанию Заказы
        ordersFilePath = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения файла", directory=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
        # Вывести сообщение об ошибке что ordersFilePath указан неверно и не продолжать выполнение кода
        if not ordersFilePath:
            QMessageBox.warning(self, 'Ошибка', 'Неверно указан путь к файлу')
            self.ui.statusBar.setStyleSheet("color: red")
            self.ui.statusBar.showMessage('Неверно указан путь к файлу')
            return
        putNomFlag = self.ui.checkBoxInsertNom.isChecked()
        allInOneFlag = self.ui.checkBoxAllSellerInOne.isChecked()
        rawDataFlag = self.ui.checkBoxRAW.isChecked()	
        saveSKUFlag = self.ui.checkBoxSaveSKU.isChecked()
        consolidFlag = self.ui.checkBoxConsolid.isChecked()
        self.ui.statusBar.setStyleSheet("color: black")
        self.ui.statusBar.showMessage('Идет выгрузка заказов...')
        QApplication.processEvents()
        self.ordersData = pd.DataFrame()
        for seller in self.sellers:
            allInOneFlag = self.ui.checkBoxAllSellerInOne.isChecked()
            params = {
            'ordersFilePath': ordersFilePath,
            'seller': seller,
            'putNom': putNomFlag,
            'allInOne': allInOneFlag,
            'rawData': rawDataFlag,
            'saveSKU': saveSKUFlag,
            'consolid': consolidFlag,
                    }
            # p = Process(target=self.getOrdersSellerProcess, kwargs=params, daemon=False)
            p = WorkerQueue(self.getOrdersSellerProcess, **params)
            listThreads.append(p)
            p.start()
        [p.join() for p in listThreads]
        # [p.terminate() for p in listThreads]
        if self.ui.checkBoxAllSellerInOne.isChecked():
            self.ui.statusBar.setStyleSheet("color: black")
            self.ui.statusBar.showMessage('Идет сохранение в файл...')
            QApplication.processEvents()
            self.saveOrders(self.ordersData, ordersFilePath)
        self.ui.statusBar.setStyleSheet("color: green")
        self.ui.statusBar.showMessage('Готово!')
        QApplication.processEvents()

          

    # С помощью pandas сохраняем заказы в файл а выбранную папку на диске:
    def saveOrders(self, orders, ordersFilePath):
        df = pd.DataFrame(orders)
        # Если в файле более милиона строк то сохраняем в csv, если меньше то в xlsx:
        date = datetime.now().date().strftime('%d.%m.%Y')
        if df.shape[0] > 1000000:
            df.to_csv(joinPath(ordersFilePath, f'Общий от {date}.csv'), index=False, sep='\t')
        else:
            df.to_excel(joinPath(ordersFilePath, f'Общий от {date}.xlsx'), index=False)


    def getOrdersSellerProcess(self, ordersFilePath, seller, allInOne, putNom, rawData, saveSKU, consolid):
        ordersGetter = OrdersGetter(seller, ordersFilePath, allInOne, putNom, rawData, saveSKU, consolid)
        ordersGetter.getOrders(token(seller), self.ui.dateEditFrom.date().toPyDate(), self.ui.dateEditTo.date().toPyDate())
        if allInOne:
            self.ordersData = pd.concat([self.ordersData, ordersGetter.orders])

    
if __name__ == '__main__':
    app = QApplication([])
    application = GetOrdersMainWindows()
    application.show()
    sys.exit(app.exec())