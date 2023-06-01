from mainShowPrint import ShowPrint
from PyQt6 import QtWidgets
import pickle
import multiprocessing
import time


class Updater():
    pathToChangelog = r"\\192.168.0.111\shared\_Общие документы_\Заказы вайлд\mainShowPrint\changelog"
    pathToVersion = r"C:\Users\Public\Documents\mainShowPrint\version"
    pathToApp = r'C:\Users\Public\Documents\mainShowPrint'
    app = QtWidgets.QApplication([])
    def __init__(self):
        self.showPrint = ''
        self.stop = False
        self.thread_1 = multiprocessing.Process(target=self.thread_worker)
        
        
    
    def doChengelog(self, version, whatNew=''):
        with open(self.pathToChangelog, "wb") as f:
            data = {'version': version, 'whatNew': whatNew}
            pickle.dump(data, f)
            f.close()

    def chekUpdate(self):
        try:
            with open(self.pathToVersion, 'rb') as f:
                version = pickle.load(f)
        except:
            version = '0'
        try:
            with open(self.pathToChangelog, 'rb') as f:
                lastVersion = pickle.load(f)['version']
        except:
            lastVersion = '0'
        if version != lastVersion:
            return True
        else:
            return False
    
    def update(self):
        pass
        
    
    def thread_worker(self):
        while not self.stop:
            app = QtWidgets.QApplication([])
            # updater().doChengelog('0.1.0', 'Новая версия')
            self.application = ShowPrint()
            self.application.startSetups()
            self.application.show()
            app.exec()
    

if __name__ == '__main__':

    a = Updater()
    a.thread_1.start()
    time.sleep(15)
    a.thread_1.terminate()
    a = Updater()
    a.thread_1.start()
    a.thread_1.join()