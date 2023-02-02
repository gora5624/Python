import barcode
from barcode.writer import ImageWriter
from fpdf import FPDF


def create_barcod(case_name, case_art, bar):
    options = dict(module_height=5.0, text_distance=1.0, format='PNG')

    barcode.get('ean13', bar,
                ImageWriter()).save('D:\ean13', options)
    image_path = 'D:\ean13.png'
    size = (400, 300)
    pdf = FPDF(format=size)
    pdf.add_page()
    pdf.image(image_path, x=-50, y=190, w=500)
    pdf.add_font(
        'DejaVu', '', r'C:\Users\user\Downloads\font\DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 55)
    pdf.multi_cell(380, 25, txt="{}".format(
        case_name))
    pdf.add_font(
        'DejaVu', '', r'C:\Users\user\Downloads\font\DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 40)
    pdf.multi_cell(380, 23, txt="{}".format(
        case_art))
    pdf.multi_cell(380, 23, txt="{}".format(
        'Продавец: ИП Караханян Э.С'))

    pdf.output(r'D:\add_image.pdf')


case_name = 'WB Чехол для Huawei P Smart 2021 силикон прозрачный'
case_art = '00-00096545Прозрачный'
bar = '2001201758187'
create_barcod(case_name, case_art, bar)
