import multiprocessing
import sys
from os import listdir
from os.path import join as joinPath, isdir, isfile, abspath, exists
sys.path.append(abspath(joinPath(__file__,'../../..')))
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from ui.parsing import Ui_Parser
from Class.taskManagerClass import TaskManager

class ParsingUI(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(ParsingUI, self).__init__(parent)
        self.ui = Ui_Parser()
        self.ui.setupUi(self)
        self.searchRequests = []
        self.countPage = int
        self.allPageCheck = bool
        self.sorting = str
        self.saveTime = int
        self.ui.startButton.clicked.connect(self.main)


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

    
    def check(self):
        # Получаем все свойства из юи
        self.searchRequests = []
        tmpList = self.ui.searchRequestsList.toPlainText().split(';')
        self.searchRequests = [i for i in range(len(tmpList)) if tmpList[i] != '']
        if not self.ui.allPageCheckBox.isChecked():
            try:
                self.countPage = int(self.ui.countPage.toPlainText())
            except:
                self.countPage = 0
            self.allPageCheck = False
        else:
            self.allPageCheck = True
        self.sorting = self.ui.sorting.currentText()
        try:
            self.saveTime = int(self.ui.timerSave.text())
        except:
            self.saveTime = 0
        # Проверяем свойства на правильность заполнения, если есть критичные ошибки, возвращаем False
        if self.searchRequests == []:
            self.createMSGError('Строка поисковых запросов пустая, запуск невозможен.')
            return False
        if not self.allPageCheck:
            if self.countPage <= 0:
                self.countPage = 5
                self.createMSGError('Количество дней заполненно некорректно, количество по умолчинию 5 дней.')
        if self.saveTime <=0:
            self.saveTime =5
            self.createMSGError('Период автосохранения промежуточных результатов заполнен некорректно, по умолчанию 5 минут.')
        return True
            


    def main(self):
        if self.check():
            pages = self.allPageCheck if self.allPageCheck else self.countPage
            taskManager = TaskManager(self.searchRequests, pages, self.sorting, self.saveTime)
            taskManager.start()
         






if __name__ =='__main__':
    app = QtWidgets.QApplication([])
    application = ParsingUI()
    application.show()

    sys.exit(app.exec())