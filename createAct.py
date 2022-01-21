from dataclasses import dataclass
import re
import requests
from datetime import timedelta, datetime
import base64
from os.path import join as joinpath
import pandas
import os
import fpdf
from fpdf import FPDF
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
import io
from PIL import Image


pathToPDFAct = r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\Акт'
namePDFAct = r'Акт приёма передачи груза от {}.pdf'.format(
    datetime.today().date().strftime(r"%d.%m.%Y"))
fullPathToPDFAct = joinpath(pathToPDFAct, namePDFAct)
Token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjgyYTU2OGZlLTgyNTctNGQ2Yi05ZTg1LTJkYTgxMTgxYWI3MSJ9.ROCdF7eOfTZA-atpsLGTAi15yDzHk2UMes05vwjZwn4'


fpdf.set_global("SYSTEM_TTFONTS", os.path.join(
    os.path.dirname(__file__), r'C:\Windows\Fonts'))


def createPDFAct(listBox):
    size = (2480, 3510)
    pdf = FPDF(format=size)
    pdf.add_page()
    pdf.add_font(
        'Arial', '', fname="Arial.ttf", uni=True)
    pdf.set_font('Arial', '', 150)
    pdf.set_margins(200, 0, 200)
    pdf.multi_cell(2080, 100)
    pdf.multi_cell(2080, 100, txt='Акт приёма передачи груза от {}'.format(
        datetime.today().date().strftime(r"%d.%m.%Y")), align='C')
    pdf.multi_cell(2080, 100)
    pdf.multi_cell(
        2080, 70, txt='Отправитель: ИП Караханян Э.С., ИНН: 561000521896', align='L')
    pdf.multi_cell(2080, 40)
    pdf.multi_cell(
        2080, 70, txt='Получатель: ООО Вайлдберриз, ИНН: 7721546864', align='L')
    pdf.multi_cell(2080, 40)
    pdf.multi_cell(
        2080, 70, txt='Адрес доставки: г. Оренбург, ул. Беляевская 4/4, ворота №1, пункт приёма ООО Вайлдберриз', align='L')
    pdf.multi_cell(2080, 40)
    pdf.multi_cell(
        2080, 70, txt='Срок доставки груза: не позднее 19:30 {}'.format(
            datetime.today().date().strftime(r"%d.%m.%Y")), align='L')
    pdf.multi_cell(2080, 40)
    pdf.multi_cell(
        2080, 70, txt='Перевозчик: ИП Петриченко Н.Н., ИНН: 561108874449', align='L')
    pdf.multi_cell(2080, 80)
    strListBox = ', '.join(listBox)
    pdf.multi_cell(
        2080, 70, txt='Настоящий документ подтверждает, что "Отправитель" передал, а "Перевозчик" принял коробы со следующими номерами: {}, общим количеством {} шт..'.format(strListBox, str(len(listBox))), align='L')
    pdf.multi_cell(2080, 200)
    pdf.multi_cell(
        2080, 70, txt='Представитель отправителя ______________________________', align='L')
    pdf.multi_cell(
        2080, 70, txt='Дата_______________', align='L')
    pdf.multi_cell(2080, 70)
    pdf.multi_cell(
        2080, 70, txt='Представитель перевозчика _______________________________', align='L')
    pdf.multi_cell(
        2080, 70, txt='Дата_______________', align='L')

    pdf.output(fullPathToPDFAct)
    input('Акт готов, нажмите Enter.')


def getListSupply():
    ListSupply = []
    Url = 'https://suppliers-api.wildberries.ru/api/v2/supplies?status=ON_DELIVERY'
    response = requests.get(Url, headers={
        'Authorization': '{}'.format(Token)})
    if response.status_code != 200:
        print('Не удалось получить список поставок, попробоуйте позже.')
        return 0
    for supply in response.json()['supplies']:
        ListSupply.append(supply['supplyId'])
    if len(ListSupply) == 0:
        print('Не удалось получить список поставок, попробоуйте позже.')
        return 0
    return ListSupply


def getListBox():
    listBox = []
    listSupply = getListSupply()
    if listSupply == 0:
        return 0
    tmpSupply = input(
        'Отсканируйте поставку, "0" чтобы закончить сканирование: ')
    while tmpSupply != '0':
        if tmpSupply not in listSupply:
            print(
                'Поставки нет в списке, проверьте корректность ввода номер поставки, либо на ВБ неполадки.')
        else:
            if tmpSupply not in listBox:
                listBox.append(tmpSupply)
            else:
                print('Поставка {} уже добавлена.'.format(tmpSupply))
        tmpSupply = input(
            'Отсканируйте поставку, "0" чтобы закончить сканирование: ')
    if len(listBox) == 0:
        print('В акт не добавлено ни одной поставки.')
    return listBox


# def getListBox1():
#     listBox = []
#     listSupply = getListSupply()
#     # if listSupply == 0:
#     #     return 0
#     # tmpSupply = input(
#     #     'Отсканируйте поствку, "0" чтобы закончить сканирование: ')
#     # while tmpSupply != '0':
#     #     if tmpSupply not in listSupply:
#     #         print(
#     #             'Поставки нет в списке, проверьте корректность воода номер поставки, либо на ВБ неполадки.')
#     #     else:
#     #         if tmpSupply not in listBox:
#     #             listBox.append(tmpSupply)
#     #         else:
#     #             print('Поставка {} уже добавленна.'.format(tmpSupply))
#     #     tmpSupply = input(
#     #         'Отсканируйте поствку, "0" чтобы закончить сканирование: ')
#     # if len(listBox) == 0:
#     #     print('В акт не добавлено ни одной поставки.')
#     return listSupply[0:100]


getListSupply()
listBox = getListBox()
createPDFAct(listBox)