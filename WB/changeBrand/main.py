from PyQt5 import QtWidgets
import sys
from ui.changeBrand import Ui_Form

# pyuic5 E:\MyProduct\Python\WB\changeBrand\ui\changeBrand.ui -o E:\MyProduct\Python\WB\changeBrand\ui\changeBrand.py



class cahngeBrand(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(cahngeBrand, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)


    def closeEvent(self, event):
            close = QtWidgets.QMessageBox.question(self,
                                                "Выход",
                                                "Вы уверенны что хотите закрыть программу?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if close == QtWidgets.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

if __name__ =='__main__':
    app = QtWidgets.QApplication([])
    application = cahngeBrand()
    application.show()

    sys.exit(app.exec())