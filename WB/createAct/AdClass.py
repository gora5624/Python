from itertools import count
import fpdf
import requests
from fpdf import FPDF
from datetime import datetime
import os
from PyQt6.QtCore import QRunnable, pyqtSlot as Slot, pyqtSignal as Signal, QObject


class Signals(QObject):
    complete = Signal(bool, str)


class SuppliesWorker(QRunnable):
    tokens = [
            {
                'IPName': 'Караханян',
                'token': 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNjM0NzA2MSwiaWQiOiIwMmE5ODU1ZS1mMjU3LTQ0NWItYjhkZC0zYTM3ODAwZGM0NGQiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjEwMTA2MiwicyI6MTYsInNpZCI6IjNhOTNkZGMxLWFhNTctNWMyYi05YzVjLWRkZDIyMTg4OTQ0MCIsInVpZCI6NDUzMjI5MjB9.QjUqQn7fEgOb4RKBIrYaXRB89mVnauWAK1H8xPOxbLZfSv2MEnhPETAYYZuM47cgYxEBp9-z8XqnuxMUV16Gzg'
            },
            {
                'IPName': 'Самвел',
                'token': 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxODY1MDUzOCwiaWQiOiJmNWNjODRhOC01Mjk1LTRjZTAtOTUwOC1mYjQ1OTdmNTY3OGEiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjgxOTI0NiwicyI6MTYsInNhbmRib3giOmZhbHNlLCJzaWQiOiIwYWI4YjEwNS0wNTFmLTRlZDYtODcwYi0zOTllNzVlMTAyODYiLCJ1aWQiOjQ1MzIyOTIwfQ.M-0NluWSI0bXaLVEGivROAG4D9h64GIi-JTRTE4JEtgDyfGOBRk4CfDHJz75ydaTntvmgZAoVXC1wswH5xBmiw'
            },
            
            {
                'IPName': 'Манвел',
                'token': 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNjM0NzExNywiaWQiOiJjZjc1MDAxMS1jZDhkLTRmMjAtYmE3Ny0yNjMwZmEwMjBkMGYiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjUyNzczNiwicyI6MTYsInNpZCI6ImFhNDdlNDg5LTU5ZTAtNDIzMi1hMWJmLTBlMTIzOWYwNDJmMSIsInVpZCI6NDUzMjI5MjB9.__KBNiAn545q-hdg1veDPaHSL0bX4G93ZqS4z2xVGT0SZageOCbEbPesn1ePoUQ0pQcCay46xcD-J1_zUpepDQ'
            } ,
            
            {
                'IPName': 'Федоров',
                'token': 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNjM0NzE3NSwiaWQiOiIwZWFjMmU0Ni1lZmMwLTQxZmEtOGNhMy1kODllZjhlMzNhYTAiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjExNzEwNDQsInMiOjE2LCJzaWQiOiJkOWU0OGUxZi05ZjgxLTQ1MmMtODRiYy05ZGYxZWRiMzNmNDkiLCJ1aWQiOjQ1MzIyOTIwfQ.AWhYAeVcj2dNdY_qTY2gfFbB7x3SdxPRKLdE2ycSs9PSxF7XoCLwJEtt10eBymRMuD2bmpGpVoA2R0FKn-aTgA'
            }             
        ]
    
    def __init__(self, IPName, supp):
        super().__init__()
        self.IPName = IPName
        self.token = self.getToken()
        self.url = f'https://suppliers-api.wildberries.ru/api/v3/supplies/{supp}'
        self.signal = Signals()

    def getToken(self):
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


# if __name__ == '__main__':
#     a = Acts('Федоров', ['WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622','WB-GI-38073622'])
#     a.createActs()