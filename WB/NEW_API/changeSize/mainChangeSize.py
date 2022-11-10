import multiprocessing
import requests
from classChangeSize import filterNomenclatures1CForChange, getNomenclaturesFromWB, changeSize


class changerSize():
    def __init__(self) -> None:
        self.listNomenclatures = []
        self.tokenList = ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w',
                    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM',
                    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y']

    def main(self):
        filterNom = filterNomenclatures1CForChange()
        filterNom.getListNomenclatures()
        # filterNom.filterNomenclatures('Чехол;силикон','книга')
        filterNom.filterNomenclatures('Чехол;силикон')
        self.listNomenclatures = filterNom.getNom()
        for token in self.tokenList:
            pool = multiprocessing.Pool()
            for nomenclature in  self.listNomenclatures:
                pool.apply_async(self.changeSize, args=(nomenclature['Штрихкод'], token,))
            pool.close()
            pool.join()
        

    def changeSize(self, barcod, token):
        getNom = getNomenclaturesFromWB(barcod, token)
        getNom.getCard()
        if getNom.cardVendorCode != '':
            nomenclature = getNom.getNomenclature()
            if type(nomenclature) != None:
                change = changeSize(nomenclature, token, (18.5,12,1.4),False)
                change.changeSize()






if __name__ =='__main__':
    a = changerSize()
    a.main()
