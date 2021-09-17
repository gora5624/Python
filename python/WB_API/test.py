import sys
import os
from mydesign import Ui_MainWindow  # импорт нашего сгенерированного файла
from PyQt5 import QtCore, QtGui, QtWidgets

text = '123'


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.label.setFont(QtGui.QFont('Arial', 30))
        self.ui.label.setGeometry(QtCore.QRect(10, 10, 200, 200))
        self.ui.label.setText('Тест')
        for excel in os.listdir(r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\Новые'):
            self.ui.comboBox.addItem(excel)


app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())
