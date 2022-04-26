from genericpath import isfile
import multiprocessing
from os import listdir
from os.path import join as joinPath, isdir
from PyQt5 import QtWidgets
from MakeBookPrintUi import Ui_Form
import sys
from makeImageBookWithNameModel import makeImageBookWithNameModel
from AddSkriptForMakeBookImage import createExcel, deleteImage, CreateImageFolderForWBMain, pathToBookPrint
from makeImageSilicon import createAllSiliconImage, pathToSiliconMaskFolder, pathToDoneSiliconImage
from AddSkriptForMakeSiliconImage import createExcelSilicon, markerForAllModel, copyImage, chekImage
from MyClassForMakeImage import ModelWithAddin
import time
from GetCardAsincio import getListCard
from Create import WBnomenclaturesCreater
start_time = time.time()
# pyuic5 E:\MyProduct\Python\WB\MakeBookPrint\MakeBookPrintUi.ui -o E:\MyProduct\Python\WB\MakeBookPrint\MakeBookPrintUi.py


class mameBookPrint(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(mameBookPrint, self).__init__(parent)
        self.listModelForExcel = []
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.CreatePrint.clicked.connect(self.btnMakePrintClicked)
        self.ui.CreateExcel.clicked.connect(self.btnMakeExcelClicked)
        self.ui.DeleteImage.clicked.connect(self.btnMakeDeleteIamge)
        self.ui.CreateImageFolderForWB.clicked.connect(self.btnCreateImageFolderForWB)
        self.ui.tabWidget.tabBarClicked.connect(self.fillSiliconMaskList)
        self.ui.ChekMask.clicked.connect(self.fillSiliconMaskList)
        self.ui.CreateSiliconImage.clicked.connect(self.btnCreateSiliconImage)
        self.ui.CreateExcelForSilicon.clicked.connect(self.btnCreateExcelForSilicon)
        self.ui.ChekImage.clicked.connect(self.btnChekImage)
        self.ui.ApplyAddin.clicked.connect(self.btnApplyAddin)
        self.ui.CreateCase.clicked.connect(self.btnCreateCase)
        self.updeteListFile()
        self.updateModelList()


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


    def btnChekImage(self):
        fileName = self.ui.FileSelector.currentText()
        mode = self.ui.IPSelector.currentText()
        status = chekImage(fileName, mode)
        self.ui.textSiliconMask.setText('{} готов.\nСтатус: {}'.format(fileName, status))
        if status == 'Во всех карточках присутствуют фото.':
            self.ui.textSiliconMask.setStyleSheet("background-color: green;")
        else:
            self.ui.textSiliconMask.setStyleSheet("background-color: red;")


    def updeteListFile(self):
        self.ui.FileSelector.clear()
        for item in listdir(pathToDoneSiliconImage):
            if isfile(joinPath(pathToDoneSiliconImage,item)):
                self.ui.FileSelector.addItem(item)


    def btnCreateCase(self):
        fileName = self.ui.FileSelector.currentText()
        pathToFileForUpload = joinPath(pathToDoneSiliconImage, fileName)
        create = WBnomenclaturesCreater()
        create.pathToFileForUpload = pathToFileForUpload
        mode = self.ui.IPSelector.currentText()
        barcodeList = getListCard(mode)
        create.createNomenclatures(mode, barcodeList)
        self.ui.textSiliconMask.setText('{} готов.'.format(fileName))
        getListCard(mode)



    def fillSiliconMaskList(self, tabIndex):
        self.ui.textSiliconMask.setText('')
        if tabIndex  == 1 or tabIndex  == False:
            negFlag = False
            for mask in listdir(pathToSiliconMaskFolder):
                if isdir(joinPath(pathToSiliconMaskFolder, mask)):
                    for color in listdir(joinPath(pathToSiliconMaskFolder, mask)):
                        fileList = listdir(joinPath(pathToSiliconMaskFolder, mask, color))
                        if 'mask.png' in fileList and 'fon.png' in fileList:
                            continue
                        elif 'mask.png' not in fileList and 'fon.png' not in fileList:
                            self.ui.textSiliconMask.setText(self.ui.textSiliconMask.toPlainText() + mask + ' ' + color + ' НЕТ МАКСИ И ФОНА\n')
                            negFlag = True
                            continue
                        elif 'mask.png' not in fileList and 'fon.png' in fileList:
                            self.ui.textSiliconMask.setText(self.ui.textSiliconMask.toPlainText() + mask + ' ' + color + ' НЕТ МАКСИ\n')
                            negFlag = True
                            continue
                        elif 'mask.png' in fileList and 'fon.png' not in fileList:
                            self.ui.textSiliconMask.setText(self.ui.textSiliconMask.toPlainText() + mask + ' ' + color +' НЕТ ФОНА\n')
                            negFlag = True
                            continue
            if not negFlag:
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
        listModel = listdir(pathToSiliconMaskFolder)
        for model in listModel:
            if isdir(joinPath(pathToSiliconMaskFolder,model)):
                self.ui.ModelSelector.addItem(model)


    def btnCreateSiliconImage(self):
        createAllSiliconImage(pathToSiliconMaskFolder,6)
        self.updateModelList()
        copyImage()
      

    def btnApplyAddin(self, curModel = False):
        if curModel == False:
            curModel = self.ui.ModelSelector.currentText()
        else:
            curModel = markerForAllModel
        listModel = []
        for i in range(1,self.ui.ModelSelector.count()):
            listModel.append(self.ui.ModelSelector.itemText(i))
        if curModel == markerForAllModel:
            self.listModelForExcel = []
            brand = self.ui.textSiliconBrand.toPlainText()
            compability = self.ui.textSiliconCompability.toPlainText()
            name = self.ui.textSiliconName.toPlainText()
            modelAddin = self.ui.textSiliconModel.toPlainText()
            cameraType = self.ui.CameraType.currentText()
            price = self.ui.textPrice.toPlainText()
            for model in listModel:
                modelWithAddin = ModelWithAddin(model, brand, compability, name, modelAddin, cameraType, price)
                modelWithAddin.colorList = listdir(joinPath(pathToSiliconMaskFolder, model))
                self.listModelForExcel.append(modelWithAddin)
                self.ui.textSiliconMask.setText('Все модели из списка записаны\n')
        else:
            if self.listModelForExcel != []:
                for i, item in enumerate(self.listModelForExcel):
                    if item.model == curModel:
                        if self.acceptEvent("Свойства для {} уже записаны, перезаписать?".format(item.model)):
                            brand = self.ui.textSiliconBrand.toPlainText()
                            compability = self.ui.textSiliconCompability.toPlainText()
                            name = self.ui.textSiliconName.toPlainText()
                            modelAddin = self.ui.textSiliconModel.toPlainText()
                            cameraType = self.ui.CameraType.currentText()
                            price = self.ui.textPrice.toPlainText()
                            self.listModelForExcel[i] = ModelWithAddin(curModel, brand, compability, name, modelAddin, cameraType, price)
                            self.listModelForExcel[i].colorList = listdir(joinPath(pathToSiliconMaskFolder, curModel))
                            self.ui.textSiliconMask.setText(curModel+' перезаписана\n')
                            break
                        else:
                            return None
                brand = self.ui.textSiliconBrand.toPlainText()
                compability = self.ui.textSiliconCompability.toPlainText()
                name = self.ui.textSiliconName.toPlainText()
                modelAddin = self.ui.textSiliconModel.toPlainText()
                cameraType = self.ui.CameraType.currentText()
                price = self.ui.textPrice.toPlainText()
                modelWithAddin = ModelWithAddin(curModel, brand, compability, name, modelAddin, cameraType, price)
                modelWithAddin.colorList = listdir(joinPath(pathToSiliconMaskFolder, curModel))
                self.listModelForExcel.append(modelWithAddin)
                self.ui.textSiliconMask.setText(curModel+' записан\n')
                return None
            else:
                brand = self.ui.textSiliconBrand.toPlainText()
                compability = self.ui.textSiliconCompability.toPlainText()
                name = self.ui.textSiliconName.toPlainText()
                modelAddin = self.ui.textSiliconModel.toPlainText()
                cameraType = self.ui.CameraType.currentText()
                price = self.ui.textPrice.toPlainText()
                modelWithAddin = ModelWithAddin(curModel, brand, compability, name, modelAddin, cameraType, price)
                modelWithAddin.colorList = listdir(joinPath(pathToSiliconMaskFolder, curModel))
                self.listModelForExcel.append(modelWithAddin)
                self.ui.textSiliconMask.setText(curModel+' записан\n')
                return None
        pass
        


    def btnCreateExcelForSilicon(self):
        if self.listModelForExcel == []:
            self.btnApplyAddin(True)
        p = multiprocessing.Process(target=createExcelSilicon, args=(self.listModelForExcel, ))
        p.start()
        p.join()
        self.updeteListFile()


    def btnCreateImageFolderForWB(sefl):
        fileName = QtWidgets.QFileDialog.getOpenFileName(None,'Выберете файл связи',r'C:\Users\Public\Documents\WBChangeStuff','*.xlsx')
        filePathCumm = fileName[0]
        CreateImageFolderForWBMain(filePathCumm, pathToBookPrint)




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
        deleteImage()


    def btnMakePrintClicked(self):
        modelBrand = self.ui.textEditBrand.toPlainText()
        if modelBrand == '':
            self.createMSGError('Поле бренд не заполенно!')
        modelModel = self.ui.textEditModel.toPlainText()
        if modelModel == '':
            self.createMSGError('Поле модель не заполенно!')
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


