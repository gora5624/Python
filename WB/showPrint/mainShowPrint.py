import os
import re
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import QThreadPool
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt
from ui_showStuff import Ui_MainWindowShowStuff
from os.path import exists, join as joinPath, dirname
import pickle
from WorkersClass import WorkerCheckDBImage, WorkerGetDataFrom1c, WorkerRequestImageAPI


# pyuic6 D:\Python\WB\showPrint\showStuff.ui -o D:\Python\WB\showPrint\ui_showStuff.py

class ShowPrint(QtWidgets.QMainWindow):
    # статические поля класса
    # сингал на изменения размера окна
    resized = QtCore.pyqtSignal()
    # токены API
    tokens = [
                    {
                        'IPName': 'Караханян',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
                    },
                    {
                        'IPName': 'Самвел',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
                    },
                    
                    {
                        'IPName': 'Манвел',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
                    } ,
                    
                    {
                        'IPName': 'Федоров',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImIxYjQ3YjQzLTFhMTYtNGQ0Ni1iZTA1LWRlY2ExZTcxMTU0MSJ9.qTIJF6fEgbRux3Ps30ciMQ802UWqtAER-y94ALvE3PI'
                    }             
                ]
    # остальное, пути ссылки и тп
    urlGetImage = 'https://suppliers-api.wildberries.ru/content/v1/cards/cursor/list'
    pathToBarcodeList1c = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\ШК.txt'
    pathToCatalogPrints = r'\\192.168.0.111\shared\_Общие документы_\Каталог принтов'
    pathToCaseImage = r'\\192.168.0.33\shared\_Общие документы_\Егор\Архив масок ВБ\Маски новые'
    pathToNoImege =r'C:\Users\Георгий\Desktop\flat,1000x1000,075,f.jpg'
    pathToPickleDBImages = joinPath(dirname(__file__),'printPicle.pkl')
    pool = QThreadPool().globalInstance()
    


    def __init__(self,parent=None):

        # инициализация интерфейса
        super(ShowPrint, self).__init__(parent)
        self.ui = Ui_MainWindowShowStuff()
        self.ui.setupUi(self)

        # подключение сигналов к методам класса и слотов
        self.ui.lineEditScan.returnPressed.connect(self.scanStuff)
        self.ui.actionUpdatePrintPkl.triggered.connect(self.forcedupdatePrintPkl)

        
        self.resized.connect(self.updatePixmap)

        # настроки фокусировки
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ui.lineEditScan.setFocus()
        # self.ui.lineEditScan.setVisible(False)

        # маска для ввода штрихкода
        self.ui.lineEditScan.setInputMask('9999999999999')

        # видимость элементов и изменение надписей и стилей
        a = self.ui.labelImagePrint.setStyleSheet('background-color: rgb(230,230,230)')
        a
        self.ui.labelStuffName.setText('')
        self.ui.labelChooseStuff.hide()
        self.ui.comboBoxChooseStuff.hide()
        self.ui.labelChoosePrint.hide()
        self.ui.comboBoxShoosePrint.hide()

        # объявление динамических полей класса
        self.pixmapWB = QtGui.QPixmap()
        self.pixmapPrint = QtGui.QPixmap()
        self.pixmapStuff = QtGui.QPixmap()
        self.barcode = ''
        self.listBarcodesFrom1C = ''
        self.name = ''
        self.dataDF = ''
        self.char = ''
        self.fullName = ''
        self.printFileName = ''
        self.pickleDBImages = []

        # выполнение при запуске
        # self.start()
        # self.getDataFrom1c()
        # checkDBImage().chekImageList()
        # self.loadsImagePrints()
        self.startSetups()
        

    def loadsImagePrints(self):
        with open(self.pathToPickleDBImages, 'rb') as f:
            self.pickleDBImages = pickle.load(f)
            f.close()


    def resizeEvent(self, event):
        # сигнал для перерисовки изображения при изменении размеров окна
        self.resized.emit()
        return super(ShowPrint, self).resizeEvent(event)
    

    def updatePixmap(self):
        # обновление размеров изображения при изменении размеров окна
        if not self.pixmapWB.isNull():
            size = self.ui.labelImageFromWB.size()
            # self.pixmapWB.scaled()
            self.ui.labelImageFromWB.setPixmap(self.pixmapWB.scaled(size, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        if not self.pixmapStuff.isNull():
            size = self.ui.labelImageStuff.size()
            self.ui.labelImageStuff.setPixmap(self.pixmapStuff.scaled(size, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        if not self.pixmapPrint.isNull():
            size = self.ui.labelImagePrint.size()
            self.ui.labelImagePrint.setPixmap(self.pixmapPrint.scaled(size, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        QtWidgets.QApplication.processEvents()


    def setNameStuff(self):
        # получение имени предмета
        if self.barcode in self.listBarcodesFrom1C:
            self.name = self.dataDF[self.dataDF.Штрихкод == self.barcode]['Номенклатура'].values.tolist()[0]
            self.char = self.dataDF[self.dataDF.Штрихкод == self.barcode]['Характеристика'].values.tolist()[0]
            self.fullName = self.name + ' ' + self.char
            if (self.char == '(Принт 0)') or ('Принт' not in self.char):
                self.printFileName = 'print 0.png'
            else:
                self.printFileName = self.char.lower().replace('принт','print').replace(')','').replace('(','') +'.png'
            self.ui.labelStuffName.setText(self.fullName)
            fontSize = 15
            self.ui.labelStuffName.setStyleSheet(f"font-size:{fontSize}px")
            
            while self.ui.labelStuffName.sizeHint().width() > self.ui.centralwidget.width():
                fontSize-=1
                self.ui.labelStuffName.setStyleSheet(f"font-size:{fontSize}px")
            return True
        else:
            self.setPixmapImageFromWB()
            self.setPixmapPrint()
            self.swMess('Нет такого товара в базе', 'red')
            return False

       
    def swMess(self, mess = '', color='black', size='14' ):
        self.ui.statusbar.showMessage(mess)
        self.ui.statusbar.setStyleSheet(f"font-size: {size}px; color: {color}")


    def setPixmapImageFromWB(self, content=''):
        # отрисовка картинки с WB в интерфейс
        if content != '' and type(content) == bytes:
            self.pixmapWB.loadFromData(content)
            self.updatePixmap()
            content = ''
            self.swMess(f'Картинка {self.fullName} загружена', 'green')
        else:
            self.pixmapWB = QtGui.QPixmap()
            self.ui.labelImageFromWB.clear()
            self.swMess(f'Картинка {self.fullName} не загружена, либо товар отсуствует на сайте', 'red')

    def chekUpdate(self):
        pass


    def setPixmapPrint(self):
        # отрисовка картинки принта в интерфейс
        if self.printFileName in self.pickleDBImages:
            if (self.char == '(Принт 0)') or ('Принт' not in self.char):
                self.pixmapPrint.loadFromData(self.pickleDBImages[self.printFileName])
            else:
                self.pixmapPrint.loadFromData(self.pickleDBImages[self.printFileName])
            self.updatePixmap()
        else:
            self.ui.labelImagePrint.clear()
            return False
        

    def setPixmapStuff(self):
        # отрисовка картинки принта в интерфейс
        if 'Пластина' in self.name:
            path = os.path.normpath(joinPath(self.pathToCaseImage, 'Пластины', 'fon.jpg'))
        elif 'Картхолдер белый под печать с лентой' in self.name:
            path = os.path.normpath(joinPath(self.pathToCaseImage, 'Картхолдер', 'tape.jpg'))
        elif 'Картхолдер белый под печать с кожаной петлей' in self.name:
            path = os.path.normpath(joinPath(self.pathToCaseImage, 'Картхолдер', 'loop.jpg'))
        elif 'Картхолдер белый под печать с металлическим кольцом' in self.name:
            path = os.path.normpath(joinPath(self.pathToCaseImage, 'Картхолдер', 'ring.jpg'))
        elif 'Картхолдер белый под печать' in self.name:
            path = os.path.normpath(joinPath(self.pathToCaseImage, 'Картхолдер', 'fon.png'))
        elif re.fullmatch(r'Комплект.+:.+матовая', self.name):
            path = os.path.normpath(joinPath(self.pathToCaseImage, 'Бронепленки', 'filmMate.jpg'))
        elif  re.fullmatch(r'Комплект.+:.+глянцевая', self.name):
            path = os.path.normpath(joinPath(self.pathToCaseImage, 'Бронепленки', 'filmClear.jpg'))
        else:
            path = os.path.normpath(joinPath(self.pathToCaseImage, self.name, 'fon.png'))
        if not exists(path):
            path = os.path.normpath(joinPath(self.pathToCaseImage, self.name, 'fon.png'))
        if exists(path):
            f = open(path, 'rb').read()
            self.pixmapStuff.loadFromData(f)
            self.updatePixmap()
        else:
            self.ui.labelImageStuff.clear()
            return False


    def startSetups(self):
        mess = QMessageBox(self)
        # mess.setTextFormat(Qt.TextFormat.RichText)
        # mess.setText('Ожидайте запуска программы')
        mess.setWindowTitle('Запуск')
        mess.setWindowModality(Qt.WindowModality.NonModal)
        mess.setText('Запуск программы, ожидате')
        mess.open()
        QtWidgets.QApplication.processEvents()
        # self.ui.statusbar.showMessage('Идёт получение данных. ждите...')
        worker_1 = WorkerGetDataFrom1c()
        worker_1.signal.complete.connect(self.updateUiGetData)
        worker_2 = WorkerCheckDBImage()
        worker_2.signal.complete.connect(self.loadsImagePrints)
        listWorkers = [worker_1, worker_2]
        for workers in listWorkers:
            self.pool.start(workers)
        self.pool.waitForDone()
        mess.close()
        self.pool.clear()

    def forcedupdatePrintPkl(self):
        worker_2 = WorkerCheckDBImage(True)
        worker_2.signal.complete.connect(self.loadsImagePrints)
        self.pool.start(worker_2)
        self.swMess('Идет обновление базы принтов ждтие', 'blue')
        QtWidgets.QApplication.processEvents()
        self.pool.waitForDone()
        self.swMess('Обновление завершено, можно работать', 'green')


        

    def updateUiGetData(self, listBarcodesFrom1C, dataDF):
        self.listBarcodesFrom1C, self.dataDF = listBarcodesFrom1C, dataDF
        self.ui.statusbar.showMessage('Программа готова к работе')

    def scanStuff(self):
        # функция последовательных вызовов доп. функиций для получания и вывода изображений
        self.barcode = self.ui.lineEditScan.text()
        self.ui.lineEditScan.clear()
        if self.setNameStuff():
            worker_1 = WorkerRequestImageAPI(self.barcode)
            worker_1.signal.complete.connect(self.setPixmapImageFromWB)
            worker_1.signal.fail.connect(self.setPixmapImageFromWB)
            self.pool.start(worker_1)
            self.setPixmapPrint()
            self.setPixmapStuff()
            # self.pool.waitForDone()        
        self.pool.clear()
        self.clearAtr()
    
    def clearAtr(self):
        self.name = ''
        self.char = ''
        self.fullName = ''
        self.printFileName = ''


if __name__ =='__main__':
    app = QtWidgets.QApplication([])
    application = ShowPrint()
    # application.startSetups()
    application.show()
    app.exec()