from PyQt5 import QtWidgets
from ui.FBOSeller import Ui_Form
import sys
from Class.GetStocksClass import GetStocks
from Class.ChangeAvailabilityClass import ChangeAvailability
from os.path import exists, abspath, join as joinPath
import pandas


# pyuic5 E:\MyProduct\Python\WB\FBOSeller\ui\FBOSeller.ui -o E:\MyProduct\Python\WB\FBOSeller\ui\FBOSeller.py

class FBOSellerStart(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(FBOSellerStart, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.Updatebtn.clicked.connect(self.getStocks)
        self.ui.Startbtn.clicked.connect(self.mainAction)
        self.dataQuatity = pandas.DataFrame
        self.quatityFull = ''
        self.quatityPrint = ''
        self.quatityNoPrint = ''
        self.quatity3D = ''
        self.quatityNano = ''
        self.pathToPriceFile = joinPath(abspath(__file__), '..','startPrice.xlsx')
        self.firstChek()
        


    def getStocks(self):
        self.seller = self.ui.comboBox.currentText()
        self.dataQuatity = GetStocks(self.seller).getStocksMain()
        price = self.dataQuatity['price'] * (100 - self.dataQuatity['discount'])/100
        self.dataQuatity.insert(0, 'priceReal', price)
        #self.dataQuatity.to_excel(r'E:\priceReal.xlsx', index=False)
        self.fillFields()


    def firstChek(self):
        if not exists(self.pathToPriceFile):
            self.getStocks()
            priceDF = self.dataQuatity.filter(items=['barcode','priceReal'])
            priceDF.to_excel(self.pathToPriceFile, index=False)



    def fillFields(self):
        dataQuatity = self.dataQuatity
        self.quatityFull = dataQuatity['quantity'].sum()
        self.ui.StocksQuatityAllText.setText(str(self.quatityFull))
        self.quatityPrint = dataQuatity[dataQuatity.Тип == u'Принт']['quantity'].sum()
        self.ui.StocksQuatityPrintText.setText(str(self.quatityPrint))
        self.ui.MinPricePrint.setText(str(dataQuatity[dataQuatity.Тип == u'Принт']['priceReal'].min()))
        self.ui.AveragePricePrint.setText(str(dataQuatity[dataQuatity.Тип == u'Принт']['priceReal'].mean()))
        self.ui.MaxPricePrint.setText(str(dataQuatity[dataQuatity.Тип == u'Принт']['priceReal'].max()))
        self.quatityNoPrint = dataQuatity[dataQuatity.Тип == u'Без принта']['quantity'].sum()
        self.ui.MinPriceNoPrint.setText(str(dataQuatity[dataQuatity.Тип == u'Без принта']['priceReal'].min()))
        self.ui.AveragePriceNoPrint.setText(str(dataQuatity[dataQuatity.Тип == u'Без принта']['priceReal'].mean()))
        self.ui.MaxPriceNoPrint.setText(str(dataQuatity[dataQuatity.Тип == u'Без принта']['priceReal'].max()))
        self.ui.StocksQuatityNoPrintText.setText(str(self.quatityNoPrint))
        self.quatity3D = dataQuatity[dataQuatity.Тип == u'3D']['quantity'].sum()
        self.ui.MinPrice3DGlass.setText(str(dataQuatity[dataQuatity.Тип == u'3D']['priceReal'].min()))
        self.ui.AveragePrice3DGlass.setText(str(dataQuatity[dataQuatity.Тип == u'3D']['priceReal'].mean()))
        self.ui.MaxPrice3DGlass.setText(str(dataQuatity[dataQuatity.Тип == u'3D']['priceReal'].max()))
        self.ui.StocksQuatity3DGlassText.setText(str(self.quatity3D))  
        self.quatityNano = dataQuatity[dataQuatity.Тип == u'Нано']['quantity'].sum()
        self.ui.MinPriceNano.setText(str(dataQuatity[dataQuatity.Тип == u'Нано']['priceReal'].min()))
        self.ui.AveragePriceNano.setText(str(dataQuatity[dataQuatity.Тип == u'Нано']['priceReal'].mean()))
        self.ui.MaxPriceNano.setText(str(dataQuatity[dataQuatity.Тип == u'Нано']['priceReal'].max()))
        self.ui.StocksQuatityNanoGlassText.setText(str(self.quatityNano))


    def mainAction(self):

        pass



    def changeAvailability(self):
        tmp = ChangeAvailability(self.seller, listBarcodes)
        tmp.takeOff()


if __name__ =='__main__':
    app = QtWidgets.QApplication([])
    application = FBOSellerStart()
    application.show()

    sys.exit(app.exec())
