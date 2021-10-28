import pandas
import os
import sys
import xlrd

#pathToExcel = sys.argv[1:]
pathToOrderFile = 'D:\ФБС принты 26.10.2021 ч1.xlsx'


def read_xlsx(file_path, nameList):
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


def getDataFromOrderFile(pathToOrderFile):
    dataFromOrderFile = read_xlsx(pathToOrderFile, 'Столы')
    return dataFromOrderFile


def splitOrderTable(dataFromOrderFile):
    tableList = {}
    numTable = 1
    nameTable = 'Table_{}'.format(str(numTable))
    if dataFromOrderFile != None:
        for line in dataFromOrderFile:
            if line['Номер задания'] != '':

            pass


dataFromOrderFile = getDataFromOrderFile(pathToOrderFile)
splitOrderTable(dataFromOrderFile)
