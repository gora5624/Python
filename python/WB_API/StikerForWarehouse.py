import base64
import barcode
from barcode.writer import ImageWriter
import fpdf
from fpdf import FPDF
import requests
import json
import pandas
from datetime import datetime, timedelta
from my_lib import file_exists
from os.path import join as joinpath
from os import makedirs
from os.path import isfile
import PyPDF2
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from pdfrw import PdfReader, PdfWriter
import xlrd
import os
import PIL

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
fpdf.set_global("SYSTEM_TTFONTS", os.path.join(
    os.path.dirname(__file__), r'C:\Windows\Fonts'))


def create_1C_barcod(case_name, case_art, bar, count):
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
    writer.write(joinpath(r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\ценники',
                          os.path.basename('Чехол для Samsung Galaxy A22 силикон с закрытой камерой с усиленными углами прозрачный.pdf')))


case_name = 'Чехол для Samsung Galaxy A22 силикон с закрытой камерой с усиленными углами прозрачный'
case_art = 'Samsung_A22ПрозрачныйСУсиленнымиУглами'
bar = '2008965273222'
count = 1350
create_1C_barcod(case_name, case_art, bar, count)
