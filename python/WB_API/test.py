from barcode.writer import ImageWriter
import barcode
from fpdf import FPDF


def create_1C_barcod(case_name, case_art, bar):
    options = dict(module_height=5.0, text_distance=1.0, format='PNG')

    barcode.get('ean13', bar,
                ImageWriter()).save('D:\ean13', options)
    image_path = 'D:\ean13.png'
    size = (370, 280)
    pdf = FPDF(format=size)
    pdf.add_page()
    pdf.image(image_path, x=-45, y=180, w=450)
    pdf.add_font(
        'DejaVu', '', r'C:\Users\user\Downloads\font\DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 55)
    pdf.multi_cell(350, 25, txt="{}".format(
        case_name))
    pdf.add_font(
        'DejaVu', '', r'C:\Users\user\Downloads\font\DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 40)
    pdf.multi_cell(350, 20, txt="{}".format(
        case_art))
    pdf.multi_cell(350, 20, txt="{}".format(
        'Продавец: ИП Караханян Э.С'))
    pdf.output(r'D:\1C_barcod.pdf')
    return r'D:\1C_barcod.pdf'


case_name = r'WB Чехол для Samsung Galaxy A3 (2017) (SM-A320) Soft-touch черный'
case_art = r'WB Чехол для Samsung Galaxyчерный'
bar = r'2001256753069'
create_1C_barcod(case_name, case_art, bar)
