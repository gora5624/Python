import sys
from os.path import abspath, join as joinPath
sys.path.append(abspath(joinPath(__file__,('../../../..'))))
from my_mod.my_lib import read_xlsx
from pandas import read_excel

class SplitStocks:
    def __init__(self, dataQuatity) -> None:
        self.Quatity = dataQuatity
    

    def getTypeCase():
        dataFromXLSX = read_excel(joinPath(__file__,'../..', 'Moduls', 'Справочник по типу.xlsx'))
        # caseBarcods = dataFromXLSX[dataFromXLSX.Тип == u'Без принта']['Штрихкод'].values.tolist()
        # printsBarcods = dataFromXLSX[dataFromXLSX.Тип == u'Принт']['Штрихкод'].values.tolist()
        # glass3DBarcods = dataFromXLSX[dataFromXLSX.Тип == u'3D']['Штрихкод'].values.tolist()
        # nanoBarcods = dataFromXLSX[dataFromXLSX.Тип == u'Нано']['Штрихкод'].values.tolist()
        return dataFromXLSX
        # return (caseBarcods, printsBarcods, glass3DBarcods, nanoBarcods)

if __name__ == '__main__':
    a = SplitStocks.getTypeCase()
    a