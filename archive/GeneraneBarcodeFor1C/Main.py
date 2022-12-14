from barcode.writer import ImageWriter
import barcode
from fpdf import FPDF
import fpdf
import os
from os.path import join    as joinpath
import sys
sys.path.insert(1, joinpath(__file__, '../../..'))
from my_mod.my_lib import read_xlsx
import requests
import time
import pandas

fpdf.set_global("SYSTEM_TTFONTS", os.path.join(
    os.path.dirname(__file__), r'C:\Windows\Fonts'))

dirForPicWithBarcode = r'E:\\'
dirForPicWithBarcodePNG = r'E:\\'
listStuff = r'E:\GeneraneBarcodeFor1C\Список сотрудников новая 1С.xlsx'

def create_1C_barcod(bc, name):
    options = dict(module_height=5.0, text_distance=1.0, format='PNG')

    barcode.get('ean13', bc,
                ImageWriter()).save(joinpath(dirForPicWithBarcodePNG, name), options)
    image_path = joinpath(dirForPicWithBarcodePNG, name+'.png')
    size = (370, 280)
    pdf = FPDF(format=size)
    pdf.add_page()
    pdf.image(image_path, x=-45, y=180, w=450)
    pdf.add_font(
        'Arial', '', fname="Arial.ttf", uni=True)
    pdf.set_font('Arial', '', 100)
    pdf.multi_cell(350, 50, txt="{}".format(    
        name), align='C')
    pdf.output(joinpath(dirForPicWithBarcode, name + '.pdf'))


# for line in read_xlsx(listStuff):
#     name = 'Макаров Алексей'#line['Пользователь']
#     bc = '2029943477623'# str(line['Штрихкод'] )[0:-2]
#     create_1C_barcod(bc, name)


def generate_bar_WB(count):
        listBarcode = []
        countTry = 0
        url = "https://suppliers-api.wildberries.ru/content/v1/barcodes"
        headers = {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'}

        while count > 5000:
            
            while True and countTry < 10:
                json = {
                        "count": 5000
                        }
                try:
                    r = requests.post(url, json=json, headers=headers)
                    listBarcode.extend(r.json()['data'])
                    if not r.json()['error']:
                        count -= 5000
                        break
                except:
                    print(
                        'Ошибка получения ШК. count = {}, пытаюсь повторно получить.'.format(count))
                    print(r.rext)
                    countTry += 1
                    time.sleep(10)
                    continue
        while True and countTry < 10:
            json = {
                        "count": count
                        }
            try:
                r = requests.post(url, json=json, headers=headers)
                listBarcode.extend(r.json()['data'])
                if not r.json()['error']:
                    break
            except:
                print(
                    'Ошибка получения ШК. count = {}, пытаюсь повторно получить.'.format(count))
                countTry += 1
                time.sleep(10)
                continue
        print(listBarcode[0])
        return str(listBarcode[0])


name = 'Гежа Матвей'#line['Пользователь']
bc = generate_bar_WB(1)# str(line['Штрихкод'] )[0:-2]
create_1C_barcod(bc, name)