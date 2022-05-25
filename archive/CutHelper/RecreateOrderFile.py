import sys
from numpy import append
import xlrd
import pandas

# Режим отдалки
DEBUG = False
# Неизменяемые настройки из файла конфигурации
pathToOrder = sys.argv[1].replace('#', ' ') if DEBUG == False else  r'C:\Users\Георгий\Downloads\Выгрузка_Документ производства_000000002_от_11_03_2022_стекла.xlsx'
pathToTableTXT = sys.argv[2].replace('#', ' ') if DEBUG == False else  r'C:\Users\Public\Documents\CutHelp\order_table_clear.txt'


def read_xlsx(file_path, title='Yes'):
    '''Считывает построчно xlsx файл и возращает список словарей - если title = 'Yes', список списков - если title = 'No'
    '''
    rd = xlrd.open_workbook(file_path)
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


def readFileWithTable():
    with open(pathToTableTXT, 'r', encoding='ANSI') as file:
        dataTableRAW = file.readlines()
    file.close()
    dataTable = {}
    numsTable = []
    for dataRAW in dataTableRAW:
        orderNum = dataRAW.strip('"').strip('"\n').split(';')[0]
        tableNum = dataRAW.strip('"').strip('"\n').split(';')[1]
        if tableNum not in numsTable:
            numsTable.append(tableNum)
            tmp = {'Стол_{}'.format(tableNum):[]}
            dataTable.update(tmp)
        dataTable['Стол_{}'.format(tableNum)].append(orderNum)
    return dataTable


def createFileWithTable(dataTable, dataFromOrder, material):

    for table in dataTable.keys():
        ordersInFile =[]
        dataOrderForExcel = []
        for orderInTable in dataTable[table]:
            for orderLine in dataFromOrder:
                if orderInTable == orderLine['Номер задания']:
                    if orderLine['Номер задания'] not in ordersInFile:
                        ordersInFile.append(orderLine['Номер задания'])
                        dataOrderForExcel.append(orderLine)
                        break
        dataOrderForExcelpd = pandas.DataFrame(dataOrderForExcel)
        dataOrderForExcelpd.to_excel(pathToOrder.replace('.xlsx','_{}_{}.xlsx'.format(material, table)), index=False)


def main():
    if 'clear' in pathToTableTXT:
        material = 'CL'
    else:
        material = 'MT'
    dataTable = readFileWithTable()
    dataFromOrder = read_xlsx(pathToOrder)
    createFileWithTable(dataTable, dataFromOrder, material)
main()

