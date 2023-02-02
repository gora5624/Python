from my_lib import file_exists
import pandas
from datetime import datetime
from fpdf import FPDF
import fpdf
import os


fpdf.set_global("SYSTEM_TTFONTS", os.path.join(
    os.path.dirname(__file__), r'C:\Windows\Fonts'))

countBox = 0
nameBox = r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\Реестры ФБО\ФБО коробка от {} № {}.xlsx'
namePDFBox = r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\ШК поставки\ФБО коробка от {} № {}.pdf'

while True:
    day = format(
        datetime.today().date().strftime(r"%d.%m.%Y"))
    countBox += 1
    while file_exists(nameBox.format(day, str(countBox))) and file_exists(namePDFBox.format(day, str(countBox))):
        countBox += 1
    listBarcode = []
    barcode = str(input('Введите штрихкод товара, 0 чтобы закрыть коробку: '))
    while barcode != '0':
        if barcode != '':
            listBarcode.append({'Баркод': barcode})
        barcode = str(
            input('Введите штрихкод товара, 0 чтобы закрыть коробку: '))

    if listBarcode != []:
        count = len(listBarcode)
        listBarcodepd = pandas.DataFrame(listBarcode)
        listBarcodepd.groupby(['Баркод']).size().reset_index(name='Количество').to_excel(
            nameBox.format(day, str(countBox)), index=False)
        size = (200, 300)
        pdf = FPDF(format=size)
        pdf.add_page()
        pdf.add_font(
            'Arial', '', fname="Arial.ttf", uni=True)
        pdf.set_font('Arial', '', 45)
        pdf.multi_cell(180, 25, txt="{}".format(
            'Коробка №{}'.format(str(countBox))), align='C')
        pdf.multi_cell(180, 25, txt="{}".format(
            'ИП Караханян Э.С.'), align='C')
        pdf.multi_cell(180, 25, txt="{}".format(
            'Поставка Казань ФБО'), align='C')
        if count != 0:
            pdf.multi_cell(180, 25, txt="{}".format(
                'Количество {} шт.').format(str(count)), align='C')
        pdf.output(namePDFBox.format(day, str(countBox)))
    print('Коробка {} сформирована.'.format(str(countBox)))
