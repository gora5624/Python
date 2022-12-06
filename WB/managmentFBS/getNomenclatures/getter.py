from Class import nomenclaturesGetter
import multiprocessing
import time


class Getter():
    def __init__(self) -> None:
        self.periodGetNomenclatures = 1 # Часы
        self.tokens = [
                    {
                        'IPName': 'Самвел',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
                    },
                    {
                        'IPName': 'Караханян',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
                    },
                    {
                        'IPName': 'Манвел',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
                    }             
                ]

    def getNom(self):
        while True:
            listProc = []
            for token in self.tokens:
                p = multiprocessing.Process(target=self.getNomProcess, args=(token,))
                p.start()
            for p in listProc:
                p.join()
            time.sleep(self.periodGetNomenclatures*60*60)



    def getNomProcess(self,token):
        getter = nomenclaturesGetter(token)
        getter.getPiaceOfNom()
            # time.sleep(self.periodGetNomenclatures*60*60)
            # p = multiprocessing.Process(target=getter.getPiaceOfNom)
            # p.start()


if __name__ == '__main__':
    getter = Getter()
    getter.getNom()