from ClassGetNomenclatures import nomenclaturesGetter, cardGetter
import multiprocessing
import time


class Getter():
    def __init__(self) -> None:
        self.periodGetNomenclatures = 1 # Часы
        self.tokens = [
                    {
                        'IPName': 'Караханян',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w',
                        'pathToDB': r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_nom Караханян.txt'
                    },
                    {
                        'IPName': 'Самвел',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y',
                        'pathToDB': r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_nom Самвел.txt'
                    },
                    
                    {
                        'IPName': 'Манвел',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM',
                        'pathToDB': r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_nom Манвел.txt'
                    } ,
                    
                    {
                        'IPName': 'Федоров',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImIxYjQ3YjQzLTFhMTYtNGQ0Ni1iZTA1LWRlY2ExZTcxMTU0MSJ9.qTIJF6fEgbRux3Ps30ciMQ802UWqtAER-y94ALvE3PI',
                        'pathToDB': r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_nom Федоров.txt'
                    }             
                ]

    def getNom(self):
        while True:
            listProc = []
            self.start_time = time.time()
            for token in self.tokens:
                p1 = multiprocessing.Process(target=self.getNomProcess, args=(token,))
                p2 = multiprocessing.Process(target=self.getCardProcess, args=(token,))
                p1.start()
                p2.start()
                listProc.append(p1)
                listProc.append(p2)
            for p in listProc:
                p.join()
        
            #time.sleep(self.periodGetNomenclatures*60*60)



    def getNomProcess(self,token):
        # while True:
        #     try:
            self.start_timeGetNomProcess = time.time()
            getter = nomenclaturesGetter(token)
            getter.getPiaceOfNom()
            time.sleep(self.periodGetNomenclatures*60*60)
            print("--- %s getNomProcess seconds ---" % (time.time() - self.start_timeGetNomProcess))
            # except:
            #     continue
            # time.sleep(self.periodGetNomenclatures*60*60)
            # p = multiprocessing.Process(target=getter.getPiaceOfNom)
            # p.start()


    def getCardProcess(self, token):
        # while True:
        #     try:
            self.start_timeGetCardProcess = time.time()
            getterCard = cardGetter(token)
            getterCard.getNom()
            print("--- %s getCardProcess seconds ---" % (time.time() - self.start_timeGetCardProcess))
            # except:
            #     continue



if __name__ == '__main__':
    getter = Getter()
    getter.getNom()