from getNomenclatures.ClassGetNomenclatures import nomenclaturesGetter
from getDB.ClassGetDB import getDB
from getListCards.ClassGetListCards import getListCards
import multiprocessing
import time
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from ui.ui_managerUI import Ui_Form
import os
import pandas

class Manager(QMainWindow):
    def __init__(self, parent=None) -> None:
        super(Manager, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.ui.updateDbBtn.clicked.connect(self.updateDb)
        self.ui.addFilterStringBtn.clicked.connect(self.addFilterString)
        self.ui.getLisCardsToFilterBtn.clicked.connect(self.getLisCardsToFilter)
        self.filterTypeComboBoxList = [] # 0 column dor filter, 1 type filter, 2 value textEdit, 3 value comboBox
        self.DB = ''
        self.index = 1
        self.startY_1 = 50
        self.delta = 25
        self.startX = 10
        self.space = 10
        self.width_ = 170
        self.height_ = 20
        self.listColumnForFilter = []
        self.listValuesColumns = {}
        self.createFilterLables()
        self.addFilterString()

        
    def getLisCardsToFilter(self):
        filter = []
        dataPath = QFileDialog.getExistingDirectory(self, ("Выберите место для сохранения"))
        for comboBox in self.filterTypeComboBoxList:
            column = comboBox[0].currentText()
            typeFilter = comboBox[1].currentText()
            if (typeFilter == 'Равно') or typeFilter == 'Не равно':
                value = comboBox[3].currentText()
            else:
                value = comboBox[2].currentText()
            filter.append([column, value])
        flterMain = self.ui.filterType.currentText()
        getter = getListCards(filter,self.DB,typeFilter,flterMain)
        data = getter.getListCards()
        data.to_excel(os.path.join(dataPath, 'tmp.xlsx'), index=False)


    def hideFilterTypeComboBox(self):
        for comboBox in self.filterTypeComboBoxList:
            if comboBox[1].currentText() in ['Равно', 'Не равно']:
                comboBox[2].hide()
                comboBox[3].show()
            else:
                comboBox[2].show()
                comboBox[3].hide()


    def fillFilterTextComboBox(self):
        if len(self.listValuesColumns)!=0:
            for comboBox in self.filterTypeComboBoxList:   
                comboBox[3].clear()   
                comboBox[3].addItems(self.listValuesColumns[comboBox[0].currentText()])


    def createListValuesColumns(self):
        for item in self.listColumnForFilter:
            listValues = []
            data = {'':['']}
            self.listValuesColumns.update(data)
            for value in self.DB[item].unique().tolist():
                listValues.append(str(value))
            listValues.sort()
            data = {item:listValues}
            self.listValuesColumns.update(data)
        self.fillFilterTextComboBox()


    def addFilterString(self):
        self.createFilterElements()
        self.index += 1
        self.updateComdoBoxFilter()


    def createFilterElements(self):
        if len(self.filterTypeComboBoxList)<=6:
            comboBox_0 = self.createFilterComboBox(self.index, 'filterColumsComboBox_{}', (self.startX, self.startY_1+self.delta*self.index, self.width_,self.height_))
            comboBox_1 = self.createFilterComboBox(self.index, 'filterTypeComboBox_{}', (self.startX+self.width_+self.space, self.startY_1+self.delta*self.index, self.width_,self.height_), items=['Равно', 'Не равно', 'Содержит', 'Не содержит'])
            textEdit = self.createFilterTextEdit(self.index, 'filterTextTextEdit_{}', (self.startX+self.width_*2+self.space*2, self.startY_1+self.delta*self.index, self.width_,self.height_))
            comboBox_2 = self.createFilterComboBox(self.index, 'filterTextComboBox_{}', (self.startX+self.width_*2+self.space*2, self.startY_1+self.delta*self.index, self.width_,self.height_))
            comboBox_0.setEditable(True)
            comboBox_0.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
            comboBox_0.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
            comboBox_1.setEditable(True)
            comboBox_1.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
            comboBox_1.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
            comboBox_2.setEditable(True)
            comboBox_2.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
            comboBox_2.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
            self.filterTypeComboBoxList.append((comboBox_0, comboBox_1, textEdit, comboBox_2))
            comboBox_1.currentIndexChanged.connect(self.hideFilterTypeComboBox)
            comboBox_0.currentIndexChanged.connect(self.fillFilterTextComboBox)


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


    def updateComdoBoxFilter(self):
        for comboBox in self.filterTypeComboBoxList:
            if len(self.listColumnForFilter) !=0:
                self.listColumnForFilter.sort()
                comboBox[0].addItem('')
                comboBox[0].addItems(self.listColumnForFilter)


    def updateDb(self):
        getterDB = getDB()
        self.DB = getterDB.getDB()
        self.listColumnForFilter = self.DB.columns.values.tolist()
        self.updateComdoBoxFilter()
        self.createListValuesColumns()
        self.listColumnForFilter
            




if __name__ =='__main__':
    app = QtWidgets.QApplication([])
    application = Manager()
    application.show()

    sys.exit(app.exec())