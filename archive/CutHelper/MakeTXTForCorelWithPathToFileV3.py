import sys
import xlrd
from os.path import join as joinPath, exists
from os import remove
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QFileDialog, QMainWindow
# from ui import Ui

class test(QMainWindow):
    def __init__(self,parent=None):
        super(test, self).__init__(parent)
        self.pathToOrderFile = QFileDialog.getOpenFileName(self, ("Выберите файл со списком номенклатуры"), r"\\192.168.0.111\shared\Отдел производство\Wildberries\Заказы принты\Заказы Эксель", ("Excel Files (*.xlsx)"))[0]

# Режим отдалки
DEBUG = False
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = test()
    pathToOrder = application.pathToOrderFile
    with open(r'C:\Users\Public\Documents\CutHelp\pathFile.txt', 'w', encoding='ANSI') as file:
        file.write(pathToOrder)
        file.close()
    # application.show()
    # app.exec()
    # startPrintHelper()
# a = test().pathToOrderFile
# a
# Неизменяемые настройки из файла конфигурации
# pathToOrder = sys.argv[1].replace('#', ' ') if DEBUG == False else  r'C:\Users\Георгий\Downloads\A1_122 от 08.05.2022.xlsx'
if not DEBUG:
    pathToOrderTXTForCorel = joinPath(r'C:\Users\Public\Documents\CutHelp', 'order_{}.txt')
    pathToOrderTXTErrorsForCorel = joinPath(__file__,'..', 'errors.txt')
    pathToConfigFile = joinPath(r'C:\Users\Public\Documents\CutHelp', 'Config.txt')
else:
    pathToOrderTXTForCorel = joinPath(__file__,'..', 'order_{}.txt')
    pathToOrderTXTErrorsForCorel = joinPath(__file__,'..', 'errors.txt')
    pathToOrderTXTErrorsForCorel = joinPath(__file__,'..', 'errors.txt')
    pathToConfigFile = joinPath(__file__,'..', 'Config.txt')


# Изменяемые настройки из файла конфигурации
# Настройки по умолчанию, если не заданы аналогичные в файле "Config.txt". Парамерты в конфиге считаются главными и будут являться действующими
pathToMakets = r'\\192.168.0.33\shared\Отдел производство\Wildberries\Макеты для новой программы'
pathToMaketsFile = r'\\192.168.0.33\shared\Отдел производство\Wildberries\Макеты для новой программы\Сопоставление макетов.xlsx'
addForOrder = {"Глянцевые": 'clear',
                "Матовые": 'mate'}
counter = 0                



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
    if exists(pathToConfigFile):
        print('Обнаружен файл конфигурации по адресу {}. Настройки взяты из него. Нажмите Enter чтобы продолжить'.format(pathToConfigFile))
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
                elif lineConfigList[0].strip() == 'pathToMaketsFile':
                    pathToMaketsFileConf = lineConfigList[1].strip() 

        fileConfig.close()
        # Применяем занчения из временных переменных к глобальным переменным только после полного прочения файла
        # Если при прочтении возникло исключение, настройки будут по умолчанию
        global pathToMakets, addForOrder, pathToMaketsFile
        pathToMakets = pathToMaketsConf
        addForOrder = addForOrderConf
        pathToMaketsFile = pathToMaketsFileConf
    else:
        input('Файл конфигурации по адресу {} не обнаружен. Настройки взяты по умолчанию. Путь к макетам {}. Нажмите Enter чтобы продолжить'.format(pathToConfigFile, pathToMakets))


def makeTXTForCorel(dataFromOrder, pathToOrder, add, counter):
    listPathToFile = []
    count = 1
    # counter = 0
    for lineOrder in dataFromOrder:
        count = 1
        if 'Комплект 2' in lineOrder['Название']:
            count = 2
        elif 'Комплект 3' in lineOrder['Название']:
            count = 3
        elif 'Комплект 4' in lineOrder['Название']:
            count = 4
        elif 'Комплект 5' in lineOrder['Название']:
            count = 5
        counter+=count
        flagAdd = False
        barcod = lineOrder['ШК'] if type(lineOrder['ШК']) == str else str(lineOrder['ШК'])[0:-2] if type(lineOrder['ШК']) == float else str(lineOrder['ШК'])
        orderNum  = lineOrder['Номер задания'] if type(lineOrder['Номер задания']) == str else str(lineOrder['Номер задания'])[0:-2] if type(lineOrder['Номер задания']) == float else str(lineOrder['Номер задания'])
        a = read_xlsx(pathToMaketsFile)
        for lineMaketFile in  read_xlsx(pathToMaketsFile):
            if barcod in (lineMaketFile['ШК'] if type(lineMaketFile['ШК']) == str else str(lineMaketFile['ШК'])[0:-2]):
                if exists(path:=joinPath(pathToMakets, lineMaketFile['Файл'])):
                    for i in range(count):
                        listPathToFile.append({'Путь к макету': path,
                                        'Номер задания': orderNum})
                else:
                    print('Ошибка! Для заказа {} не обнаружен макет {} в {}. Нажмите Enter чтобы продолжить'.format(orderNum, lineMaketFile['Файл'], pathToMakets))
                    continue
                flagAdd = True
                break
        if not flagAdd:
            print('Ошибка! Для заказа {} не обнаружен макет. Проверьте штрихкод {} в {}. Нажмите Enter чтобы продолжить'.format(orderNum, barcod, pathToMakets))
            with open(pathToOrder.replace('.xlsx','_{}_errors.txt'.format(add)), 'a', encoding='ANSI') as fileTXTErrors:
                fileTXTErrors.write(orderNum  +';'+barcod+';'+pathToMakets+'\n')
    with open(pathToOrderTXTForCorel.format(add), 'w', encoding='ANSI') as fileTXTForCorel:
        for line in listPathToFile:
            fileTXTForCorel.writelines(';'.join([line['Путь к макету'], line['Номер задания']])+'\n')
    fileTXTForCorel.close()
    input(str(f'Количество стекол в заказе = {counter}'))


def deleteOredrTXT():
    for add in [addForOrder['Глянцевые'], addForOrder['Матовые']]:
        if exists(pathToOrderTXTForCorel.format(add)):
            remove(pathToOrderTXTForCorel.format(add))


def main():
    try:
        # Применяем настройки из файла конфига, если возникает ошибка, настройки остануться по умолчанию
        applyConfig()
    except:
        input('Ошибка при чении и применении файла конфигурации, значения будут заданы по умолчанию. Нажмите Enter чтобы продолжить')
    try:
        dataFromOrder = read_xlsx(pathToOrder)
    except:
        input('Непредвиденная ошибка при чтении файла с заказом. Нажмите Enter чтобы продолжить')
        return 0
    if len(dataFromOrder)==0:
        input('Пустой файл с заказом. Нажмите Enter чтобы продолжить')
        return 0
    try:
        makeTXTForCorel(dataFromOrder)
    except:
        input('Непредвиденная ошибка при формировании файла с путями к макетам для корела. Нажмите Enter чтобы продолжить')

def main2():
# Применяем настройки из файла конфига, если возникает ошибка, настройки остануться по умолчанию
    applyConfig()
    deleteOredrTXT()
    dataFromOrder = read_xlsx(pathToOrder)
    if len(dataFromOrder)==0:
        input('Пустой файл с заказом')
        return 0
    dataFromOrderCL = []
    dataFromOrderMT = []
    for lineOrder in dataFromOrder:
        if lineOrder['Характеристика'] == 'глянцевая':
            dataFromOrderCL.append(lineOrder)
        elif lineOrder['Характеристика'] == 'матовая':
            dataFromOrderMT.append(lineOrder)
        else:
            input('Для заказа {} не удалось определить характеристику (глянец/мат). Проверьте характеристику {} в {}.'.format(lineOrder['Номер задания'], lineOrder['Характеристика'], pathToMakets))
    if len(dataFromOrderCL)==0:
        input('Не обнаружены глянцевые заказы')
    elif len(dataFromOrderMT)==0:
        input('Не обнаружены матовые заказы')
    makeTXTForCorel(dataFromOrderCL, pathToOrder, addForOrder['Глянцевые'], counter)
    makeTXTForCorel(dataFromOrderMT, pathToOrder, addForOrder['Матовые'], counter)
    

main2()