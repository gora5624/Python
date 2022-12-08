from Class import nomenclaturesGetter, cardGetter
import multiprocessing
import time


class Getter():
    def __init__(self) -> None:
        self.periodGetNomenclatures = 6 # Часы
        self.tokens = [
                    {
                        'IPName': 'Караханян',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w',
                        'pathToDB': r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\db_nom Караханян.txt'
                    },
                    {
                        'IPName': 'Самвел',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y',
                        'pathToDB': r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\db_nom Самвел.txt'
                    },
                    
                    {
                        'IPName': 'Манвел',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM',
                        'pathToDB': r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\db_nom Манвел.txt'
                    }             
                ]

    def getNom(self):
        while True:
            listProc = []
            start_time = time.time()
            for token in self.tokens:
                p1 = multiprocessing.Process(target=self.getNomProcess, args=(token,))
                p2 = multiprocessing.Process(target=self.getCardProcess, args=(token,))
                p1.start()
                p2.start()
                listProc.append(p1)
                listProc.append(p2)
            for p in listProc:
                p.join()
            print("--- %s seconds ---" % (time.time() - start_time))
            time.sleep(self.periodGetNomenclatures*60*60)



    def getNomProcess(self,token):
        getter = nomenclaturesGetter(token)
        getter.getPiaceOfNom()
            # time.sleep(self.periodGetNomenclatures*60*60)
            # p = multiprocessing.Process(target=getter.getPiaceOfNom)
            # p.start()


    def getCardProcess(self, token):
        getterCard = cardGetter(token)
        getterCard.getNom()


if __name__ == '__main__':
    getter = Getter()
    getter.getNom()