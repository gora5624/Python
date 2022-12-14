from getNomenclatures.ClassGetNomenclatures import nomenclaturesGetter

import multiprocessing
import time
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from ui.ui_managerUI import Ui_Form
import os

class Manager(QMainWindow):
    def __init__(self, parent=None) -> None:
        super(Manager, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.ui.updateDbBtn.clicked.connect(self.updateDb)
        self.ui.addFilterStringBtn.clicked.connect(self.addFilterString)
        self.filterTypeComboBoxList = []
        self.index = 1
        self.startY_1 = 50
        self.delta = 25
        self.startX = 10
        self.space = 10
        self.width_ = 170
        self.height_ = 20
        self.createFilterLables()
        self.addFilterString()

        


    def filterTypeComboBox(self):
        for comboBox in self.filterTypeComboBoxList:
            if comboBox[0].currentText() in ['Равно', 'Не равно']:
                comboBox[1].hide()
                comboBox[2].show()
            else:
                comboBox[1].show()
                comboBox[2].hide()


    def addFilterString(self):
        self.createFilterElements()
        self.index += 1


    def createFilterElements(self):
        self.createFilterComboBox(self.index, 'filterColumsComboBox_{}', (self.startX, self.startY_1+self.delta*self.index, self.width_,self.height_))
        comboBox_1 = self.createFilterComboBox(self.index, 'filterTypeComboBox_{}', (self.startX+self.width_+self.space, self.startY_1+self.delta*self.index, self.width_,self.height_), items=['Равно', 'Не равно', 'Содержит', 'Не содержит'])
        textEdit = self.createFilterTextEdit(self.index, 'filterTextTextEdit_{}', (self.startX+self.width_*2+self.space*2, self.startY_1+self.delta*self.index, self.width_,self.height_))
        comboBox_2 = self.createFilterComboBox(self.index, 'filterTextComboBox_{}', (self.startX+self.width_*2+self.space*2, self.startY_1+self.delta*self.index, self.width_,self.height_))
        self.filterTypeComboBoxList.append((comboBox_1, textEdit, comboBox_2))
        comboBox_1.currentTextChanged.connect(self.filterTypeComboBox)


    def createFilterTextEdit(self, index, objectName, size):
        textEdit = QTextEdit(self)
        textEdit.setObjectName(objectName.format(index))
        textEdit.setGeometry(QtCore.QRect(*size))
        textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # textEdit.show()
        return textEdit


    def createFilterComboBox(self, index, objectName, size, items=''):
        comboBox = QComboBox(self)
        comboBox.setObjectName(objectName.format(index))
        comboBox.setGeometry(QtCore.QRect(*size))
        if items !='':
           comboBox.addItems(items)
        comboBox.show()
        return comboBox


    def createFilterLables(self):
        self.createFilterLable(self.index, 'filterColumsLabel_{}', 'Выберите поле для фильтрации', (self.startX,self.startY_1*self.index,self.width_,self.height_))
        self.createFilterLable(self.index, 'filterTypeLabel_{}', 'Тип фильтра', (self.startX+self.width_+self.space,self.startY_1*self.index,self.width_,self.height_))
        self.createFilterLable(self.index, 'filterTextLabel_{}', 'Текст для фильтра', (self.startX+self.width_*2+self.space*2,self.startY_1*self.index,self.width_,self.height_))


    def createFilterLable(self,index, objectName, text, size):
        lable = QLabel(self)
        lable.setObjectName(objectName.format(index))
        lable.setText(text)
        lable.setGeometry(QtCore.QRect(*size))
        lable.show()


    def updateDb(self):
        for file in os.listdir(self.pathToDb)




if __name__ =='__main__':
    app = QtWidgets.QApplication([])
    application = Manager()
    application.show()

    sys.exit(app.exec())