import multiprocessing
import sys
from os import listdir, makedirs
from os.path import join as joinPath, isdir, isfile, abspath, exists
sys.path.append(abspath(joinPath(__file__,'../../..')))
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication
from my_mod.my_lib import file_exists
# импортируем интерфейс
from ui.ui_MakeBookPrintUi import Ui_Form
# импортируем дополнительные скрипты
from Moduls.makeImageBookWithNameModel import makeImageBookWithNameModel, makeImageBookWithNameModelNew, makeImageBookWithNameModelNew2
from Moduls.AddSkriptForMakeBookImage import createExcel, deleteImage
from Moduls.makeImageBookWithNameModel import copyImage as copyBooks
from Moduls.makeImageSilicon import createAllSiliconImage, fakecreateAllSiliconImage
from Folders import pathToDoneBookImageWithName, pathToMaskFolderSilicon, pathToDoneSiliconImageSilicon, pathToTopPrint, pathToTopPrintSkin
from Moduls.AddSkriptForMakeSiliconImage import createExcelSilicon, markerForAllModel, chekImage, siliconCaseColorDict, CreateExcelForFolder
from Moduls.GetCardAsincio import getListCard
# импортируем дополнительные классы
from Class.MyClassForMakeImage import ModelWithAddin
from Class.Create_copy import WBnomenclaturesCreater
from Class.CreateCartholders import WBnomenclaturesCreaterHolders
from Class.MakePlastinsClass import MakePlastins
import pandas
from Class.CreateExists_copy import ExistsNomenclaturesCreater
import os



# pyuic5 E:\MyProduct\Python\WB\MakePrint\ui\MakeBookPrintUi.ui -o E:\MyProduct\Python\WB\MakePrint\ui\ui_MakeBookPrintUi.py


class mameBookPrint(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(mameBookPrint, self).__init__(parent)
        self.bookName = 'Книжки'
        self.siliconName = 'Силикон'
        self.listModelForExcel = []
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.tabWidget.setTabVisible(2,False)
        self.ui.tabWidget.setTabVisible(3,False)
        self.ui.ChekMask.hide()
        self.ui.label_4.hide()
        self.ui.AddPhotoSelector.hide()
        self.ui.SiliconeMode.hide()
        self.ui.CreateSiliconImage.hide()
        self.ui.CreatePrint.clicked.connect(self.btnMakeBookPrint)
        self.ui.tabWidget.tabBarClicked.connect(self.fillSiliconMaskList)
        self.ui.tabWidget.tabBarClicked.connect(self.updeteListFile)
        self.ui.ChekMask.clicked.connect(self.fillSiliconMaskList)
        self.ui.CreateSiliconImage.clicked.connect(self.btnCreateSiliconImage)
        self.ui.CreateSiliconImageTop.clicked.connect(self.btnCreateSiliconImageTop)
        self.ui.CreateExcelForSilicon.clicked.connect(self.btnCreateExcelForSilicon)
        self.ui.ChekImage.clicked.connect(self.btnChekImage)
        self.ui.ChekImageAll.clicked.connect(self.ChekImageAll)
        # self.ui.ApplyAddin.clicked.connect(self.btnApplyAddin)
        self.ui.ApplyAddinFromFile.clicked.connect(self.btnApplyAddinFromFile)
        self.ui.CreateCase.clicked.connect(self.btnCreateCase)
        self.ui.CreateCaseAll.clicked.connect(self.btnCreateCaseAll)
        # self.ui.updateListModel.clicked.connect(self.updateModelList)
        self.ui.makePlastinsBut.clicked.connect(self.makeplastins)
        # self.ui.ClearAddin.clicked.connect(self.crearAdiin)
        # self.ui.CreateDB.clicked.connect(self.crateDB)
        self.ui.chooseExistsCardsBtn.clicked.connect(self.chooseExistsCardsBtn)
        self.ui.makeCartholdersButt.clicked.connect(self.btnCreateCartholders)
        self.tokenAb = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njk1MSwiaWQiOiIyMzUyZGFmYS05NTdhLTQ0MzAtYWFhMi1lZGM5NDZkZDY0ODEiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjUyNzczNiwicyI6MTAsInNpZCI6ImFhNDdlNDg5LTU5ZTAtNDIzMi1hMWJmLTBlMTIzOWYwNDJmMSIsInVpZCI6NDUzMjI5MjB9.j9s_VtDpTEWceEd1vUTWf6uofUuSY30q0UrR-H047qZE40sb8atwtAviABB7eoeLQdu3T69UosBdn_Bvj2-2ZQ'   
        self.tokenIvan = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5NzAwNywiaWQiOiI1ZWRjMWY0Ni04OWVhLTQxMzktYjVjYi1hNDM5OGUwMzUxNTMiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjExNzEwNDQsInMiOjEwLCJzaWQiOiJkOWU0OGUxZi05ZjgxLTQ1MmMtODRiYy05ZGYxZWRiMzNmNDkiLCJ1aWQiOjQ1MzIyOTIwfQ.y2sbT8zqvoM-iSxKJcsdiEphMoLRfNq8pBsIQnmGQIbc1btCIoe7Qkz65Ur91fVEqyDbQZ-Ry_1tTkgof5hKDw'
        self.tokenKar = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njg4MiwiaWQiOiI4YjEzZWUzOC03MGIxLTQ3ZjgtYTdlNC03OTIzY2Q2ZmQ3ZTciLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjEwMTA2MiwicyI6MTAsInNpZCI6IjNhOTNkZGMxLWFhNTctNWMyYi05YzVjLWRkZDIyMTg4OTQ0MCIsInVpZCI6NDUzMjI5MjB9.DXm6RuooUieyrnNdXr3FfPPdwK5uV4aiTF5SZIryJUhbQW4uScXQLEb-n8p0iM3RT6Js6aVKijiyOkawE6r76g'
        self.tokenSam = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njk3MiwiaWQiOiJjZWE4ZTNmYy1iYzg5LTRjYjktYmNmNy0xN2ZiNmNjNzk1MTQiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjgxOTI0NiwicyI6MTAsInNpZCI6IjBhYjhiMTA1LTA1MWYtNGVkNi04NzBiLTM5OWU3NWUxMDI4NiIsInVpZCI6NDUzMjI5MjB9.bOmPtl_ZXx-1C25-5CbftPJVQuuHzwG5iH9QUx0x8CdZCjI9ZnbFgMU1ijL-lfgn_N1JxPvojV2dBrKTpDnolw'
        self.pathToSiliconCLRAddin = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиСиликонПроз.xlsx'
        self.pathToPlasticAddin = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиПластик.xlsx'
        self.pathToSiliconMTAddin = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиСиликонМат.xlsx'
        self.pathToCardhonlderAddin = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиКардхолдер.xlsx' 
        self.pathToNewPoketAddin = r"E:\MyProduct\Python\WB\MakePrint\ХарактеристикиNewPoket.xlsx"
        self.pathToBookAddin = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиКнижки.xlsx'
        self.pathToBookAddin = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиКнижкиNew.xlsx'
        self.pathToPrintAddin = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиПринтов.xlsx'
        self.pathToSkinShell = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиSkinShell.xlsx'
        self.pathToSkinShell = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиSkinShellNew.xlsx'
        self.pathToCategoryPrint = r'E:\MyProduct\Python\WB\MakePrint\cat.xlsx'
        self.pathToAddinFile = ''
        self.topPrint = ''
        self.ui.toExistsCardsChek.setChecked(True)
        self.dfExistCase = ''
        self.updeteListFile()
        # self.crateDB()
        # self.tstcomp()
        # self.updateModelList()

    def tstcomp(sekl):
        tmpComp = pandas.read_excel(r"F:\Маски силикон\Новое книги.xlsx")
        listNom = tmpComp.Номенклатура.unique().tolist()
        for i in listNom:
            for dir in os.listdir(r'\\192.168.0.33\shared\_Общие документы_\Егор\Архив принтов xlsx'):
                if (i+'.xlsx') in os.listdir(os.path.join(r'\\192.168.0.33\shared\_Общие документы_\Егор\Архив принтов xlsx', dir)):
                    compTMP = pandas.read_excel(os.path.join(r'\\192.168.0.33\shared\_Общие документы_\Егор\Архив принтов xlsx', dir,(i+'.xlsx'))).Совместимость.unique().tolist()[0]
                    tmpComp.loc[tmpComp['Номенклатура']==i, 'Совместимость'] = compTMP
        tmpComp.to_excel(r"F:\Маски силикон\Новое книги.xlsx")





    def crateDB(self):
        pdSNewPoketAddin = pandas.DataFrame(pandas.read_excel(self.pathToNewPoketAddin))
        # pdSilsiconCLRAddin = pandas.DataFrame(pandas.read_excel(self.pathToSiliconCLRAddin))
        # pdPlasticAddin = pandas.DataFrame(pandas.read_excel(self.pathToPlasticAddin))
        # pdSilsiconMTAddin = pandas.DataFrame(pandas.read_excel(self.pathToSiliconMTAddin))
        # pdSkinShellAddin = pandas.DataFrame(pandas.read_excel(self.pathToSkinShell))
        # pdCardhonlderAddin = pandas.DataFrame(pandas.read_excel(self.pathToCardhonlderAddin))
        # pdPrintAddin = pandas.DataFrame(pandas.read_excel(self.pathToPrintAddin))
        # pdCategoryPrint = pandas.DataFrame(pandas.read_excel(self.pathToCategoryPrint))
        # pdBookAddin = pandas.DataFrame(pandas.read_excel(self.pathToBookAddin))
        # pdSilsiconCLRAddin.to_csv(self.pathToSiliconCLRAddin.replace('xlsx','txt'),index=None,sep='\t')
        pdSNewPoketAddin.to_csv(self.pathToNewPoketAddin.replace('xlsx','txt'),index=None,sep='\t')
        # pdPlasticAddin.to_csv(self.pathToPlasticAddin.replace('xlsx','txt'),index=None,sep='\t')
        # pdSilsiconMTAddin.to_csv(self.pathToSiliconMTAddin.replace('xlsx','txt'),index=None,sep='\t')
        # pdSkinShellAddin.to_csv(self.pathToSkinShell.replace('xlsx','txt'),index=None,sep='\t')
        # pdBookAddin.to_csv(self.pathToBookAddin.replace('xlsx','txt'),index=None,sep='\t')
        # pdCardhonlderAddin.to_csv(self.pathToCardhonlderAddin.replace('xlsx','txt'),index=None,sep='\t')
        # pdPrintAddin.to_csv(self.pathToPrintAddin.replace('xlsx','txt'),index=None,sep='\t')
        # pdCategoryPrint.to_csv(self.pathToCategoryPrint.replace('xlsx','txt'),index=None,sep='\t')


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


    def makeplastins():
        MakePlastins.makePlastin()


    def crearAdiin(self):
        self.listModelForExcel = []

    def ChekImageAll(self):
        pathToDoneFilesForUplaodsPhoto = QFileDialog.getExistingDirectory(self, ("Выберите папку с файлами"), r'F:\Для загрузки\Готовые принты')
        # fileName = self.ui.FileSelector.currentText()
        mode = self.ui.IPSelector.currentText()
        for file in listdir(pathToDoneFilesForUplaodsPhoto):
        # force = self.ui.ForceUpdate.checkState() 
            if not isdir(joinPath(pathToDoneFilesForUplaodsPhoto,file)):
                if mode =='Караханян':
                    token = self.tokenKar
                elif mode =='Абраамян':
                    token = self.tokenAb
                elif mode =='Самвел':
                    token = self.tokenSam
                elif mode =='Иван':
                    token = self.tokenIvan
                WBnomenclaturesCreater.uplaodImage(joinPath(pathToDoneFilesForUplaodsPhoto,file), token)


    def btnChekImage(self):
        fileName = self.ui.FileSelector.currentText()
        mode = self.ui.IPSelector.currentText()
        # force = self.ui.ForceUpdate.checkState() 
        if mode =='Караханян':
            token = self.tokenKar
        elif mode =='Абраамян':
            token = self.tokenAb
        elif mode =='Самвел':
            token = self.tokenSam
        elif mode =='Иван':
            token = self.tokenIvan
        WBnomenclaturesCreater.uplaodImage(joinPath(pathToDoneSiliconImageSilicon,fileName), token)


    def updeteListFile(self):
        self.ui.FileSelector.clear()
        for item in listdir(pathToDoneSiliconImageSilicon):
            if isfile(joinPath(pathToDoneSiliconImageSilicon,item)):
                if '~' not in item:
                    self.ui.FileSelector.addItem(item)


    def btnCreateCaseAll(self):
        pathToDoneSiliconImageSilicon = QFileDialog.getExistingDirectory(self, ("Выберите папку с файлами"), r'F:\Для загрузки\Готовые принты')
        mode = self.ui.IPSelector.currentText()
        if mode =='Караханян':
            DBpath = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Караханян.txt'
        elif mode =='Абраамян':
            DBpath = r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Манвел.txt"
        elif mode =='Самвел':
            DBpath = r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Самвел2.txt"
        elif mode =='Иван':
            DBpath = r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Федоров.txt"
        tmpDB = pandas.read_table(DBpath)
        for file in listdir(pathToDoneSiliconImageSilicon):
            if not isdir(joinPath(pathToDoneSiliconImageSilicon, file)):
                pathToFileForUpload = joinPath(pathToDoneSiliconImageSilicon, file)
                if '.db' not in pathToFileForUpload and '~' not in pathToFileForUpload and '1C_' not in pathToFileForUpload:
                    if not self.ui.toExistsCardsChek.isChecked():
                        if not isdir(pathToFileForUpload):
                            create = WBnomenclaturesCreater()
                            create.pathToFileForUpload = pathToFileForUpload
                            create.createNomenclaturesMultiporocessing(mode)
                    else:
                        if not isdir(pathToFileForUpload):
                            start_time = time.time()
                            data = pandas.DataFrame(pandas.read_excel(pathToFileForUpload))
                            tmp = ExistsNomenclaturesCreater(data, mode, pathToFileForUpload)
                            tmp.dataFromDB = tmpDB
                            pool = multiprocessing.Pool(1)
                            # pool.apply_async(ExistsNomenclaturesCreater.uplaodImage, args=(pathToFileForUpload, mode,))
                            pool.apply_async(tmp.start(), args=(pathToFileForUpload, mode,))
                            pool.close()
                            pool.join()
                            print("--- %s seconds ---" % (time.time() - start_time))
        self.ui.CreateCaseAll.setStyleSheet("background-color : green")



    def btnCreateCartholders(self):
            pathToFile = QFileDialog.getOpenFileName(self, ("Выберите файл свойств"), "", ("xlsx files (*.xlsx)"))[0]
            create = WBnomenclaturesCreaterHolders()
            pathToFileForUpload = joinPath(pathToFile)
            create.pathToFileForUpload = pathToFileForUpload
            mode = self.ui.IPSelector.currentText()
            create.createNomenclaturesMultiporocessing(mode)


    def btnCreateCase(self):
        fileName = self.ui.FileSelector.currentText()
        pathToFileForUpload = joinPath(pathToDoneSiliconImageSilicon, fileName)
        mode = self.ui.IPSelector.currentText()
        if mode =='Караханян':
            DBpath = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Караханян.txt'
        elif mode =='Абраамян':
            DBpath = r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Манвел.txt"
        elif mode =='Самвел':
            DBpath = r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Самвел2.txt"
        elif mode =='Иван':
            DBpath = r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Федоров.txt"
        tmpDB = pandas.read_table(DBpath)
        if not self.ui.toExistsCardsChek.isChecked():
            create = WBnomenclaturesCreater()
            create.pathToFileForUpload = pathToFileForUpload
            create.createNomenclaturesMultiporocessing(mode)
        else:
            start_time = time.time()
            data = pandas.DataFrame(pandas.read_excel(pathToFileForUpload))
            tmp = ExistsNomenclaturesCreater(data, mode, pathToFileForUpload)
            if mode =='Караханян':
                DBpath = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Караханян.txt'
            elif mode =='Абраамян':
                DBpath = r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Манвел.txt"
            elif mode =='Самвел':
                DBpath = r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Самвел2.txt"
            elif mode =='Иван':
                DBpath = r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Федоров.txt"
            tmp.dataFromDB = tmpDB
            pool = multiprocessing.Pool(2)
            # pool.apply_async(ExistsNomenclaturesCreater.uplaodImage, args=(pathToFileForUpload, mode,))
            pool.apply_async(tmp.start(), args=(pathToFileForUpload, mode,))
            pool.close()
            pool.join()
            print("--- %s seconds ---" % (time.time() - start_time))
          

    def fillSiliconMaskList(self, tabIndex):
        self.ui.textSiliconMask.setText('')
        if tabIndex  == 1 or tabIndex  == False:
            negFlag = False
            for mask in listdir(pathToMaskFolderSilicon):
                if isdir(joinPath(pathToMaskFolderSilicon, mask)):
                    #color = self.detectColor(mask)
                    #if 'Thumbs.db' not in color:
                    fileList = listdir(joinPath(pathToMaskFolderSilicon, mask))
                    if 'mask.png' in fileList and 'fon.png' in fileList:
                        continue
                    elif 'mask.png' not in fileList and 'fon.png' not in fileList:
                        self.ui.textSiliconMask.setText(self.ui.textSiliconMask.toPlainText() + mask + ' НЕТ МАКСИ И ФОНА\n')
                        negFlag = True
                        continue
                    elif 'mask.png' not in fileList and 'fon.png' in fileList:
                        self.ui.textSiliconMask.setText(self.ui.textSiliconMask.toPlainText() + mask + ' НЕТ МАКСИ\n')
                        negFlag = True
                        continue
                    elif 'mask.png' in fileList and 'fon.png' not in fileList:
                        self.ui.textSiliconMask.setText(self.ui.textSiliconMask.toPlainText() + mask + ' НЕТ ФОНА\n')
                        negFlag = True
                        continue
            if not negFlag:
                for mask in listdir(pathToMaskFolderSilicon):
                    self.ui.textSiliconMask.setText(mask + '\n')
                self.ui.textSiliconMask.setText('Все маски готовы к работе\n')
    

    def checkColorBox(self):
        listColor = []
        for i in range(self.ui.splitterColor.count()):
            statusCheckBox = self.ui.splitterColor.widget(i).checkState()
            if statusCheckBox:
                listColor.append(self.ui.splitterColor.widget(i).text())
        if len(listColor) == 0:
            self.createMSGError('Не выбран ни один цвет!')
            return 0
        return listColor


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


    # def updateModelList(self):
    #     # self.ui.ModelSelector.clear()
    #     # self.ui.ModelSelector.addItem(markerForAllModel)
    #     if exists(pathToDoneSiliconImageSilicon):
    #         listModel = listdir(pathToDoneSiliconImageSilicon)
    #         for model in listModel:
    #             for maskFolder in listdir(pathToMaskFolderSilicon):
    #                 if isdir(joinPath(pathToMaskFolderSilicon, maskFolder)):
    #                     if model in maskFolder:
    #                         if isdir(joinPath(pathToMaskFolderSilicon,model)):
    #                             self.ui.ModelSelector.addItem(model)
    #     if exists(pathToDoneBookImageWithName):
    #         listModel = listdir(pathToDoneBookImageWithName)
    #         for model in listModel:
    #             if isdir(joinPath(pathToDoneBookImageWithName,model)):
    #                 self.ui.ModelSelector.addItem(model)

    def makeFakeDirsWithMask(self):
        pathToFile = QFileDialog.getOpenFileName(self, 'Выберите файл со свойствами', r'F:\Маски силикон', '*.xlsx',)[0]
        for i in pandas.DataFrame(pandas.read_excel(pathToFile))['Номенклатура'].unique().tolist():
            makedirs(joinPath(pathToMaskFolderSilicon, i), exist_ok=True)


    def btnCreateSiliconImage(self):
        addImage = self.ui.AddPhotoSelector.currentText()
        mode = 'all' if self.ui.SiliconeMode.checkState() == 2 else 'withOutBack'
        if self.ui.FakeModeChekBox.checkState() == 2:
            self.makeFakeDirsWithMask()
            fakecreateAllSiliconImage(pathToMaskFolderSilicon, mode)
        else:
            createAllSiliconImage(pathToMaskFolderSilicon,6, addImage, mode)
        # self.updateModelList()


    def btnCreateSiliconImageTop(self):
        addImage = self.ui.AddPhotoSelector.currentText()
        mode = 'all'
        countPrint = self.ui.countPrints.value()
        # if 'SkinShell'.lower() not in pathToMaskFolderSilicon.lower(): 
        #     self.topPrint = pandas.DataFrame(pandas.read_excel(pathToTopPrint))[0:countPrint]# ['Принт'].values.tolist()
        # else:
        #     self.topPrint = pandas.DataFrame(pandas.read_excel(pathToTopPrintSkin))[0:countPrint]# ['Принт'].values.tolist()
        if self.ui.FakeModeChekBox.checkState() == 2:
            self.makeFakeDirsWithMask()
            fakecreateAllSiliconImage(pathToMaskFolderSilicon, mode, countPrint=countPrint)
        else:
            createAllSiliconImage(pathToMaskFolderSilicon,6, addImage, mode, countPrint=countPrint)
        # self.updateModelList()


    def chooseExistsCardsBtn(self):
        pathToListExistCaseFile = QFileDialog.getOpenFileName(self, ("Выберите файл с существующими карточками"), r"F:\Маски силикон", ("xlsx files (*.xlsx)"))[0]
        if not pathToListExistCaseFile:
            QtWidgets.QMessageBox.warning('Файл с карточками ВБ не выбран')
            return
        self.ui.chooseExistsCardsBtn.setText(pathToListExistCaseFile)
        countCase = 0
        for case in listdir(pathToDoneSiliconImageSilicon):
            if isdir(pathTMP:=joinPath(pathToDoneSiliconImageSilicon,case)):
                countCase+= len(listdir(pathTMP))
        if '.txt' in pathToListExistCaseFile:
            self.dfExistCase = pandas.DataFrame(pandas.read_table(pathToListExistCaseFile, sep='\t'))
        elif '.xlsx' in pathToListExistCaseFile:
            self.dfExistCase = pandas.DataFrame(pandas.read_excel(pathToListExistCaseFile))
        countExistsCase = self.dfExistCase.shape[0]
        if countExistsCase>countCase:
            print('Количестов существующих артикулов ({}) больше чем нужно ({}>{}), будут использованы не все'.format(countExistsCase, countExistsCase, countCase))
            self.ui.toExistsCardsChek.setChecked(True)
        elif countExistsCase<countCase:
            print('Количестов существующих артикулов ({}) меньше чем нужно ({}<{}), добавьте строки в документ'.format(countExistsCase, countExistsCase, countCase))
            return 0
        else:
            self.ui.toExistsCardsChek.setChecked(True)
        self.ui.chooseExistsCardsBtn.setStyleSheet("background-color : green")

        


    def btnApplyAddinFromFile(self):
        # print('tst')
        self.pathToAddinFile = QFileDialog.getOpenFileName(self, ("Выберите файл с совместимостью"), r'F:\Маски силикон', ("xlsx files (*.xlsx)"))[0]
        if not self.pathToAddinFile:
            QtWidgets.QMessageBox.warning('файл с совместимостью не выбран')
            return 
        self.ui.ApplyAddinFromFile.setText(self.pathToAddinFile)
        dfAddinFile = pandas.DataFrame(pandas.read_excel(self.pathToAddinFile))
        existsFlag = self.ui.toExistsCardsChek.isChecked()
        counter = 0
        for case in listdir(pathToDoneSiliconImageSilicon):
            if case[-4:] =='проз':
                maskNew = case.replace('проз', 'проз.')
            elif case[-3:] == 'мат':
                maskNew = case.replace('мат', 'мат.')
            else:
                maskNew = case
            try:
                if isdir(pathTMP:=joinPath(pathToDoneSiliconImageSilicon, case)):
                    delta = len(listdir(pathTMP))
                    if existsFlag:
                        if 'vendorCode' in self.dfExistCase:
                            listDataVendorCode = self.dfExistCase['vendorCode'].values.tolist()[counter:counter+delta]
                        elif 'Артикул товара' in self.dfExistCase:
                            listDataVendorCode = self.dfExistCase['Артикул товара'].values.tolist()[counter:counter+delta]
                        else:
                            listDataVendorCode = self.dfExistCase['Артикул продавца'].values.tolist()[counter:counter+delta]
                    counter+=delta
                    try:
                        compability = modelAddin = dfAddinFile[dfAddinFile['Номенклатура'] == maskNew]['Совместимость'].values.tolist()[0]
                    except IndexError:
                        compability = modelAddin = dfAddinFile[dfAddinFile['Номенклатура'] == case]['Совместимость'].values.tolist()[0]
                    # brand = self.ui.textSiliconBrand.toPlainText()
                    if self.ui.IPSelector.currentText() == 'Иван':
                        brand = 'SuperPrint'
                    else:
                        brand = 'Mobi711'
                    try:
                        price = dfAddinFile[dfAddinFile['Номенклатура'] == maskNew]['Цена'].values.tolist()[0]
                    except IndexError:
                        price = dfAddinFile[dfAddinFile['Номенклатура'] == case]['Цена'].values.tolist()[0]
                    if existsFlag:
                        modelWithAddin = ModelWithAddin(brand, compability, modelAddin, price, case, pathToDoneSiliconImageSilicon, siliconCaseColorDict, existsFlag=existsFlag, listDataVendorCode=listDataVendorCode)
                    else:
                        modelWithAddin = ModelWithAddin(brand, compability, modelAddin, price, maskNew, pathToDoneSiliconImageSilicon, siliconCaseColorDict, existsFlag=existsFlag)
                    self.listModelForExcel.append(modelWithAddin)
            except:
                print('Для {} не удалось получить свойства.'.format(maskNew))
        self.ui.ApplyAddinFromFile.setStyleSheet("background-color : green")




    # def btnApplyAddin(self, curModel = False):
    #     # if curModel == False:
    #     #     curModel = self.ui.ModelSelector.currentText()
    #     # else:
    #     curModel = markerForAllModel
    #     listModel = []
    #     for i in range(1,self.ui.ModelSelector.count()):
    #         listModel.append(self.ui.ModelSelector.itemText(i))
    #     counter =0
    #     if curModel == markerForAllModel:
    #         existsFlag = self.ui.toExistsCardsChek.isChecked()
    #         self.listModelForExcel = []
    #         brand = self.ui.textSiliconBrand.toPlainText()
    #         compability = self.ui.textSiliconCompability.toPlainText()
    #         # name = self.ui.textSiliconName.toPlainText()
    #         modelAddin = self.ui.textSiliconModel.toPlainText()2
    #         price = self.ui.textPrice.toPlainText()
    #         for modelTMP in listModel:
    #             # model = modelTMP.replace(caseType,'').strip()
    #             delta = len(listdir(joinPath(pathToDoneSiliconImageSilicon, modelTMP)))
    #             if existsFlag:
    #                 listDataVendorCode = self.dfExistCase['vendorCode'].values.tolist()[counter:counter+delta]
    #             else:
    #                 listDataVendorCode = ''
    #             counter+=delta
    #             modelWithAddin = ModelWithAddin(brand, compability, modelAddin, price, modelTMP, pathToDoneSiliconImageSilicon, siliconCaseColorDict, existsFlag=existsFlag, listDataVendorCode=listDataVendorCode)
    #             # if caseType == self.bookName:
    #             #     modelWithAddin.colorList = listdir(joinPath(pathToDoneBookImageWithName, model.replace(caseType,'').strip()))
    #             # else:
    #             #     modelWithAddin.colorList = listdir(joinPath(pathToMaskFolderSilicon, model.replace(caseType,'').strip()))
    #             self.listModelForExcel.append(modelWithAddin)
    #             self.ui.textSiliconMask.setText('Все модели из списка записаны\n')
    #     else:
    #         if self.listModelForExcel != []:
    #             for i, item in enumerate(self.listModelForExcel):
    #                 # if item.model == curModel:
    #                     # if self.acceptEvent("Свойства для {} уже записаны, перезаписать?".format(item.model)):
    #                 delta = len(listdir(joinPath(pathToDoneSiliconImageSilicon, modelTMP)))
    #                 if existsFlag:
    #                     listDataVendorCode = self.dfExistCase['vendorCode'].values.tolist()[counter:counter+delta]
    #                 else:
    #                     listDataVendorCode = ''
    #                 counter+=delta
    #                 brand = self.ui.textSiliconBrand.toPlainText()
    #                 compability = self.ui.textSiliconCompability.toPlainText()
    #                 modelAddin = self.ui.textSiliconModel.toPlainText()
    #                 price = self.ui.textPrice.toPlainText()
    #                 self.listModelForExcel[i] = ModelWithAddin(brand, compability, modelAddin, price, curModel, pathToDoneSiliconImageSilicon, siliconCaseColorDict, existsFlag=existsFlag, listDataVendorCode=listDataVendorCode)

    #                 # self.listModelForExcel[i].colorList = listdir(joinPath(pathToMaskFolderSilicon, curModel.replace(caseType,'').strip()))
    #                 self.ui.textSiliconMask.setText(curModel+' перезаписана\n')
    #                 break
    #                     # else:
    #                     #     return None
    #             brand = self.ui.textSiliconBrand.toPlainText()
    #             compability = self.ui.textSiliconCompability.toPlainText()
    #             modelAddin = self.ui.textSiliconModel.toPlainText()
    #             price = self.ui.textPrice.toPlainText()
    #             modelWithAddin = ModelWithAddin(brand, compability, modelAddin, price, curModel, pathToDoneSiliconImageSilicon, siliconCaseColorDict, existsFlag=existsFlag, listDataVendorCode=listDataVendorCode)
    #             # modelWithAddin.colorList = listdir(joinPath(pathToMaskFolderSilicon, curModel.replace(caseType,'').strip()))
    #             self.listModelForExcel.append(modelWithAddin)
    #             self.ui.textSiliconMask.setText(curModel+' записан\n')
    #             return None
    #         else:
    #             brand = self.ui.textSiliconBrand.toPlainText()
    #             compability = self.ui.textSiliconCompability.toPlainText()
    #             modelAddin = self.ui.textSiliconModel.toPlainText()
    #             price = self.ui.textPrice.toPlainText()
    #             modelWithAddin = ModelWithAddin(brand, compability, modelAddin, price, curModel, pathToDoneSiliconImageSilicon, siliconCaseColorDict, existsFlag=existsFlag, listDataVendorCode=listDataVendorCode)
    #             # modelWithAddin.colorList = listdir(joinPath(pathToMaskFolderSilicon, curModel.replace(caseType,'').strip()))
    #             self.listModelForExcel.append(modelWithAddin)
    #             self.ui.textSiliconMask.setText(curModel+' записан\n')
    #             return None
        


    def btnCreateExcelForSilicon(self):
        addImage = self.ui.AddPhotoSelector.currentText()
        # if self.listModelForExcel == []:
        #     self.btnApplyAddin(True)
        # procList = []
        # for item in self.listModelForExcel:
        #     p = multiprocessing.Process(target=CreateExcelForFolder, args=(item, addImage, ))
        #     p.start()
        #     procList.append(p)
        # for p in procList:
        #     p.join()
        pool = multiprocessing.Pool()
        for item in self.listModelForExcel:
            pool.apply_async(CreateExcelForFolder, args=(item, self.topPrint, ))
        pool.close()
        pool.join()
        # for item in self.listModelForExcel:
        #     CreateExcelForFolder(item, self.topPrint)
        self.updeteListFile()
        self.ui.CreateExcelForSilicon.setStyleSheet("background-color : green")

    def btnMakeExcelClicked(self):
        resp = multiprocessing.Queue()
        resp.put(1)
        p = multiprocessing.Process(target=createExcel, args=(resp,))
        p.start()
        p.join()
        resp.get()
        if resp.get() == 0:
            self.createMSGSuc('Excel создан успешно!')
        else:
            self.createMSGError('Неизвестная ошибка при создании.')

    def btnMakeDeleteIamge(self):
        # deleteImage()
        pass


    def btnMakeBookPrint(self):
        # modelBrand = self.ui.textEditBrand.toPlainText()
        # if modelBrand == '':
        #     self.createMSGError('Поле бренд не заполенно!')
        #     #return 0
        # modelModel = self.ui.textEditModel.toPlainText()
        # if modelModel == '':
        #     self.createMSGError('Поле модель не заполенно!')
            #return 0
        colorList = self.checkColorBox()
        if colorList == 0:
            return 0
        # временный костыль, потом переделать
        for line in pandas.DataFrame(pandas.read_excel(r'F:\Маски силикон\Новое2.xlsx')).to_dict('records'):
            tmpListName = line['Номенклатура'].replace('Чехол книга ','').replace(' черный с сил. вставкой Fashion','').split(' ')
            modelBrand = tmpListName[0]
            modelModel = ' '.join(tmpListName[1:])
            if not self.ui.newDesignChek.checkState():
                p = multiprocessing.Process(target=makeImageBookWithNameModel, args=(colorList, modelBrand, modelModel,))
            else:
                p = multiprocessing.Process(target=makeImageBookWithNameModelNew2, args=(colorList, modelBrand, modelModel,))
            #self.ui.textLog.setText(self.ui.textLog.toPlainText() + modelBrand +' ' + modelModel + ' добавлен в очередь\n')
            p.start()
            p.join()
        copyBooks()



if __name__ =='__main__':
    app = QtWidgets.QApplication([])
    application = mameBookPrint()
    application.show()

    sys.exit(app.exec())

