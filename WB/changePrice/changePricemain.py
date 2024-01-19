import pickle
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import QThreadPool, Qt
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem, QApplication
from changePrice import Ui_ChangePrice
import os
import pandas as pd
import datetime

# pyuic6 D:\Python\WB\changePrice\changePrice.ui -o D:\Python\WB\changePrice\changePrice.py

class PrintHelper(QtWidgets.QMainWindow):

    def __init__(self,parent=None):
        # setup Ui
        super(PrintHelper, self).__init__(parent)
        self.ui = Ui_ChangePrice()
        self.ui.setupUi(self)

        # binding func to buttons
        self.ui.pushButtonChoisExcel.clicked.connect(self.openFileExcelFor1c)
        self.ui.updateDB.triggered.connect(self.updateDB)
        self.ui.updateTokens.triggered.connect(self.updateTokens)
        self.ui.lineEditSearchInTable.textChanged.connect(self.searhInTable)
        self.ui.pushButtonSortTable.clicked.connect(self.searchInTable)
        self.ui.pushButtoGetCurPrice.clicked.connect(self.getPrice)

        # declaration self var
        self.pathToExcelFor1CFile = ''
        self.listNomFromFile = ''
        self.dataFromFile = ''
        self.dbFromWB = ''
        self.tokens = ''
        self.listForGetPrice = []
        self.fileName = r'Изменение цен от {}'.format(datetime.datetime.now().strftime('%d.%m.%y'))

        self.getDB()
        self.initTable()
        self.getTokens()
    
    def openFileExcelFor1c(self):
        # open and validate "xlsx" file for 1c and add contents to temporary variable and then run func that get info from this file
        self.pathToExcelFor1CFile = QFileDialog.getOpenFileName(self, ("Выберите файл со списком номенклатуры из 1С"), r'C:\Users\Георгий\Documents\цены', ("Excel Files (*.xlsx)"))[0]
        if not self.pathToExcelFor1CFile:
            QMessageBox.warning(self,'Не выбран файл', 'Файл Excel не выбран')
            return
        else:
            self.ui.statusbar.showMessage('Идёт чтение файла...')
            QApplication.processEvents()
            try:
                self.dataFromFile = pd.DataFrame(pd.read_excel(self.pathToExcelFor1CFile))
                # check colums in file
                try:
                    self.listNomFromFile = self.dataFromFile['Номенклатура'].unique().tolist()
                except KeyError:
                    QMessageBox.warning(self,'Ошибка', 'Отсуствует столбец "Номенклатура" в файле.')
                    self.pathToExcelFor1CFile = ''
                    return
                try:
                    self.listNomFromFile = self.dataFromFile['Штрихкод']
                except KeyError:
                    QMessageBox.warning(self,'Ошибка', 'Отсуствует столбец "Штрихкод" в файле.')
                    self.pathToExcelFor1CFile = ''
                    return
            except:
                QMessageBox.warning(self,'Ошибка', 'При чтении файла возникла непредвиденная ошибка.')
            self.ui.statusbar.showMessage('Файл прочитан, получение информации из файла...')
            QApplication.processEvents()
        self.getInfomationFromExcelFile()


    def getInfomationFromExcelFile(self):
        # get list nomenclatures form file, get barcodes list from file and add to temporary variable and then run func that fill in table on UI
        df = self.createAndSaveXLSX()
        self.listNomFromFile = df['Номенклатура'].unique().tolist()
        self.listUniqueNom = df.loc[:, ['Номенклатура', 'ИП']].drop_duplicates().to_dict('records')#.fillna('Абр./Нет')
        self.ui.statusbar.showMessage('Заполняю таблицу...')
        QApplication.processEvents()
        self.fillIninformationInUI()


    def createAndSaveXLSX(self):
        df = pd.DataFrame(pd.read_excel(self.pathToExcelFor1CFile))
        df = df.merge(self.dbFromWB,'left', left_on='Штрихкод', right_on='Последний баркод')
        df = df.dropna(subset=['ИП'])
        df = df.loc[:, ['Номенклатура', 'ИП', 'Артикул WB','Артикул продавца','Последний баркод']]
        df.insert(2,'Бренд','Mobi711')
        df.insert(3,'Категория','Чехлы для телефонов') 
        df.insert(7,'Остатки WB',0)
        df.insert(8,'Остатки продавца',0)
        df.insert(9,'Оборачиваемость',0)
        df.insert(10,'Текущая цена',0)
        df.insert(11,'Новая цена',0)
        df.insert(12,'Текущая скидка',0)
        df.insert(13,'Новая скидка',0)
        writer = pd.ExcelWriter(os.path.join(os.path.dirname(self.pathToExcelFor1CFile),'ДЛЯ ЗАГРУЗКИ {}'.format(os.path.basename(self.pathToExcelFor1CFile))), engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']
        redF = workbook.add_format({'bg_color': '#FFC7CE',
                               'font_color': '#9C0006'})
        greenF = workbook.add_format({'bg_color': '#C6EFCE',
                               'font_color': '#006100'})
        worksheet.conditional_format(1, 11, len(df), 11,
                                    {'type':     'cell',
                                     'criteria': '=',
                                     'value':    0,
                                    'format':   redF})
        worksheet.conditional_format(1, 13, len(df), 13,
                                    {'type':     'cell',
                                    'criteria': '=',
                                    'value':    0,
                                    'format':   redF})
        worksheet.conditional_format(1, 11, len(df), 11,
                                    {'type':     'cell',
                                     'criteria': '>',
                                     'value':    0,
                                    'format':   greenF})
        worksheet.conditional_format(1, 13, len(df), 13,
                                    {'type':     'cell',
                                    'criteria': '>',
                                    'value':    0,
                                    'format':   greenF})
        worksheet.conditional_format(0, 0, len(df), 1,
                                    {'type':     'no_errors',
                                    # 'criteria': '>',
                                    # 'value':    'all',
                                    'format':   redF})
        writer.close()
        return df


    def initTable(self):
        self.ui.tableWidgetListNom.clear()
        self.ui.tableWidgetListNom.insertColumn(0)
        self.ui.tableWidgetListNom.setHorizontalHeaderItem(0, QTableWidgetItem('Номенклатура'))
        self.ui.tableWidgetListNom.insertColumn(1)
        self.ui.tableWidgetListNom.setHorizontalHeaderItem(1, QTableWidgetItem('Текущая цена'))
        self.ui.tableWidgetListNom.insertColumn(2)
        self.ui.tableWidgetListNom.setHorizontalHeaderItem(2, QTableWidgetItem('Текущая скидка'))
        self.ui.tableWidgetListNom.insertColumn(3)
        self.ui.tableWidgetListNom.setHorizontalHeaderItem(3, QTableWidgetItem('Текущая цена с учетом скидки'))
        self.ui.tableWidgetListNom.insertColumn(4)
        self.ui.tableWidgetListNom.setHorizontalHeaderItem(4, QTableWidgetItem('Новая цена'))
        self.ui.tableWidgetListNom.insertColumn(5)
        self.ui.tableWidgetListNom.setHorizontalHeaderItem(5, QTableWidgetItem('Новая скидка'))
        self.ui.tableWidgetListNom.insertColumn(6)
        self.ui.tableWidgetListNom.setHorizontalHeaderItem(6, QTableWidgetItem('Новая цена с учетом скидки'))
        self.ui.tableWidgetListNom.insertColumn(0)
        self.ui.tableWidgetListNom.setHorizontalHeaderItem(0, QTableWidgetItem('ИП'))


    def fillIninformationInUI(self):
        # get info from temporary var and display it interface
        # if not s:
        for i, item in enumerate(self.listUniqueNom):
            self.ui.tableWidgetListNom.insertRow(i)
            self.ui.tableWidgetListNom.setItem(i, 0, QTableWidgetItem(item['ИП']))
            self.ui.tableWidgetListNom.setItem(i, 1, QTableWidgetItem(item['Номенклатура']))
            self.ui.tableWidgetListNom.setItem(i, 2, QTableWidgetItem('Ещё не получено'))
            self.ui.tableWidgetListNom.setItem(i, 3, QTableWidgetItem('Ещё не получено'))
            self.ui.tableWidgetListNom.setItem(i, 4, QTableWidgetItem('Ещё не получено'))
            self.ui.tableWidgetListNom.setItem(i, 5, QTableWidgetItem('Заполните поле'))
            self.ui.tableWidgetListNom.setItem(i, 6, QTableWidgetItem('Заполните поле'))
            self.ui.tableWidgetListNom.setItem(i, 7, QTableWidgetItem('Заполните поле'))
        # else:
        #     for i, item in enumerate(self.listUniqueNom):
        #         if s in item['Номенклатура']:
        #             self.ui.tableWidgetListNom.insertRow(i)
        #             self.ui.tableWidgetListNom.setItem(i, 0, QTableWidgetItem(item['ИП']))
        #             self.ui.tableWidgetListNom.setItem(i, 1, QTableWidgetItem(item['Номенклатура']))
        #             self.ui.tableWidgetListNom.setItem(i, 2, QTableWidgetItem('Ещё не получено'))
        #             self.ui.tableWidgetListNom.setItem(i, 3, QTableWidgetItem('Ещё не получено'))
        #             self.ui.tableWidgetListNom.setItem(i, 4, QTableWidgetItem('Ещё не получено'))
        #             self.ui.tableWidgetListNom.setItem(i, 5, QTableWidgetItem('Заполните поле'))
        #             self.ui.tableWidgetListNom.setItem(i, 6, QTableWidgetItem('Заполните поле'))
        #             self.ui.tableWidgetListNom.setItem(i, 7, QTableWidgetItem('Заполните поле'))
        # self.ui.tableWidgetListNom.sortByColumn(1, QtCore.Qt.SortOrder.AscendingOrder)
        self.ui.tableWidgetListNom.resizeColumnsToContents()
        self.ui.tableWidgetListNom.setSortingEnabled(True)
        self.ui.statusbar.showMessage('Готово...')
        QApplication.processEvents()


    def searchInTable(self):
         [self.ui.tableWidgetListNom.hideRow(i) for i in range(self.ui.tableWidgetListNom.rowCount())]
         searchStr = self.ui.lineEditSearchInTable.text()
         matchItems = self.ui.tableWidgetListNom.findItems(searchStr, Qt.MatchFlag.MatchContains)
         for item in matchItems:
              self.ui.tableWidgetListNom.showRow(item.row())


    def searhInTable(self):
        s = self.ui.lineEditSearchInTable.text() 
        matchRows = self.ui.tableWidgetListNom.findItems(s,Qt.MatchFlag.MatchContains) #| Qt.MatchFlag.MatchFixedString)
        self.ui.tableWidgetListNom.setCurrentItem(None)
        if matchRows:
            item = matchRows[0]  # take the first
            self.ui.tableWidgetListNom.setCurrentItem(item)
    

    def getDB(self):
        with open(os.path.join(os.path.dirname(__file__),'dataBase.pkl'), 'rb') as fileDBTMP:
            self.dbFromWB = pickle.load(fileDBTMP)
            fileDBTMP.close()
        # df2 = pd.DataFrame(pd.read_table(r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_nom Манвел.txt"))
        # dfTMP = pd.DataFrame(pd.read_table(r"C:\Users\Георгий\Desktop\ШК.txt"))
        # dfnew = pd.DataFrame({'Артикул WB':df2['nmID'],
        #                       'Артикул продавца':df2['vendorCode'],
        #                       'Последний баркод':df2['sku'],})
        # dfnew.insert(0,'ИП', 'Манвел')
        # dfnew = pd.concat([dfnew,self.dbFromWB])
        # dfnew.to_excel(r"C:\Users\Георгий\Desktop\tmp.xlsx", index=False)
    

    def getPrice(self):
         
         for i in range(self.ui.tableWidgetListNom.rowCount()):
            if self.ui.tableWidgetListNom.isRowHidden(i):
                 continue
            else:
                self.listForGetPrice.append(
                     {
                          'ИП': self.ui.tableWidgetListNom.item(i,0),
                          'Номенклатура': self.ui.tableWidgetListNom.item(i,1)
                     }
                )
                self.ui.tableWidgetListNom.item(i,1)


    def getTokens(self):
         with open(os.path.join(os.path.dirname(__file__),'tokens.pkl'), 'rb') as fileTokens:
              self.tokens = pickle.load(fileTokens)
              fileTokens.close()


    def updateTokens(self):
        pathTotokens = QFileDialog.getOpenFileName(self, ("Выберите файл с токенами"), os.path.expanduser('~/Desktop'), ("Excel Files (*.xlsx)"))[0]
        with open(os.path.join(os.path.dirname(__file__),'tokens.pkl'), 'wb') as fileTokens:
             pickle.dump(pd.read_excel(pathTotokens).to_dict('records')[0], fileTokens)
             fileTokens.close()      


    def updateDB(self):
        with open(os.path.join(os.path.dirname(__file__),'dataBase.pkl'), 'rb') as fileDBTMP:
                    a = pickle.load(fileDBTMP)
                    a
                    fileDBTMP.close()
        pathToDBTMPKar = r"F:\Downloads\Караханян цены.xlsx"
        pathToDBTMPSam = r"F:\Downloads\Самвел цены.xlsx"
        pathToDBTMPFed = r"F:\Downloads\Федоров цены.xlsx"
        dfTMPKar = pd.DataFrame(pd.read_excel(pathToDBTMPKar))
        dfTMPSam = pd.DataFrame(pd.read_excel(pathToDBTMPSam))
        dfTMPFed = pd.DataFrame(pd.read_excel(pathToDBTMPFed))
        dfTMPKar.insert(0,'ИП', 'Караханян')
        dfTMPSam.insert(0,'ИП', 'Самвел')
        dfTMPFed.insert(0,'ИП', 'Федоров')
        # dbFromWB = [
        #     {
        #         "Seller":'Караханян',
        #         'db':dfTMPKar.loc[:, ['Артикул WB','Артикул продавца','Последний баркод']]
        #         },
        #     {
        #         'Seller':'Самвел',
        #         'db':dfTMPSam.loc[:, ['Артикул WB','Артикул продавца','Последний баркод']]
        #         },
        #     {
        #         "Seller":'Федоров',
        #         'db':dfTMPFed.loc[:, ['Артикул WB','Артикул продавца','Последний баркод']]
        #         }
        #     
        #         ]
        
        dbFromWB = pd.concat([dfTMPKar,dfTMPSam,dfTMPFed])
        with open(os.path.join(os.path.dirname(__file__),'dataBase.pkl'), 'wb') as fileDBTMP:
                    pickle.dump(dbFromWB, fileDBTMP)
                    fileDBTMP.close()


if __name__ =='__main__':
    app = QtWidgets.QApplication([])
    application = PrintHelper()
    application.show()
    app.exec()

    # def updateDB(self):
    # with open(os.path.join(os.path.dirname(__file__),'dataBase.pkl'), 'rb') as fileDBTMP:
    #             a = pickle.load(fileDBTMP)
    #             a
    #             fileDBTMP.close()
    # pathToDBTMPKar = r"F:\Downloads\Караханян цены.xlsx"
    # pathToDBTMPSam = r"F:\Downloads\Самвел цены.xlsx"
    # pathToDBTMPFed = r"F:\Downloads\Федоров цены.xlsx"
    # dfTMPKar = pd.DataFrame(pd.read_excel(pathToDBTMPKar)).loc[:, ['Артикул WB','Артикул продавца','Последний баркод']]
    # dfTMPSam = pd.DataFrame(pd.read_excel(pathToDBTMPSam)).loc[:, ['Артикул WB','Артикул продавца','Последний баркод']]
    # dfTMPFed = pd.DataFrame(pd.read_excel(pathToDBTMPFed)).loc[:, ['Артикул WB','Артикул продавца','Последний баркод']]
    # dfTMPKar.insert(0,'ИП', 'Караханян')
    # dfTMPSam.insert(0,'ИП', 'Самвел')
    # dfTMPFed.insert(0,'ИП', 'Федоров')
    # dbFromWB = pd.concat([dfTMPKar,dfTMPSam,dfTMPFed])
    # with open(os.path.join(os.path.dirname(__file__),'dataBase.pkl'), 'wb') as fileDBTMP:
    #             pickle.dump(dbFromWB, fileDBTMP)
    #             fileDBTMP.close()
     
    # with open(os.path.join(os.path.dirname(__file__),'dataBase.pkl'), 'rb') as fileDBTMP:
    #     dbFromWB = pickle.load(fileDBTMP)
    #     fileDBTMP.close()
    # df2 = pd.DataFrame(pd.read_table(r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_nom Манвел.txt"))
    # dfTMP = pd.DataFrame(pd.read_table(r"C:\Users\Георгий\Desktop\ШК.txt"))
    # dfnew = pd.DataFrame({'Артикул WB':df2['nmID'],
    #                         'Артикул продавца':df2['vendorCode'],
    #                         'Последний баркод':df2['sku'],})
    # dfnew.insert(0,'ИП', 'Манвел')
    # dfnew = pd.concat([dfnew,dbFromWB])
    # with open(os.path.join(os.path.dirname(__file__),'dataBase.pkl'), 'wb') as fileDBTMP:
    #     pickle.dump(dfnew, fileDBTMP)
    #     fileDBTMP.close()