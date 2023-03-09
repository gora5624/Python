import fpdf
import requests
from fpdf import FPDF
from datetime import datetime
import os


class Supplies():
    def __init__(self):
        self.tokens = [
                    {
                        'IPName': 'Караханян',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
                    },
                    {
                        'IPName': 'Самвел',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y'
                    },
                    
                    {
                        'IPName': 'Манвел',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
                    } ,
                    
                    {
                        'IPName': 'Федоров',
                        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImIxYjQ3YjQzLTFhMTYtNGQ0Ni1iZTA1LWRlY2ExZTcxMTU0MSJ9.qTIJF6fEgbRux3Ps30ciMQ802UWqtAER-y94ALvE3PI'
                    }             
                ]

    def isExistsSupp(self, supp):
        url = f'https://suppliers-api.wildberries.ru/api/v3/supplies/{supp}'
        for token in self.tokens:
            headers = {
                    'Authorization': token['token']
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                #data = response.json()
                return token['IPName']
            else:
                continue
        return False



class Acts():
    def __init__(self, seller, nambersBox):
        self.sellerToname = seller
        self.pathToStandartFonts = os.path.join(os.environ['WINDIR'],'fonts')
        self.seller = self.setSeller(seller)
        self.strNamberBox = ', '.join(nambersBox)
        self.numBox = len(nambersBox)


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