import multiprocessing
from classChangeSize import filterNomenclatures1CForChange, getNomenclaturesFromWB, changeSize
import os


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
        filterNom.filterNomenclatures('Чехол')
        # self.listNomenclatures = filterNom.getNom()
        listNomenclatures= filterNom.getNom()
        for token in self.tokenList:
            pool = multiprocessing.Pool()
            # self.listNomenclatures = listNomenclatures
            listProcess = []
            for i in  listNomenclatures:  # range(0,len(listNomenclatures),25):
                # for j in listNomenclatures[i:i+25]:
                #     p = multiprocessing.Process(target=self.changeSize, args=(j['Штрихкод'], token,))
                #     p.start()
                #     listProcess.append(p)
                # for p in listProcess:
                #     p.join()
                pool.apply_async(self.changeSize, args=(i['Штрихкод'], token,))
            pool.close()
            pool.join()
        

    def changeSize(self, barcod, token):
        getNom = getNomenclaturesFromWB(barcod, token)
        getNom.getCard()
        if getNom.cardVendorCode != '':
            nomenclature = getNom.getNomenclature()
            if type(nomenclature) != None:
                change = changeSize(nomenclature, token, (20,15,2),True)
                change.changeSize()
            else:
                print('1')
        else:
            print('1')
        # obj = [change, nomenclature, getNom]
        # return 0






if __name__ =='__main__':
    a = changerSize()
    a.main()
