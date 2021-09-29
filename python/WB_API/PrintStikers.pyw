from ntpath import join
import sys
import os

from mydesign import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
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
from os import makedirs, remove
from os.path import join
import PyPDF2
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from pdfrw import PdfReader, PdfWriter
import xlrd
import multiprocessing


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.btnClicked)
        self.ui.pushButton_2.clicked.connect(self.updateComboBox)
        for excel in os.listdir(pathToOrders):
            if '~' not in excel:
                self.ui.comboBox.addItem(
                    excel) if '~' not in excel else self.ui.comboBox

    def updateComboBox(self):
        self.ui.comboBox.clear()
        for excel in os.listdir(pathToOrders):
            if '~' not in excel:
                self.ui.comboBox.addItem(
                    excel) if '~' not in excel else self.ui.comboBox
        self.ui.textEdit.setText('Обновление списка заказов выполненно')

    def btnClicked(self, a):
        self.ui.textEdit.setText('Ожидайте, идёт формирование ценников')
        text = self.ui.comboBox.currentText()
        t1 = multiprocessing.Process(
            target=main, args=(os.path.join(pathToOrders, text), str(datetime.today()).replace(":", '.'),))

        t1.start()

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox.question(self,
                                               "Выход",
                                               "Вы уверенны что хотите закрыть программу?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            try:
                for tmpFile in os.listdir(TMPDir):
                    remove(join(TMPDir, tmpFile))
            except:
                pass
            event.accept()
        else:
            event.ignore()


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
NameTitle1CStiker = 'Name{}.pdf'
NameEAN13PNG = 'ean13_{}.png'
NameTable = 'TBL_{}.pdf'


def startChek():
    dirList = [main_path, WBOrdersData, TMPDir]
    for dir_ in dirList:
        if not file_exists(dir_):
            makedirs(dir_)
    if not file_exists(Token_path):
        print('Токен авторизации по адресу {} не обнаружен, получение заказов невозможно.'.format(
            Token_path))
        with open(Token_path, 'w', encoding='UTF-8') as file:
            file.close()
        return 1
    return 0


def read_xlsx(file_path, num=0, title='Yes'):
    '''Считывает построчно xlsx файл и возращает список словарей - если title = 'Yes', список списков - если title = 'No'
    '''
    rd = xlrd.open_workbook(file_path)
    try:
        sheet = rd.sheet_by_index(num)
    except:
        print("Введено некорректное число листов, читаю лист 1")
        sheet = rd.sheet_by_index(0)
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


def read_xlsx_by_name(file_path, nameList):
    '''Считывает построчно xlsx файл и возращает список словарей - если title = 'Yes', список списков - если title = 'No'
    '''
    rd = xlrd.open_workbook(file_path)
    sheet = rd.sheet_by_name(nameList)
    try:
        Name_row = sheet.row_values(0)
    except IndexError:
        return None
    start = 1
    data = []
    for rownum in range(start, sheet.nrows):
        row = sheet.row_values(rownum)
        dct = {}
        for i, cel in enumerate(row):
            tmp = {Name_row[i]: cel}
            dct.update(tmp)
        data.append(dct)
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
        trying = 0
        while True:
            trying += 1
            try:
                response = requests.get(Url.format(start_data, count_skip), headers={
                    'Authorization': '{}'.format(Token)})
                if response.status_code == 200:
                    break
                elif trying > 500:
                    print("Не удолось достучаться до сервера ВБ")
                    return 1
                else:
                    continue
            except:
                continue
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


def create_1C_barcod(case_name, case_art, bar, procNum):
    options = dict(module_height=5.0, text_distance=1.0, format='PNG')

    barcode.get('ean13', bar,
                ImageWriter()).save(joinpath(TMPDir, NameEAN13PNG.format(procNum)[0:-4]), options)
    image_path = joinpath(TMPDir, NameEAN13PNG.format(procNum))
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
    pdf.output(joinpath(TMPDir, Name1CStiker.format(procNum)))
    return joinpath(TMPDir, Name1CStiker.format(procNum))


def create_WB_barcod(Base64, procNum):
    Base64 = bytes(Base64, 'utf-8')
    pdf_writer = PyPDF2.PdfFileWriter()
    png_recovered = base64.decodestring(Base64)
    f = open(joinpath(TMPDir, NameSVG.format(procNum)), "wb")
    f.write(png_recovered)
    f.close()
    drawing = svg2rlg(joinpath(TMPDir, NameSVG.format(procNum)))
    renderPDF.drawToFile(drawing, joinpath(
        TMPDir, NameWBStikerTMP.format(procNum)))
    pdf_file = PyPDF2.PdfFileReader(
        open(joinpath(TMPDir, NameWBStikerTMP.format(procNum)), 'rb'))
    page = pdf_file.getPage(0)
    page.mediaBox.upperRight = (370, 280)
    page.mediaBox.upperLeft = (20, 280)
    page.mediaBox.lowerRight = (370, 15)
    page.scaleBy(3)
    pdf_writer.addPage(page)
    with open(joinpath(TMPDir, NameWBStiker.format(procNum)), 'wb') as out_file:
        pdf_writer.write(out_file)
    return joinpath(TMPDir, NameWBStiker.format(procNum))


def create_1C_name(name, file_order_name, procNum):
    size = (370, 280)
    pdf = FPDF(format=size)
    pdf.add_page()
    pdf.add_font(
        'Arial', '', fname="Arial.ttf", uni=True)
    pdf.set_font('Arial', '', 70)
    pdf.multi_cell(350, 35, txt="{}".format(
        name))
    pdf.set_font('Arial', '', 50)
    pdf.multi_cell(350, 35, txt="{}".format(
        os.path.basename(file_order_name)), align="C")
    pdf.output(joinpath(TMPDir, NameTitle1CStiker.format(procNum)))
    return joinpath(TMPDir, NameTitle1CStiker.format(procNum))


def makeTableStiker(table_num, file_order_name, procNum):
    size = (370, 280)
    pdf = FPDF(format=size)
    pdf.add_page()
    pdf.add_font(
        'Arial', '', fname="Arial.ttf", uni=True)
    pdf.set_font('Arial', '', 200)
    pdf.multi_cell(350, 190, txt="Стол {}".format(
        str(table_num)), align='C')
    pdf.set_font('Arial', '', 50)
    pdf.multi_cell(350, 30, txt='{}'.format(
        os.path.basename(file_order_name)), align="C")
    pdf.output(joinpath(TMPDir, NameTable.format(procNum)))
    return joinpath(TMPDir, NameTable.format(procNum))


def menu():
    # Режим печати

    print('1 - режим печати с разбивкой на модели (По умолчанию)')
    print('2 - режим печати с разбивкой на столы')
    mode = 1
    mode_tmp = input('Введите режим печати: ')
    if mode_tmp == '':
        mode = 1
    else:
        try:
            mode = int(mode_tmp)
        except:
            print('Введён неверный режим, установлен режим по умолчанию')
            mode = 1
    print('1 или Enter - название модели или стола, ценник 1С, этикетка ВБ (По умолчанию)')
    print('2 - название модели или стола, этикетка ВБ')
    print('3 - этикетка ВБ')
    print('4 - название модели или стола, ценник 1С')
    print('5 - ценник 1С')
    mode2 = 1
    mode2_tmp = input('Введите режим печати: ')
    if mode2_tmp == '':
        mode2 = 1
    else:
        try:
            mode2 = int(mode2_tmp)
        except:
            print('Введён неверный режим, установлен режим по умолчанию')
            mode2 = 1
    return mode, mode2


def make_with_name(OrderFileName, mode2, days, procNum):

    data_from_order = read_xlsx_by_name(joinpath(OrderFileName), 'основной')
    data_about_order = recreate_data(
        read_xlsx(joinpath(WBOrdersData, WBOrdersDataFileName)))
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
        try:
            tmp = {'Название': order['Название'].replace('\xa0', ' '),
                   'Этикетка': order['Этикетка'],
                   'ШК': bar,
                   'Артикул поставщика': order['Артикул поставщика'],
                   'Номер задания': num_ord,
                   'Информация в стикере': data_about_order[num_ord]['Информация в стикере'],
                   'Стикер64': data_about_order[num_ord]['Стикер64']}
        except KeyError:
            get_orders(days)
            return make_with_name(OrderFileName, mode2, days, procNum)
        data_for_print[order['Название'].replace(
            '\xa0', ' ')].append(tmp)
    writer = PdfWriter()
    for name in data_for_print:
        if mode2 == 1 or mode2 == 2 or mode2 == 4:
            path1 = PdfReader(create_1C_name(
                name, OrderFileName, procNum), decompress=False).pages
            writer.addpages(path1)
        for data in data_for_print[name]:
            if mode2 == 1 or mode2 == 5 or mode2 == 4:
                path2 = PdfReader(create_1C_barcod(data['Название'],
                                                   data['Артикул поставщика'], data['ШК'], procNum), decompress=False).pages
                writer.addpages(path2)
            if mode2 == 1 or mode2 == 3 or mode2 == 2:
                path3 = PdfReader(create_WB_barcod(
                    data['Стикер64'], procNum), decompress=False).pages
                writer.addpages(path3)

    writer.write(joinpath(r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\ценники',
                          os.path.basename(OrderFileName.replace('.xlsx', '.pdf'))))


def make_glass_body(OrderFileName, mode2, name_sheet, days, procNum):
    data_from_order = read_xlsx_by_name(OrderFileName, name_sheet)
    if data_from_order == None:
        return 0
    data_about_order = recreate_data(
        read_xlsx(joinpath(WBOrdersData, WBOrdersDataFileName)))
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
        try:
            tmp = {'Название': order['Название'].replace('\xa0', ' '),
                   'Этикетка': order['Этикетка'],
                   'ШК': bar,
                   'Артикул поставщика': order['Артикул поставщика'],
                   'Номер задания': num_ord,
                   'Информация в стикере': data_about_order[num_ord]['Информация в стикере'],
                   'Стикер64': data_about_order[num_ord]['Стикер64']}
        except KeyError:
            get_orders(days)
            return make_glass_body(OrderFileName, mode2, name_sheet, days, procNum)
        data_for_print[order['Название'].replace(
            '\xa0', ' ')].append(tmp)
    writer = PdfWriter()
    for name in data_for_print:
        if mode2 == 1 or mode2 == 2 or mode2 == 4:
            path1 = PdfReader(create_1C_name(
                name, OrderFileName, procNum), decompress=False).pages
            writer.addpages(path1)
        for data in data_for_print[name]:
            if mode2 == 1 or mode2 == 5 or mode2 == 4:
                path2 = PdfReader(create_1C_barcod(data['Название'],
                                                   data['Артикул поставщика'], data['ШК'], procNum), decompress=False).pages
                writer.addpages(path2)
            if mode2 == 1 or mode2 == 3 or mode2 == 2:
                path3 = PdfReader(create_WB_barcod(
                    data['Стикер64'], procNum), decompress=False).pages
                writer.addpages(path3)
    return writer


def make_glass(OrderFileName, days, procNum):
    day = datetime.today().date().strftime(r"%d.%m.%Y")
    writer = make_glass_body(OrderFileName, 1, '3D_стекла', days, procNum)
    if writer != 0:
        writer.write(
            joinpath(r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\ценники', '3D1_{}.pdf'.format(day)))
    writer = make_glass_body(OrderFileName, 4, '3D_стекла', days, procNum)
    if writer != 0:
        writer.write(
            joinpath(r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\ценники', '3D2_{}.pdf'.format(day)))
    writer = make_glass_body(OrderFileName, 1, 'глянец', days, procNum)
    if writer != 0:
        writer.write(
            joinpath(r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\ценники', 'GL1_{}.pdf'.format(day)))
    writer = make_glass_body(OrderFileName, 4, 'глянец', days, procNum)
    if writer != 0:
        writer.write(
            joinpath(r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\ценники', 'GL2_{}.pdf'.format(day)))
    writer = make_glass_body(OrderFileName, 1, 'матовые', days, procNum)
    if writer != 0:
        writer.write(
            joinpath(r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\ценники', 'MT1_{}.pdf'.format(day)))
    writer = make_glass_body(OrderFileName, 4, 'матовые', days, procNum)
    if writer != 0:
        writer.write(
            joinpath(r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\ценники', 'MT2_{}.pdf'.format(day)))
    writer = make_glass_body(OrderFileName, 1, 'камеры', days, procNum)
    if writer != 0:
        writer.write(
            joinpath(r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\ценники', 'Cam_{}.pdf'.format(day)))


def make_with_table(OrderFileName, mode2, days, procNum):

    data_from_order = read_xlsx_by_name(OrderFileName, 'основной')
    data_about_tale = read_xlsx_by_name(OrderFileName, 'Столы')
    data_about_order = recreate_data(
        read_xlsx(joinpath(WBOrdersData, WBOrdersDataFileName)))
    data_for_print = {}
    for order in data_from_order:
        if type(order['Номер задания']) == float:
            ord_num = str(order['Номер задания'])[0:-2]
        else:
            ord_num = order['Номер задания']
        data_for_print[ord_num] = []

    for order in data_from_order:
        if type(order['ШК']) == float:
            bar = str(order['ШК'])[0:-2]
        else:
            bar = order['ШК']
        if type(order['Номер задания']) == float:
            num_ord = str(order['Номер задания'])[0:-2]
        else:
            num_ord = order['Номер задания']

        try:
            tmp = {'Название': order['Название'].replace('\xa0', ' '),
                   'Этикетка': order['Этикетка'],
                   'ШК': bar,
                   'Артикул поставщика': order['Артикул поставщика'],
                   'Номер задания': num_ord,
                   'Информация в стикере': data_about_order[num_ord]['Информация в стикере'],
                   'Стикер64': data_about_order[num_ord]['Стикер64']}
        except KeyError:
            get_orders(days)
            return make_with_table(OrderFileName, mode2, days, procNum)
        data_for_print[num_ord].append(tmp)
    writer = PdfWriter()
    table_num = 1
    if mode2 == 1 or mode2 == 2 or mode2 == 4:
        path1 = PdfReader(makeTableStiker(
            table_num, OrderFileName, procNum), decompress=False).pages
        writer.addpages(path1)
    for order_line in data_about_tale:
        if type(order_line['Номер задания']) == float:
            order_line_num = str(order_line['Номер задания'])[0:-2]
        else:
            order_line_num = order_line['Номер задания']
        if mode2 == 1 or mode2 == 2 or mode2 == 4:
            if order_line_num == '':
                table_num = table_num + 1
                path1 = PdfReader(makeTableStiker(
                    table_num, OrderFileName, procNum), decompress=False).pages
                writer.addpages(path1)
                continue
        for data in data_for_print[order_line_num]:
            if mode2 == 1 or mode2 == 5 or mode2 == 4:
                path2 = PdfReader(create_1C_barcod(data['Название'],
                                                   data['Артикул поставщика'], data['ШК'], procNum), decompress=False).pages
                writer.addpages(path2)
            if mode2 == 1 or mode2 == 3 or mode2 == 2:
                path3 = PdfReader(create_WB_barcod(
                    data['Стикер64'], procNum), decompress=False).pages
                writer.addpages(path3)

    writer.write(joinpath(r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\ценники',
                          os.path.basename(OrderFileName.replace('.xlsx', '.pdf'))))

    # Тело


def main(text, procNum):

    if startChek() == 0:

        OrderFileName = text
        if 'ч1' in OrderFileName:
            days = 3
        else:
            days = 1
        if 'ФБС стекла' in OrderFileName:
            make_glass(OrderFileName, days, procNum)
        elif 'ФБС без принтов' in OrderFileName or 'ФБС планки принты' in OrderFileName:
            make_with_name(OrderFileName, 1, days, procNum)
        elif 'ФБС принты' in OrderFileName:
            make_with_table(OrderFileName, 1, days, procNum)
        else:
            mode, mode2 = menu()
            if mode == 1:
                make_with_name(OrderFileName, mode2, days, procNum)
            elif mode == 2:
                make_with_table(OrderFileName, mode2, days, procNum)


if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()

    sys.exit(app.exec())
