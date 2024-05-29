from itertools import count
import fpdf
import requests
from fpdf import FPDF
from datetime import datetime
import os
import pickle
from PyQt6.QtCore import QRunnable, pyqtSlot as Slot, pyqtSignal as Signal, QObject


class Signals(QObject):
    complete = Signal(bool, str)


class SuppliesWorker(QRunnable):
    tokens = [
            {
                'IPName': 'Караханян',
                'token': 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwNTA2djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTczMjEyNTY5NSwiaWQiOiI4OWY4NWM1ZC1iOTlmLTQ5MTMtODY2My1iNzEwNTQ0MDk1NjciLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjEwMTA2MiwicyI6MTYsInNpZCI6IjNhOTNkZGMxLWFhNTctNWMyYi05YzVjLWRkZDIyMTg4OTQ0MCIsInQiOmZhbHNlLCJ1aWQiOjQ1MzIyOTIwfQ.e_S9SBIzEkN3EiAXhfnk31m4ugAly-88k7HqetaMWfIqq74bVPCPHScQQA_T4CSLfguOMvQoz1qwzNjje36CMg'
            },
            {
                'IPName': 'Самвел',
                'token': 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwNTA2djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTczMjEyNTg2NywiaWQiOiIwMzc0MDYzNi02MjIzLTQzN2ItOThjMi03YTk1MjQ0OWJkZWQiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjgxOTI0NiwicyI6MTYsInNpZCI6IjBhYjhiMTA1LTA1MWYtNGVkNi04NzBiLTM5OWU3NWUxMDI4NiIsInQiOmZhbHNlLCJ1aWQiOjQ1MzIyOTIwfQ.8_kZlEQ2seAe2AHDHtnAIrwCOLzyX0xmnTEQFLUboiBQAsCZSFUyY0B5xDSikVUARU4i2SC6a8W22vfpojOIcA'
            },
            
            {
                'IPName': 'Манвел',
                'token': 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwNTA2djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTczMjEyNTgxNiwiaWQiOiJkMDZjNWFmZi1jZjgxLTQ5ZDgtYWRlNi02MDE0NTkyNmQxNjMiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjUyNzczNiwicyI6MTYsInNpZCI6ImFhNDdlNDg5LTU5ZTAtNDIzMi1hMWJmLTBlMTIzOWYwNDJmMSIsInQiOmZhbHNlLCJ1aWQiOjQ1MzIyOTIwfQ.ANBlYtkVAaKHCkNXXRj8_NVFeVwv_gh2VvL7TSsXntXvE6EYYUFKGoeVdEyMhwmCdC-KdrJTWVLUWpto8KIfCg'
            } ,
            
            {
                'IPName': 'Федоров',
                'token': 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwNTA2djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTczMjEyNTkwMywiaWQiOiJjMWRmOWVmMS1jYmY5LTQ5ODMtYjA3NS1kODVkOGNkZGU0M2QiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjExNzEwNDQsInMiOjE2LCJzaWQiOiJkOWU0OGUxZi05ZjgxLTQ1MmMtODRiYy05ZGYxZWRiMzNmNDkiLCJ0IjpmYWxzZSwidWlkIjo0NTMyMjkyMH0.q5S2OSWOO8lgRuDGZbZ2_wZ24_kbimrK6iVFpIFnEVPlcnIn69x97JbQu-3GE8OZTQ6TVJe5eCoIQDemTc_a_Q'
            }             
        ]
    
    

    def __init__(self, IPName, supp):
        super().__init__()
        self.IPName = IPName
        # self.saveToken()
        self.token = self.getToken()
        self.url = f'https://suppliers-api.wildberries.ru/api/v3/supplies/{supp}'
        self.signal = Signals()

    def loadToken(self):
        return pickle.load(open(os.path.join(r'C:\Users\Public\Documents', r'token.pkl'), 'rb'))

    def saveToken(self):
        pickle.dump(self.tokens, open(os.path.join(r'C:\Users\Public\Documents', r'token.pkl'), 'wb'))

    def getToken(self):
        self.tokens = self.loadToken()
        for token in self.tokens:
            if token['IPName'] == self.IPName:
                return token['token']


    def isExistsSupp(self, supp):
        countTry = 0
        while countTry <5:
            for token in self.tokens:
                headers = {
                        'Authorization': token['token']
                }
                try:
                    response = requests.get(self.url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        #data = response.json()
                        return token['IPName']
                    else:
                        continue
                except:
                    countTry += 1
                    continue
        return False
    
    @Slot()
    def run(self):
        countTry = 0
        while countTry <5:
            headers = {
                    'Authorization': self.token
            }
            try:
                response = requests.get(self.url, headers=headers, timeout=10)
                if 'Не найдено' in response.text:
                    break
                if response.status_code == 200:
                    #data = response.json()
                    self.signal.complete.emit(True, self.IPName)
                    break
                    # 
                    # return self.IPName
                else:
                    countTry += 1
                    continue
            except:
                countTry += 1
                continue
        # self.signal.complete.emit(False, self.IPName)
        # return False




class Acts():
    def __init__(self, seller, nambersBox):
        self.sellerToname = seller
        self.pathToStandartFonts = os.path.join(os.environ['WINDIR'],'fonts')
        self.seller = self.setSeller(seller)
        # проверить есть ли в nambersBox повторяющиеся значения
        self.nambersBox = self.checkNambersBox(nambersBox)
        self.strNamberBox = ', '.join(self.nambersBox)
        self.numBox = len(self.nambersBox)


    def checkNambersBox(self, nambersBox):
        for box in nambersBox:
            if box in nambersBox:
                # посчитать количество box в nambersBox
                count = nambersBox.count(box)
                if count > 1:
                    nambersBox.remove(box)
                    # повторить проверку для оставшихся box в nambersBox
                    self.checkNambersBox(nambersBox)
                    break
                else:
                    continue
            else:
                continue
        return nambersBox




    def setSeller(self, seller):
        if seller == 'Караханян':
            return 'ИП Караханян Эдуард Сергеевич, ИНН: 561000521896'
        elif seller == 'Самвел':
            return 'ИП Абраамян Самвел Манвелович, ИНН: 563808760345'
        elif seller == 'Манвел':
            return 'ИП Абраамян Манвел Сойрабович, ИНН: 561208348680'        
        elif seller == 'Федоров':
            return 'ИП Федоров Иван Иванович, ИНН: 561703121059'
        else:
            return 'НЕИЗВЕСТНОЕ ИП'


    def createActs(self, ordersFilePath):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("Arial",'', os.path.join(self.pathToStandartFonts, 'Arial.ttf'))
        pdf.set_font("Arial", size=12)
        widthCell = 190
        heightCell =8
        date = datetime.date(datetime.now())
        pdf.cell(widthCell, heightCell*2, txt=f"Акт приёма-передачи груза от {str(date.strftime('%d.%m.%Y'))}",new_y=fpdf.YPos.NEXT,new_x=fpdf.XPos.LMARGIN, align="C")
        pdf.cell(widthCell, heightCell, txt=f"Отправитель: {self.seller}",new_y=fpdf.YPos.NEXT,new_x=fpdf.XPos.LMARGIN, align="L")
        pdf.cell(widthCell, heightCell, txt=f"Получатель: ООО Вайлдберриз, ИНН: 7721546864",new_y=fpdf.YPos.NEXT,new_x=fpdf.XPos.LMARGIN, align="L")
        pdf.cell(widthCell, heightCell, txt="Республика Татарстан, Зеленодольск, промышленный парк Зеленодольск, 20",new_y=fpdf.YPos.NEXT,new_x=fpdf.XPos.LMARGIN, align="L")
        pdf.cell(widthCell, heightCell, txt=f"Перевозчик: ИП Гайнанов Артур Римович, ИНН: 561017881199",new_y=fpdf.YPos.NEXT,new_x=fpdf.XPos.LMARGIN, align="L")
        pdf.cell(widthCell, heightCell, new_y=fpdf.YPos.NEXT,new_x=fpdf.XPos.LMARGIN, align="L")
        pdf.multi_cell(widthCell, heightCell, txt=f'       Настоящий документ подтверждает, что "Отправитель" передал, а "Перевозчик" принял коробы со следующими номерами: {self.strNamberBox}.',new_y=fpdf.YPos.NEXT,new_x=fpdf.XPos.LMARGIN, align="L")
        pdf.cell(widthCell, heightCell,txt=f'Общее количество: {self.numBox}', new_y=fpdf.YPos.NEXT,new_x=fpdf.XPos.LMARGIN, align="L")
        pdf.cell(widthCell, heightCell, new_y=fpdf.YPos.NEXT,new_x=fpdf.XPos.LMARGIN, align="L")
        pdf.multi_cell(widthCell, heightCell,txt='       Представитель перевозчика обязуется осуществить контроль факта приёмки товара на складе "Получателя" и убедиться, что каждая коробка была отсканирована надлежащим образом.', new_y=fpdf.YPos.NEXT,new_x=fpdf.XPos.LMARGIN, align="L")
        pdf.cell(widthCell, heightCell, new_y=fpdf.YPos.NEXT,new_x=fpdf.XPos.LMARGIN, align="L")
        pdf.cell(widthCell,heightCell,txt='Предствитель отправителя: __________________________', align="L" , new_y=fpdf.YPos.NEXT,new_x=fpdf.XPos.LMARGIN)
        pdf.cell(widthCell,heightCell,txt=f"Дата: {str(date.strftime('%d.%m.%Y'))}", align="L" , new_y=fpdf.YPos.NEXT,new_x=fpdf.XPos.LMARGIN)
        pdf.cell(widthCell,heightCell,txt='Предствитель перевозчика: __________________________', align="L" , new_y=fpdf.YPos.NEXT,new_x=fpdf.XPos.LMARGIN)
        pdf.cell(widthCell,heightCell,txt=f"Дата: {str(date.strftime('%d.%m.%Y'))}", align="L" , new_y=fpdf.YPos.NEXT,new_x=fpdf.XPos.LMARGIN)
        pdf.output(os.path.join(ordersFilePath, f"Акт приёма передачи от {str(date.strftime('%d.%m.%Y'))} {self.sellerToname}.pdf"))

# SuppliesWorker('','')
# if __name__ == '__main__':
#     a = Acts('Федоров', ['WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622'])
#     a.createActs()