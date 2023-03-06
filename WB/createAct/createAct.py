from PyQt6 import QtWidgets, QtGui, QtCore
import os
import pickle
from datetime import datetime, timedelta
from ui.ui_CreateAct import Ui_CreateAct
from AdClass import Supplies, Acts



class createAct(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(createAct, self).__init__(parent)
        self.ui = Ui_CreateAct()
        self.ui.setupUi(self)
        self.ui.lineEditScan.returnPressed.connect(self.scan)
        self.ui.lineEditScan.returnPressed.connect(self.scan)
        self.ui.pushButtonCreateActs.clicked.connect(self.createActs)
        self.ui.tableWidgetSupp.insertColumn(0)
        self.ui.tableWidgetSupp.insertColumn(1)
        self.dateNow = datetime.now().date()
        self.fileSuppsName = f'{self.dateNow}_supp.pkl'
        self.pathTofileSupps = os.path.join(os.environ['LOCALAPPDATA'],self.fileSuppsName)
        self.ui.tableWidgetSupp.setHorizontalHeaderLabels(['ИП', 'Номер поставки'])
        self.data = {'Караханян':[],
                    'Самвел':[],
                    'Манвел':[],
                    'Федоров':[],
                    }
        # self.ui.statusbar.setStyleSheet('font-size: 14px')
        # self.ui.tableWidgetSupp.resizeColumnsToContents()


    def createActs(self):
        ordersFilePath = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения Актов", directory=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
        self.ui.statusbar.showMessage('Создание актов...')
        self.ui.statusbar.setStyleSheet("font-size: 20px; color: black")
        for ip, supplIdList in self.data.items():
            if len(supplIdList) !=0:
                Acts(ip, supplIdList).createActs(ordersFilePath)
        self.ui.statusbar.showMessage('Акты созданы')
        self.ui.statusbar.setStyleSheet("font-size: 20px; color: green")
        # act.createActs

    def createDB(self):
        with open(self.pathTofileSupps, 'wb') as file:
            pickle.dump(self.data, file)
            file.close()


    def scan(self):
        supplId = self.ui.lineEditScan.text().strip().replace('ЦИ', 'WB').replace('ПШ', 'GI')
        self.ui.lineEditScan.clear()
        self.ui.lineEditScan.setFocus()
        supp = Supplies()
        if ip:=supp.isExistsSupp(supplId):
            self.addToView(ip, supplId)
            self.createDB()
        else:
            self.ui.statusbar.showMessage('Поставка не найдена')
            self.ui.statusbar.setStyleSheet("font-size: 20px; color: red")

        # self.addToView('test', 'supplId')

    def startInitial(self):
        for key, values in self.data.items():
            if len(values) != 0:
                for value in values:
                    self.addToView(key, value)


    def addToView(self, ip, supplId):
        rowCount = self.ui.tableWidgetSupp.rowCount()
        if not self.ui.tableWidgetSupp.findItems(supplId, QtCore.Qt.MatchFlag.MatchExactly):
            self.ui.tableWidgetSupp.insertRow(rowCount)
            self.ui.tableWidgetSupp.setItem(rowCount,0,QtWidgets.QTableWidgetItem(ip))
            self.ui.tableWidgetSupp.setItem(rowCount,1,QtWidgets.QTableWidgetItem(supplId))
            self.data[ip].append(supplId)
            self.ui.tableWidgetSupp.resizeColumnsToContents()
            self.ui.statusbar.showMessage('Поставка добавлена')
            self.ui.statusbar.setStyleSheet("font-size: 20px; color: green")
        else:
            self.ui.statusbar.showMessage('Поставка уже добавлена')
            self.ui.statusbar.setStyleSheet("font-size: 20px; color: red")