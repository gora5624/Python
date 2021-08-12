import base64
import barcode
from barcode.writer import ImageWriter
from fpdf import FPDF
import requests
import json
import pandas
from datetime import datetime, timedelta
from my_lib import file_exists
from os.path import join as joinpath
from os import mkdir
from os.path import isfile
from shutil import copyfile
import PyPDF2
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from pdfrw import PdfReader, PdfWriter
import xlrd

# OrderFileName = r'ФБС принты 11.08.21.xlsx'
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

dirList = [main_path, WBOrdersData, OrdersDir, TMPDir]
for dir_ in dirList:
    if not file_exists(dir_):
        mkdir(dir_)


def read_xlsx(file_path, num=0, title='Yes'):
    '''Считывает построчно xlsx файл и возращает список словарей - если title = 'Yes', список списков - если title = 'No'
    '''
    rd = xlrd.open_workbook(file_path)
    sheet = rd.sheet_by_index(num)
    if title == 'Yes':
        Name_row = sheet.row_values(0)
        start = 1
    elif title == 'No':
        Name_row = None
        start = 0
    data = []
    for rownum in range(start, sheet.nrows):
        row = sheet.row_values(rownum)
        if title == 'Yes':
            dct = {}
            for i, cel in enumerate(row):
                tmp = {Name_row[i]: cel}
                dct.update(tmp)
            data.append(dct)
        elif title == 'No':
            data.append(row)
    return data


def get_orders(days):
    with open(Token_path, 'r', encoding='UTF-8') as file:
        Token = file.read()
        file.close()
    print("Идёт получение свежих заказов, ожидайте...")
    Url = 'https://suppliers-api.wildberries.ru/api/v2/orders?date_start={}%2B03%3A00&take=1000&skip={}'

    start_data = (datetime.today() - timedelta(days=int(days))).isoformat('T', 'seconds').replace(
        ':', '%3A').replace('+', '%2B').replace('.', '%2E')
    count_skip = 0
    data = '123'
    all_data = pandas.DataFrame()
    while len(data) > 0:
        response = requests.get(Url.format(start_data, count_skip), headers={
            'Authorization': '{}'.format(Token)})
        if response.status_code != 200:
            print('Не удалось получить заказы, ошибка на стороне ВБ.')
            return 1
        count_skip = count_skip+1000
        data = response.json()['orders']
        for line in data:
            line.update(wbStickerEncoded=line['sticker']['wbStickerEncoded'])
            line.update(
                wbStickerSvgBase64=line['sticker']['wbStickerSvgBase64'])
        with open(joinpath(WBOrdersData, WBOrdersJsonDataFileName), 'w') as file:
            json.dump(data, file)
        file.close()
        tmp = pandas.read_json(
            joinpath(WBOrdersData, WBOrdersJsonDataFileName))
        all_data = all_data.append(tmp)
    all_data.to_excel(joinpath(WBOrdersData,
                               WBOrdersDataFileName), index=False)
    copyfile(joinpath(WBOrdersData, WBOrdersDataFileName),
             joinpath(r"D:\\", WBOrdersDataFileName))
    return 0


def recreate_data(order_xlsx):
    order_xlsx
    data_new = {}
    for line in order_xlsx:
        Order_num = str(line['orderId'])[0:-2]
        data_new[Order_num] = {'Номер задания': Order_num,
                               'Баркод': str(line['barcode'])[0:-2],
                               'Информация в стикере': line['wbStickerEncoded'],
                               'Стикер64': line['wbStickerSvgBase64']}
    return data_new


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
    pdf.set_font('DejaVu', '', 60)
    pdf.multi_cell(350, 25, txt="{}".format(
        case_name))
    pdf.add_font(
        'DejaVu', '', r'C:\Users\user\Downloads\font\DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 40)
    pdf.multi_cell(350, 24, txt="{}".format(
        case_art))
    pdf.multi_cell(350, 24, txt="{}".format(
        'Продавец: ИП Караханян Э.С'))
    pdf.output(r'D:\1C_barcod.pdf')
    return r'D:\1C_barcod.pdf'


def create_WB_barcod(Base64):
    Base64 = bytes(Base64, 'utf-8')
    pdf_writer = PyPDF2.PdfFileWriter()
    png_recovered = base64.decodestring(Base64)
    f = open(r'D:\WB_barcod.PDF.SVG', "wb")
    f.write(png_recovered)
    f.close()
    drawing = svg2rlg(r'D:\WB_barcod.PDF.SVG')
    renderPDF.drawToFile(drawing, r'D:\WB_barcod_tmp.PDF')
    pdf_file = PyPDF2.PdfFileReader(
        open(r'D:\WB_barcod_tmp.PDF', 'rb'))
    page = pdf_file.getPage(0)
    page.mediaBox.upperRight = (370, 280)
    page.mediaBox.upperLeft = (20, 280)
    page.mediaBox.lowerRight = (370, 15)
    page.scaleBy(3)
    pdf_writer.addPage(page)
    with open(r'D:\WB_barcod.PDF', 'wb') as out_file:
        pdf_writer.write(out_file)
    return r'D:\WB_barcod.PDF'


def create_1C_name(name):
    size = (370, 280)
    pdf = FPDF(format=size)
    pdf.add_page()
    pdf.add_font(
        'DejaVu', '', r'C:\Users\user\Downloads\font\DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 70)
    pdf.multi_cell(350, 35, txt="{}".format(
        name))
    pdf.output(r'D:\name.pdf')
    return r'D:\name.pdf'


if str(input('Получить новые заказы? 1 - Да, 2 - Нет: ')) == str(1):
    days = input(
        "Ведите количество дней, за которое нужно получить заказы или нажмите Enter: ")
    if days == '':
        days = 10
    resp = get_orders(days)
else:
    resp = 0

# Режим печати
'''
print('1 - режим печати по столам')
print('2 - режим печати с разбивкой на модели')
mode = int(input('Введите режим печати: '))
print('1 или Enter - режим по умолчанию (Название модели или стола, ценник 1С, этикетка ВБ)')
print('2 - название модели или стола, этикетка ВБ')
print('3 - этикетка ВБ')
print('4 - название модели или стола, ценник 1С')
print('5 - ценник 1С')
mode2 = int(input('Введите 2й режим печати: '))
'''

if resp == 0:
    print("Заказы успешно получены, идём дальше")
    OrderFileName = input(
        'Название файла (Если он в папке Oreders) или полный путь до файла (Если он в другой папке): ')
    if OrderFileName[-5:len(OrderFileName)] != '.xlsx':
        OrderFileName = OrderFileName + '.xlsx'
    if file_exists(OrderFileName) and isfile(joinpath(OrdersDir, OrderFileName)):
        print('Файл найден.')
        Flag = True
    elif file_exists(joinpath(OrdersDir, OrderFileName)) and isfile(joinpath(OrdersDir, OrderFileName)):
        OrderFileName = joinpath(OrdersDir, OrderFileName)
        print('Файл найден.')
        Flag = True
    else:
        print('Файл Не найден.')
        Flag = False
    if Flag:
        data_from_order = read_xlsx(joinpath(
            OrdersDir, OrderFileName))
        data_about_order = recreate_data(
            read_xlsx(joinpath(WBOrdersData, r'Data_order.xlsx')))
        data_for_print = {}
        for order in data_from_order:
            if order['Название'].replace('\xa0', ' ') not in data_for_print:
                data_for_print[order['Название'].replace('\xa0', ' ')] = []
            else:
                continue
        for order in data_from_order:
            if type(order['ШК']) == float:
                bar = str(order['ШК'])[0:-2]
            else:
                bar = order['ШК']
            if type(order['Номер задания']) == float:
                num_ord = str(order['Номер задания'])[0:-2]
            else:
                num_ord = order['Номер задания']

            tmp = {'Название': order['Название'].replace('\xa0', ' '),
                   'Этикетка': order['Этикетка'],
                   'ШК': bar,
                   'Артикул поставщика': order['Артикул поставщика'],
                   'Номер задания': num_ord,
                   'Информация в стикере': data_about_order[num_ord]['Информация в стикере'],
                   'Стикер64': data_about_order[num_ord]['Стикер64']}
            data_for_print[order['Название'].replace('\xa0', ' ')].append(tmp)
        writer = PdfWriter()
        for name in data_for_print:
            path1 = PdfReader(create_1C_name(name), decompress=False).pages
            # writer.addpages(path1)
            for data in data_for_print[name]:
                path2 = PdfReader(create_1C_barcod(data['Название'],
                                                   data['Артикул поставщика'], data['ШК']), decompress=False).pages
                writer.addpages(path2)
                path3 = PdfReader(create_WB_barcod(
                    data['Стикер64']), decompress=False).pages
                # writer.addpages(path3)
else:
    print("Не удалось получить заказы")

writer.write(joinpath(main_path, r'result.pdf'))
