import barcode
from barcode.writer import ImageWriter
import fpdf
from fpdf import FPDF
from my_lib import file_exists, read_xlsx
from os.path import join as joinpath
from pdfrw import PdfReader, PdfWriter
import os

WBOrdersDataFileName = r'Data_orders.xlsx'
WBOrdersJsonDataFileName = r'Order.json'
main_path = r'C:\Users\Public\Documents\WBHelpTools\MakeWBStikersWithName'
WBOrdersData = joinpath(
    main_path, r'WBOrdersData')
OrdersDir = joinpath(
    main_path, r'Orders')
TMPDir = joinpath(
    main_path, r'TMPDir')
Token_path = joinpath(
    main_path, r'Token.txt')
FontPath = r'C:\Users\Public\Documents\WBHelpTools\MakeWBStikersWithName\font\ArialSans.ttf'
orders = ''
caseFilePath = r'\\192.168.0.33\shared\Отдел производство\Wildberries\Список номенклатуры — копия.XLSX'
fpdf.set_global("SYSTEM_TTFONTS", os.path.join(
    os.path.dirname(__file__), r'C:\Windows\Fonts'))


def create_1C_barcod(count, art='', case_name='', case_art='', bar=''):
    if case_name == '':
        for line in read_xlsx(caseFilePath):
            if art == str(line['Артикул WB'])[0:-2] if type(line['Артикул WB']) == float else line['Артикул WB']:
                case_name = line['Название 1С']
                case_art = line['Артикул поставщика']
                bar = str(line['Баркод'])[0:-2] if type(
                    line['Баркод']) == float else line['Баркод']
                break

    options = dict(module_height=5.0, text_distance=1.0, format='PNG')

    barcode.get('ean13', bar,
                ImageWriter()).save(joinpath(TMPDir, 'ean13'), options)
    image_path = joinpath(TMPDir, 'ean13.png')
    size = (370, 280)
    pdf = FPDF(format=size)
    pdf.add_page()
    pdf.image(image_path, x=-45, y=180, w=450)
    pdf.add_font(
        'Arial', '', fname="Arial.ttf", uni=True)
    pdf.set_font('Arial', '', 60)
    pdf.multi_cell(350, 25, txt="{}".format(
        case_name))
    pdf.set_font('Arial', '', 40)
    pdf.multi_cell(350, 24, txt="{}".format(
        case_art))
    pdf.multi_cell(350, 24, txt="{}".format(
        'Продавец: ИП Караханян Э.С'))
    pdf.output(joinpath(TMPDir, r'testBarcod.pdf'))
    writer = PdfWriter()
    path2 = PdfReader(joinpath(TMPDir, r'testBarcod.pdf'),
                      decompress=False).getPage(0)
    for i in range(count):
        writer.addpage(path2)
    fileName = joinpath(r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\ценники',
                        os.path.basename(case_name.replace(":", " ") + '.pdf'))
    cnt = 1
    while file_exists(fileName):
        cnt += 1
        fileName = joinpath(r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\ценники',
                            os.path.basename(case_name.replace(":", " ") + '_{}.pdf'.format(str(cnt))))

    writer.write(fileName)


case_name = ''
case_art = ''
bar = ''
count = 300
art = ''

# while True:
#     if case_name == '':
#         try:
#             art = str(input('Введите артикул: '))
#             count = int(input('Введите количество: '))
#         except:
#             continue
#     create_1C_barcod(count, art, case_name, case_art, bar)
#     if case_name != '':
#         break

for line in read_xlsx(r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\ФБО без принтов 07.02.2022 ч1 KZN.xlsx'):
    if case_name == '':
        try:
            art = str(line['Артикул']) if type(
                line['Артикул']) == str else str(line['Артикул'])[0:-2]
            count = int(line['Количество'])
        except:
            continue
    create_1C_barcod(count, art, case_name, case_art, bar)
    print(art)
    if case_name != '':
        break
