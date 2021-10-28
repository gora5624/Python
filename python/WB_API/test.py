import os
import pandas
import xlrd


file_path = 'C:\Users\user\Desktop\Список самых ходовых тест V2.xlsx'
nameList = 'Стекло производство'


def read_xlsx_by_name(file_path, nameList):
    '''Считывает построчно xlsx файл и возращает список словарей - если title = 'Yes', список списков - если title = 'No'
    '''
    rd = xlrd.open_workbook(file_path)
    try:
        sheet = rd.sheet_by_name(nameList)
    except:
        sheet = rd.sheet_by_name('основной')
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


data = read_xlsx_by_name(file_path, nameList)
for line in data:
    line = {}
    line.update{'Площадь': }
