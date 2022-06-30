from ui.managerFBSMain import managerUI
from PyQt5 import QtWidgets
import sys


if __name__ =='__main__':
    app = QtWidgets.QApplication([])
    application = managerUI()
    application.show()
    sys.exit(app.exec())