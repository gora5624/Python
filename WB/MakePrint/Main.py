import multiprocessing
import sys
from os import listdir
from os.path import join as joinPath, isdir, isfile, abspath, exists
sys.path.append(abspath(joinPath(__file__,'../../..')))
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication
from my_mod.my_lib import file_exists
# импортируем интерфейс
from ui.ui_MakeBookPrintUi import Ui_Form
# импортируем дополнительные скрипты
from Moduls.makeImageBookWithNameModel import makeImageBookWithNameModel
from Moduls.AddSkriptForMakeBookImage import createExcel, deleteImage, copyImage
from Moduls.makeImageSilicon import createAllSiliconImage, fakecreateAllSiliconImage
from Folders import pathToDoneBookImageWithName, pathToMaskFolderSilicon, pathToDoneSiliconImageSilicon, pathToTopPrint
from Moduls.AddSkriptForMakeSiliconImage import createExcelSilicon, markerForAllModel, copyImage, chekImage, siliconCaseColorDict, CreateExcelForFolder
from Moduls.GetCardAsincio import getListCard
# импортируем дополнительные классы
from Class.MyClassForMakeImage import ModelWithAddin
from Class.Create import WBnomenclaturesCreater
from Class.CreateCartholders import WBnomenclaturesCreaterHolders
from Class.MakePlastinsClass import MakePlastins
import pandas
from Class.CreateExists import ExistsNomenclaturesCreater



# pyuic5 E:\MyProduct\Python\WB\MakePrint\ui\MakeBookPrintUi.ui -o E:\MyProduct\Python\WB\MakePrint\ui\MakeBookPrintUi.py


class mameBookPrint(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(mameBookPrint, self).__init__(parent)
        self.bookName = 'Книжки'
        self.siliconName = 'Силикон'
        self.listModelForExcel = []
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.CreatePrint.clicked.connect(self.btnMakeBookPrint)
        self.ui.tabWidget.tabBarClicked.connect(self.fillSiliconMaskList)
        self.ui.tabWidget.tabBarClicked.connect(self.updeteListFile)
        self.ui.ChekMask.clicked.connect(self.fillSiliconMaskList)
        self.ui.CreateSiliconImage.clicked.connect(self.btnCreateSiliconImage)
        self.ui.CreateSiliconImageTop.clicked.connect(self.btnCreateSiliconImageTop)
        self.ui.CreateExcelForSilicon.clicked.connect(self.btnCreateExcelForSilicon)
        self.ui.ChekImage.clicked.connect(self.btnChekImage)
        self.ui.ChekImageAll.clicked.connect(self.ChekImageAll)
        self.ui.ApplyAddin.clicked.connect(self.btnApplyAddin)
        self.ui.ApplyAddinFromFile.clicked.connect(self.btnApplyAddinFromFile)
        self.ui.CreateCase.clicked.connect(self.btnCreateCase)
        self.ui.CreateCaseAll.clicked.connect(self.btnCreateCaseAll)
        self.ui.updateListModel.clicked.connect(self.updateModelList)
        self.ui.makePlastinsBut.clicked.connect(self.makeplastins)
        self.ui.ClearAddin.clicked.connect(self.crearAdiin)
        self.ui.CreateDB.clicked.connect(self.crateDB)
        self.ui.chooseExistsCardsBtn.clicked.connect(self.chooseExistsCardsBtn)
        self.ui.makeCartholdersButt.clicked.connect(self.btnCreateCartholders)
        self.tokenAb = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'   
        self.tokenIvan = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImIxYjQ3YjQzLTFhMTYtNGQ0Ni1iZTA1LWRlY2ExZTcxMTU0MSJ9.qTIJF6fEgbRux3Ps30ciMQ802UWqtAER-y94ALvE3PI'
        self.tokenKar = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
        self.tokenSam = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
        self.pathToSiliconCLRAddin = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиСиликонПроз.xlsx'
        self.pathToPlasticAddin = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиПластик.xlsx'
        self.pathToSiliconMTAddin = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиСиликонМат.xlsx'
        self.pathToCardhonlderAddin = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиКардхолдер.xlsx'
        self.pathToBookAddin = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиКнижки.xlsx'
        self.pathToPrintAddin = r'E:\MyProduct\Python\WB\MakePrint\ХарактеристикиПринтов.xlsx'
        self.pathToCategoryPrint = r'E:\MyProduct\Python\WB\MakePrint\cat.xlsx'
        self.pathToAddinFile = ''
        self.topPrint = ''
        self.ui.toExistsCardsChek.setChecked(False)
        self.dfExistCase = ''
        self.updeteListFile()
        self.updateModelList()


    def crateDB(self):
        pdSilsiconCLRAddin = pandas.DataFrame(pandas.read_excel(self.pathToSiliconCLRAddin))
        pdPlasticAddin = pandas.DataFrame(pandas.read_excel(self.pathToPlasticAddin))
        pdSilsiconMTAddin = pandas.DataFrame(pandas.read_excel(self.pathToSiliconMTAddin))
        pdCardhonlderAddin = pandas.DataFrame(pandas.read_excel(self.pathToCardhonlderAddin))
        pdPrintAddin = pandas.DataFrame(pandas.read_excel(self.pathToPrintAddin))
        pdCategoryPrint = pandas.DataFrame(pandas.read_excel(self.pathToCategoryPrint))
        pdBookAddin = pandas.DataFrame(pandas.read_excel(self.pathToBookAddin))
        pdSilsiconCLRAddin.to_csv(self.pathToSiliconCLRAddin.replace('xlsx','txt'),index=None,sep='\t')
        pdPlasticAddin.to_csv(self.pathToPlasticAddin.replace('xlsx','txt'),index=None,sep='\t')
        pdSilsiconMTAddin.to_csv(self.pathToSiliconMTAddin.replace('xlsx','txt'),index=None,sep='\t')
        pdBookAddin.to_csv(self.pathToBookAddin.replace('xlsx','txt'),index=None,sep='\t')
        pdCardhonlderAddin.to_csv(self.pathToCardhonlderAddin.replace('xlsx','txt'),index=None,sep='\t')
        pdPrintAddin.to_csv(self.pathToPrintAddin.replace('xlsx','txt'),index=None,sep='\t')
        pdCategoryPrint.to_csv(self.pathToCategoryPrint.replace('xlsx','txt'),index=None,sep='\t')


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
        pathToDoneFilesForUplaodsPhoto = QFileDialog.getExistingDirectory(self, ("Выберите папку с файлами"))
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
        pathToDoneSiliconImageSilicon = QFileDialog.getExistingDirectory(self, ("Выберите папку с файлами"))
        mode = self.ui.IPSelector.currentText()
        for file in listdir(pathToDoneSiliconImageSilicon):
            if not isdir(joinPath(pathToDoneSiliconImageSilicon, file)):
                pathToFileForUpload = joinPath(pathToDoneSiliconImageSilicon, file)
                if not self.ui.toExistsCardsChek.isChecked():
                    create = WBnomenclaturesCreater()
                    create.pathToFileForUpload = pathToFileForUpload
                    create.createNomenclaturesMultiporocessing(mode)
                else:
                    start_time = time.time()
                    data = pandas.DataFrame(pandas.read_excel(pathToFileForUpload))
                    tmp = ExistsNomenclaturesCreater(data, mode, pathToFileForUpload)
                    pool = multiprocessing.Pool(2)
                    pool.apply_async(ExistsNomenclaturesCreater.uplaodImage, args=(pathToFileForUpload, mode,))
                    pool.apply_async(tmp.start(), args=(pathToFileForUpload, mode,))
                    pool.close()
                    pool.join()
                    print("--- %s seconds ---" % (time.time() - start_time))



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
        if not self.ui.toExistsCardsChek.isChecked():
            create = WBnomenclaturesCreater()
            create.pathToFileForUpload = pathToFileForUpload
            create.createNomenclaturesMultiporocessing(mode)
        else:
            start_time = time.time()
            data = pandas.DataFrame(pandas.read_excel(pathToFileForUpload))
            tmp = ExistsNomenclaturesCreater(data, mode, pathToFileForUpload)
            pool = multiprocessing.Pool(2)
            pool.apply_async(ExistsNomenclaturesCreater.uplaodImage, args=(pathToFileForUpload, mode,))
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


    def updateModelList(self):
        self.ui.ModelSelector.clear()
        self.ui.ModelSelector.addItem(markerForAllModel)
        if exists(pathToDoneSiliconImageSilicon):
            listModel = listdir(pathToDoneSiliconImageSilicon)
            for model in listModel:
                for maskFolder in listdir(pathToMaskFolderSilicon):
                    if isdir(joinPath(pathToMaskFolderSilicon, maskFolder)):
                        if model in maskFolder:
                            if isdir(joinPath(pathToMaskFolderSilicon,model)):
                                self.ui.ModelSelector.addItem(model)
        if exists(pathToDoneBookImageWithName):
            listModel = listdir(pathToDoneBookImageWithName)
            for model in listModel:
                if isdir(joinPath(pathToDoneBookImageWithName,model)):
                    self.ui.ModelSelector.addItem(model)


    def btnCreateSiliconImage(self):
        addImage = self.ui.AddPhotoSelector.currentText()
        mode = 'all' if self.ui.SiliconeMode.checkState() == 2 else 'withOutBack'
        if self.ui.FakeModeChekBox.checkState() == 2:
            fakecreateAllSiliconImage(pathToMaskFolderSilicon, mode)
        else:
            createAllSiliconImage(pathToMaskFolderSilicon,6, addImage, mode)
        self.updateModelList()


    def btnCreateSiliconImageTop(self):
        addImage = self.ui.AddPhotoSelector.currentText()
        mode = 'all'
        countPrint = self.ui.countPrints.value()
        self.topPrint = pandas.DataFrame(pandas.read_excel(pathToTopPrint))[0:countPrint]# ['Принт'].values.tolist()
        if self.ui.FakeModeChekBox.checkState() == 2:
            fakecreateAllSiliconImage(pathToMaskFolderSilicon, mode, topPrint=self.topPrint)
        else:
            createAllSiliconImage(pathToMaskFolderSilicon,6, addImage, mode, topPrint=self.topPrint)
        self.updateModelList()


    def chooseExistsCardsBtn(self):
        pathToListExistCaseFile = QFileDialog.getOpenFileName(self, ("Выберите файл с существующими карточками"), "", ("xlsx files (*.xlsx)"))[0]
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
        


    def btnApplyAddinFromFile(self):
        print('tst')
        self.pathToAddinFile = QFileDialog.getOpenFileName(self, ("Выберите файл свойств"), "", ("xlsx files (*.xlsx)"))[0]
        dfAddinFile = pandas.DataFrame(pandas.read_excel(self.pathToAddinFile))
        existsFlag = self.ui.toExistsCardsChek.isChecked()
        counter = 0
        for mask in listdir(pathToMaskFolderSilicon):
            if 'проз.' not in mask:
                maskNew = mask.replace('проз', 'проз.')
            if 'мат.' not in mask:
                maskNew = mask.replace('мат', 'мат.')
            try:
                if isdir(pathTMP:=joinPath(pathToDoneSiliconImageSilicon, mask)):
                    delta = len(listdir(pathTMP))
                    listDataVendorCode = self.dfExistCase['vendorCode'].values.tolist()[counter:counter+delta]
                    counter+=delta
                    try:
                        compability = modelAddin = dfAddinFile[dfAddinFile['Номенклатура'] == maskNew]['Совместимость'].values.tolist()[0]
                    except IndexError:
                        compability = modelAddin = dfAddinFile[dfAddinFile['Номенклатура'] == mask]['Совместимость'].values.tolist()[0]
                    brand = self.ui.textSiliconBrand.toPlainText()
                    price = dfAddinFile[dfAddinFile['Номенклатура'] == mask]['Цена'].values.tolist()[0]
                    modelWithAddin = ModelWithAddin(brand, compability, modelAddin, price, mask, pathToDoneSiliconImageSilicon, siliconCaseColorDict, existsFlag=existsFlag, listDataVendorCode=listDataVendorCode)
                    self.listModelForExcel.append(modelWithAddin)
            except:
                print('Для {} не удалось получить свойства.'.format(mask))




    def btnApplyAddin(self, curModel = False):
        if curModel == False:
            curModel = self.ui.ModelSelector.currentText()
        else:
            curModel = markerForAllModel
        listModel = []
        for i in range(1,self.ui.ModelSelector.count()):
            listModel.append(self.ui.ModelSelector.itemText(i))
        counter =0
        if curModel == markerForAllModel:
            existsFlag = self.ui.toExistsCardsChek.isChecked()
            self.listModelForExcel = []
            brand = self.ui.textSiliconBrand.toPlainText()
            compability = self.ui.textSiliconCompability.toPlainText()
            # name = self.ui.textSiliconName.toPlainText()
            modelAddin = self.ui.textSiliconModel.toPlainText()
            # cameraType = self.ui.CameraType.currentText()
            price = self.ui.textPrice.toPlainText()
            for modelTMP in listModel:
                # model = modelTMP.replace(caseType,'').strip()
                delta = len(listdir(joinPath(pathToDoneSiliconImageSilicon, modelTMP)))
                listDataVendorCode = self.dfExistCase['vendorCode'].values.tolist()[counter:counter+delta]
                counter+=delta
                modelWithAddin = ModelWithAddin(brand, compability, modelAddin, price, modelTMP, pathToDoneSiliconImageSilicon, siliconCaseColorDict, existsFlag=existsFlag, listDataVendorCode=listDataVendorCode)
                # if caseType == self.bookName:
                #     modelWithAddin.colorList = listdir(joinPath(pathToDoneBookImageWithName, model.replace(caseType,'').strip()))
                # else:
                #     modelWithAddin.colorList = listdir(joinPath(pathToMaskFolderSilicon, model.replace(caseType,'').strip()))
                self.listModelForExcel.append(modelWithAddin)
                self.ui.textSiliconMask.setText('Все модели из списка записаны\n')
        else:
            if self.listModelForExcel != []:
                for i, item in enumerate(self.listModelForExcel):
                    # if item.model == curModel:
                        # if self.acceptEvent("Свойства для {} уже записаны, перезаписать?".format(item.model)):
                    delta = len(listdir(joinPath(pathToDoneSiliconImageSilicon, modelTMP)))
                    listDataVendorCode = self.dfExistCase['vendorCode'].values.tolist()[counter:counter+delta]
                    counter+=delta
                    brand = self.ui.textSiliconBrand.toPlainText()
                    compability = self.ui.textSiliconCompability.toPlainText()
                    modelAddin = self.ui.textSiliconModel.toPlainText()
                    price = self.ui.textPrice.toPlainText()
                    self.listModelForExcel[i] = ModelWithAddin(brand, compability, modelAddin, price, curModel, pathToDoneSiliconImageSilicon, siliconCaseColorDict, existsFlag=existsFlag, listDataVendorCode=listDataVendorCode)

                    # self.listModelForExcel[i].colorList = listdir(joinPath(pathToMaskFolderSilicon, curModel.replace(caseType,'').strip()))
                    self.ui.textSiliconMask.setText(curModel+' перезаписана\n')
                    break
                        # else:
                        #     return None
                brand = self.ui.textSiliconBrand.toPlainText()
                compability = self.ui.textSiliconCompability.toPlainText()
                modelAddin = self.ui.textSiliconModel.toPlainText()
                price = self.ui.textPrice.toPlainText()
                modelWithAddin = ModelWithAddin(brand, compability, modelAddin, price, curModel, pathToDoneSiliconImageSilicon, siliconCaseColorDict, existsFlag=existsFlag, listDataVendorCode=listDataVendorCode)
                # modelWithAddin.colorList = listdir(joinPath(pathToMaskFolderSilicon, curModel.replace(caseType,'').strip()))
                self.listModelForExcel.append(modelWithAddin)
                self.ui.textSiliconMask.setText(curModel+' записан\n')
                return None
            else:
                brand = self.ui.textSiliconBrand.toPlainText()
                compability = self.ui.textSiliconCompability.toPlainText()
                modelAddin = self.ui.textSiliconModel.toPlainText()
                price = self.ui.textPrice.toPlainText()
                modelWithAddin = ModelWithAddin(brand, compability, modelAddin, price, curModel, pathToDoneSiliconImageSilicon, siliconCaseColorDict, existsFlag=existsFlag, listDataVendorCode=listDataVendorCode)
                # modelWithAddin.colorList = listdir(joinPath(pathToMaskFolderSilicon, curModel.replace(caseType,'').strip()))
                self.listModelForExcel.append(modelWithAddin)
                self.ui.textSiliconMask.setText(curModel+' записан\n')
                return None
        


    def btnCreateExcelForSilicon(self):
        addImage = self.ui.AddPhotoSelector.currentText()
        if self.listModelForExcel == []:
            self.btnApplyAddin(True)
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
        modelBrand = self.ui.textEditBrand.toPlainText()
        if modelBrand == '':
            self.createMSGError('Поле бренд не заполенно!')
            return 0
        modelModel = self.ui.textEditModel.toPlainText()
        if modelModel == '':
            self.createMSGError('Поле модель не заполенно!')
            return 0
        colorList = self.checkColorBox()
        if colorList == 0:
            return 0
        p = multiprocessing.Process(target=makeImageBookWithNameModel, args=(colorList, modelBrand, modelModel,), name=modelBrand + ' ' + modelModel)
        self.ui.textLog.setText(self.ui.textLog.toPlainText() + modelBrand +' ' + modelModel + ' добавлен в очередь\n')
        p.start()



if __name__ =='__main__':
    app = QtWidgets.QApplication([])
    application = mameBookPrint()
    application.show()

    sys.exit(app.exec())


