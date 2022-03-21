import sys
import xlrd
from os.path import join as joinPath, exists
from os import listdir, remove



# Режим отдалки
DEBUG = False
# Неизменяемые настройки из файла конфигурации
pathToOrder = sys.argv[1].replace('#', ' ') if DEBUG == False else  r'C:\Users\Георгий\Downloads\Выгрузка_Документ производства_000000002_от_11_03_2022_стекла.xlsx'
if not DEBUG:
    pathToOrderTXTForCorel = joinPath(r'C:\Users\Public\Documents\CutHelp', 'order_{}.txt')
    pathToConfigFile = joinPath(r'C:\Users\Public\Documents\CutHelp', 'Config.txt')
else:
    pathToOrderTXTForCorel = joinPath(__file__,'..', 'order_{}.txt')
    pathToConfigFile = joinPath(__file__,'..', 'Config.txt')


# Изменяемые настройки из файла конфигурации
# Настройки по умолчанию, если не заданы аналогичные в файле "Config.txt". Парамерты в конфиге считаются главными и будут являться действующими
pathToMakets = r'E:\Макеты'
addForOrder = {"Глянцевые": 'clear',
                "Матовые": 'mate'}



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


def applyConfig():
    # Открываем и читаем файл конфига
    print(pathToConfigFile)
    with open(pathToConfigFile, 'r', encoding='utf-8') as fileConfig:
        dataConfig = fileConfig.readlines()
        for lineConfig in dataConfig:
            # Построчно считываем текст файла и разбираем его
            lineConfigList = lineConfig.split('#')[0].split('=')
            # Если находим сопоставимые значения, записываем новые параметры во временные переменные
            if lineConfigList[0].strip() == 'pathToMakets':
                pathToMaketsConf = lineConfigList[1].strip() 
            elif lineConfigList[0].strip() == 'addForOrder':
                addForOrderConf= {"Глянцевые": lineConfigList[1].split(',')[0].strip(),
                                  "Матовые": lineConfigList[1].split(',')[1].strip()}
    fileConfig.close()
    # Применяем занчения из временных переменных к глобальным переменным только после полного прочения файла
    # Если при прочтении возникло исключение, настройки будут по умолчанию
    global pathToMakets, addForOrder
    pathToMakets = pathToMaketsConf
    addForOrder = addForOrderConf


def makeTXTForCorel(dataFromOrder, add):
    listPathToFile = []
    
    for lineOrder in dataFromOrder:
        flagAdd = False
        barcod = lineOrder['ШК'] if type(lineOrder['ШК']) == str else str(lineOrder['ШК'])[0:-2] if type(lineOrder['ШК']) == float else str(lineOrder['ШК'])
        orderNum  = lineOrder['Номер задания'] if type(lineOrder['Номер задания']) == str else str(lineOrder['Номер задания'])[0:-2] if type(lineOrder['Номер задания']) == float else str(lineOrder['Номер задания'])
        for nameMaketFile in listdir(pathToMakets):
            if barcod in nameMaketFile:
                listPathToFile.append({'Путь к макету': joinPath(pathToMakets, nameMaketFile),
                                       'Номер задания': orderNum})
                flagAdd = True
                break
        if not flagAdd:
            print('Для заказа {} не обнаружен макет. Проверьте штрихкод {} в {}.'.format(orderNum, barcod, pathToMakets))
    with open(pathToOrderTXTForCorel.format(add), 'w', encoding='ANSI') as fileTXTForCorel:
        for line in listPathToFile:
            fileTXTForCorel.writelines(';'.join([line['Путь к макету'], line['Номер задания']])+'\n')
    fileTXTForCorel.close()


def deleteOredrTXT():
    for add in [addForOrder['Глянцевые'], addForOrder['Матовые']]:
        if exists(pathToOrderTXTForCorel.format(add)):
            remove(pathToOrderTXTForCorel.format(add))


def main():
    try:
        # Применяем настройки из файла конфига, если возникает ошибка, настройки остануться по умолчанию
        applyConfig()
    except:
        print('Ошибка при чении и применении файла конфигурации, значения будут заданы по умолчанию.')
    try:
        dataFromOrder = read_xlsx(pathToOrder)
    except:
        print('Непредвиденная ошибка при чтении файла с заказом')
        return 0
    if len(dataFromOrder)==0:
        print('Пустой файл с заказом')
        return 0
    try:
        makeTXTForCorel(dataFromOrder)
    except:
        print('Непредвиденная ошибка при формировании файла с путями к макетам для корела.')

def main2():
# Применяем настройки из файла конфига, если возникает ошибка, настройки остануться по умолчанию
    print(pathToConfigFile)
    applyConfig()
    deleteOredrTXT()
    dataFromOrder = read_xlsx(pathToOrder)
    if len(dataFromOrder)==0:
        print('Пустой файл с заказом')
        return 0
    dataFromOrderCL = []
    dataFromOrderMT = []
    for lineOrder in dataFromOrder:
        if lineOrder['Характеристика'] == 'глянцевая':
            dataFromOrderCL.append(lineOrder)
        elif lineOrder['Характеристика'] == 'матовая':
            dataFromOrderMT.append(lineOrder)
        else:
            print('Для заказа {} не удалось определить характеристику (глянце/мат). Проверьте характеристику {} в {}.'.format(lineOrder['Номер задания'], lineOrder['Характеристика'], pathToMakets))
    if len(dataFromOrderCL)==0:
        print('Не обнаружены глянцевые заказы')
    elif len(dataFromOrderMT)==0:
        print('Не обнаружены матовые заказы')
    makeTXTForCorel(dataFromOrderCL, addForOrder['Глянцевые'])
    makeTXTForCorel(dataFromOrderMT, addForOrder['Матовые'])
    

main2()