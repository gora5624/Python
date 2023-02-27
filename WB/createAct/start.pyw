from PyQt6 import QtWidgets
from createAct import createAct
import pickle
import os
from datetime import datetime, timedelta


class managerSupp():
    def __init__(self) -> None:
        self.dateNow = datetime.now().date()
        self.fileSuppsName = f'{self.dateNow}_supp.pkl'
        self.pathTofileSupps = os.path.join(os.environ['LOCALAPPDATA'],self.fileSuppsName)
        self.existsFlag = os.path.exists(self.pathTofileSupps)
        self.deleteOld()
        

    def deleteOld(self):
        dateOld = (datetime.now() - timedelta(1)).date()
        if os.path.exists(os.path.join(os.environ['LOCALAPPDATA'], f'{dateOld}_supp.pkl')):
            os.remove(os.path.join(os.environ['LOCALAPPDATA'], f'{dateOld}_supp.pkl'))

    def createDB(self, myapp):
        with open(self.pathTofileSupps, 'wb') as file:
            pickle.dump(myapp.data, file)
            file.close()
        

    def readDB(self, myapp):
        if self.existsFlag:
            with open(self.pathTofileSupps, 'rb') as file:
                myapp.data = pickle.load(file)
                myapp.startInitial()
                file.close()


if __name__ == '__main__':
    try:
        date = datetime.now().date()
        app = QtWidgets.QApplication([])
        myapp = createAct()
        managerSupp().readDB(myapp)
        myapp.show()
        app.exec()
    finally:
        managerSupp().createDB(myapp)

        
