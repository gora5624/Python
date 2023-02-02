import base64
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import PyPDF2
from my_lib import read_xlsx
from fpdf import FPDF
import barcode
from barcode.writer import ImageWriter


Orders = read_xlsx(
    r'C:\Users\Public\Documents\WBHelpTools\MakeWBStikersWithName\Orders\ФБС стекла 09.08.21.xlsx')

out_file = r'D:\temp.PDF'


def All_to_one_PDF(PDF_path):
    pdf_writer = PyPDF2.PdfFileWriter()
    pdf_file = PyPDF2.PdfFileReader(
        open(PDF_path, 'rb'))
    page = pdf_file.getPage(0)
    pdf_writer.addPage(page)
    return pdf_writer


def create_data():
    data_tmp = read_xlsx('D:\Список номенклатуры.XLSX')
    data_new = {}
    for line in data_tmp:
        tmp = {line['Баркод']: {
            'Название': line['Название'], 'Артикул поставщика': line['Артикул поставщика']}}
        data_new.update(tmp)
    return data_new


def generate_pic_with_barcod(barcod_case):
    options = dict(module_height=5.0, text_distance=1.0, format='PNG')
    ean = barcode.get('ean13', barcod_case,
                      ImageWriter())
    ean.save('D:\ean13', options)
    return 'D:\ean13.png'


def create_pdf_with_case_name(Case_name, Art, barcod_case):
    size = (400, 300)
    pdf = FPDF(format=size)
    pdf.add_page()
    pdf.image(generate_pic_with_barcod(barcod_case), x=-50, y=190, w=500)
    pdf.add_font(
        'DejaVu', '', r'C:\Users\user\Downloads\font\DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 60)
    pdf.multi_cell(380, 25, txt="{}".format(Case_name))
    pdf.set_font('DejaVu', '', 50)
    pdf.multi_cell(380, 25, txt="{}".format(
        'Продавец: ИП Караханян Э.С'))
    pdf.multi_cell(380, 25, txt="{}".format(Art))
    pdf_out_path = r"D:\PDF_with_case_name.pdf"
    pdf.output(pdf_out_path)
    return pdf_out_path


data = create_data()
for order in Orders:
    Case_name = data[order['ШК']]['Название'].replace(r'\xa0', '')
    Art = data[order['ШК']]['Артикул поставщика']
    barcod_case = order['ШК']
    page = All_to_one_PDF(create_pdf_with_case_name(
        Case_name, Art, barcod_case))

page.write(out_file)
