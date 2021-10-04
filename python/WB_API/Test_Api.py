
from fpdf import FPDF
from os.path import join as joinpath
import fpdf
import os


pathToOrders = r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\Новые'
WBOrdersDataFileName = r'Data_orders.xlsx'
WBOrdersJsonDataFileName = r'Order.json'
main_path = r'C:\Users\Public\Documents\WBHelpTools\MakeWBStikersWithName'
WBOrdersData = joinpath(
    main_path, r'WBOrdersData')
TMPDir = joinpath(
    main_path, r'TMPDir')
Token_path = joinpath(
    main_path, r'Token.txt')
fpdf.set_global("SYSTEM_TTFONTS", os.path.join(
    os.path.dirname(__file__), r'C:\Windows\Fonts'))
Name1CStiker = '1c_{}.pdf'
NameWBStikerTMP = 'WBTMP_{}.pdf'
NameWBStiker = 'WB_{}.pdf'
NameSVG = 'WB_{}.svg'
NameTitle1CStiker = 'Name1.pdf'
NameEAN13PNG = 'ean13_{}.png'
NameTable = 'TBL_{}.pdf'


def create_CallBackStiker():
    size = (370, 280)
    pdf = FPDF(format=size)
    pdf.add_page()
    pdf.add_font(
        'Arial', '', fname="Arial.ttf", uni=True)
    pdf.set_font('Arial', '', 85)
    pdf.multi_cell(360, 40, txt="{}".format(
        'Уважаемый клиент, если у Вас возникли проблемы или вопросы с нашим товаром, свяжитесь с нами по WhatsApp +79096036674.'), align="C")
    pdf.output(joinpath(TMPDir, NameTitle1CStiker))
    return joinpath(TMPDir, NameTitle1CStiker)


create_CallBackStiker()
