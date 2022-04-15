import multiprocessing
from os import listdir
from os.path import join as joinPath, isdir
from PyQt5 import QtWidgets
from MakeBookPrintUi import Ui_Form
import sys
from makeImageBookWithNameModel import makeImageBookWithNameModel
from AddSkriptForMakeBookImage import createExcel, deleteImage, CreateImageFolderForWBMain, pathToBookPrint
from makeImageSilicon import createAllSiliconImage, pathToSiliconMaskFolder, pathToDoneSiliconImage
from AddSkriptForMakeSiliconImage import createExcelSilicon
import time
start_time = time.time()
# pyuic5 E:\MyProduct\Python\WB\MakeBookPrint\MakeBookPrintUi.ui -o E:\MyProduct\Python\WB\MakeBookPrint\MakeBookPrintUi.py


class mameBookPrint(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(mameBookPrint, self).__init__(parent)
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


    def fillSiliconMaskList(self, tabIndex):
        if tabIndex  == 1 or tabIndex  == False:
            negFlag = False
            for mask in listdir(pathToSiliconMaskFolder):
                if isdir(joinPath(pathToSiliconMaskFolder, mask)):
                    fileList = listdir(joinPath(pathToSiliconMaskFolder, mask))
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


    def btnCreateSiliconImage(self):
        createAllSiliconImage(pathToSiliconMaskFolder,6)
        
        

    def btnCreateExcelForSilicon(self):
        {
            'Бренд': self.ui.textSiliconBrand.toPlainText(),
            'Совместимость': self.ui.textSiliconCompability.toPlainText(),
            'Наименование': self.ui.textSiliconName.toPlainText(),
            'Модель': self.ui.textSiliconModel.toPlainText(),
        }

        p = multiprocessing.Process(target=createExcelSilicon)
        p.start()
        p.join()


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


