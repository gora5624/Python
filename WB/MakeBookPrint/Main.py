from audioop import mul
from os.path import join as joinPath, abspath
from os import listdir
import multiprocessing
from PyQt5 import QtWidgets
from MakeBookPrintUi import Ui_Form
import sys
from makeImageWithNameModel import makeImageWithNameModel
from AddSkriptForMakeImage import RenameImage, genArtColor, generate_bar_WB, multiReplace, reductionDict, reductionDict2
# from makeImageWithNameModel import makeImageColor
# pyuic5 E:\MyProduct\Python\python\MakeBookPrint\MakeBookPrintUi.ui -o E:\MyProduct\Python\python\MakeBookPrint\MakeBookPrintUi.py


diskWithPrint = 'F'
pathToBookPrint = r'{}:\Готовые картинки Fashion по моделям'.format(diskWithPrint)


class mameBookPrint(QtWidgets.QMainWindow):
    def __init__(self):
        super(mameBookPrint, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.CreatePrint.clicked.connect(self.btnMakePrintClicked)
        self.ui.CreateExcel.clicked.connect(self.btnMakeExcelClicked)


    def createMSG(self,text):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setText(text)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.exec_()


    def checkColorBox(self):
        listColor = []
        for i in range(self.ui.splitterColor.count()):
            statusCheckBox = self.ui.splitterColor.widget(i).checkState()
            if statusCheckBox:
                listColor.append(self.ui.splitterColor.widget(i).text())
        return listColor


    def btnMakeExcelClicked(self):
        listImageAll = []
        for model in listdir(pathToBookPrint):
            listModel = []
            for color in listdir(joinPath(pathToBookPrint, model)):
                listColor = []
                RenameImage(joinPath(pathToBookPrint, model,color))
                listArt = genArtColor(color, listdir(joinPath(pathToBookPrint, model,color)))
                listBarcodes = generate_bar_WB(len(listArt))
                for i, art in enumerate(listArt):
                    name = 'Чехол книга {} {} с силиконовый вставкой Fashion'.format(model, color.lower())
                    data = {'Баркод': listBarcodes[i],
                            'Группа': 'Чехол производство (принт)',
                            'Основная характеристика': art['Принт'],
                            'Название 1С': multiReplace(name, reductionDict),
                            'Название полное': name,
                            'Название полное с принтом': name + ' ' + art['Принт'],
                            'Размер печать': '',
                            'Категория': art['Категория'],
                            'Код категории': art['Код категории'],
                            'Код цвета': art['Код цвета'],
                            'Артикул цвета': art['Артикул цвета']}
                    listColor.append(data)
                listModel.extend(listColor)
            listImageAll.extend(listModel)
        pass


    def btnMakePrintClicked(self):
        modelBrand = self.ui.textEditBrand.toPlainText()
        if modelBrand == '':
            self.createMSG('Поле бренд не заполенно!')
        modelModel = self.ui.textEditModel.toPlainText()
        if modelModel == '':
            self.createMSG('Поле модель не заполенно!')
        colorList = self.checkColorBox()
        p = multiprocessing.Process(target=makeImageWithNameModel, args=(colorList, modelBrand, modelModel,), name=modelBrand + ' ' + modelModel)
        self.ui.textLog.setText(self.ui.textLog.toPlainText() + modelBrand +' ' + modelModel + ' добавлен в очередь\n')
        p.start()



if __name__ =='__main__':
    app = QtWidgets.QApplication([])
    application = mameBookPrint()
    application.show()

    sys.exit(app.exec())


