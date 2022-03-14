import multiprocessing
from PyQt5 import QtWidgets
from MakeBookPrintUi import Ui_Form
import sys
from makeImageWithNameModel import makeImageWithNameModel
from AddSkriptForMakeImage import createExcel, deleteImage, CreateImageFolderForWBMain
# pyuic5 E:\MyProduct\Python\WB\MakeBookPrint\MakeBookPrintUi.ui -o E:\MyProduct\Python\WB\MakeBookPrint\MakeBookPrintUi.py


diskWithPrint = 'F'
pathToBookPrint = r'{}:\Готовые картинки Fashion по моделям'.format(diskWithPrint)


class mameBookPrint(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(mameBookPrint, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.CreatePrint.clicked.connect(self.btnMakePrintClicked)
        self.ui.CreateExcel.clicked.connect(self.btnMakeExcelClicked)
        self.ui.DeleteImage.clicked.connect(self.btnMakeDeleteIamge)
        self.ui.CreateImageFolderForWB.clicked.connect(self.btnCreateImageFolderForWB)


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
        p = multiprocessing.Process(target=makeImageWithNameModel, args=(colorList, modelBrand, modelModel,), name=modelBrand + ' ' + modelModel)
        self.ui.textLog.setText(self.ui.textLog.toPlainText() + modelBrand +' ' + modelModel + ' добавлен в очередь\n')
        p.start()



if __name__ =='__main__':
    app = QtWidgets.QApplication([])
    application = mameBookPrint()
    application.show()

    sys.exit(app.exec())


