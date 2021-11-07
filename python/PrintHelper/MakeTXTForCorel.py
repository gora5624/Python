import sys
import xlrd
from os.path import join as joinpath
from my_lib import file_exists
from os import makedirs


# pathToOrderFile = sys.argv[1:][0].replace('#', ' ')
pathToOrderFile = r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\Новые\ФБС принты 05.11.2021 ч3.xlsx'
mainPath = r'C:\Users\Public\Documents\WBHelpTools\PrintHelper'
pathToExcelWithSize = r'\\192.168.0.33\shared\Отдел производство\Wildberries\список печати.xlsx'
pathToPrint = r'\\192.168.0.33\shared\Отдел производство\макеты для принтера\Макеты для 6090'
pathToSizeFile = r'C:\Users\Public\Documents\WBHelpTools\PrintHelper\size.txt'
pathToBug = r'\\192.168.0.33\shared\Отдел производство\макеты для принтера\Макеты для 6090\Bug\print 0.cdr'

# Режим отладки True - да, False - боевой режим
Debug = True


pathToTables = joinpath(mainPath, 'Tables')
pathToConfig = joinpath(mainPath, 'config.txt')
pathDebug = joinpath(mainPath, 'debug')
listSize = ['13', '13 min', '13 pm', 'L', 'M', 'MS', 'S', 'XL', 'XS', 'Книга']
dataWithSizePath = {}
tableSize = ['925', '535']
startPoint = ['47.569', '92.508']
XDelta = '83'
YDelta = '175'


def applyConfig():
    with open(pathToConfig, 'r') as fileConfig:
        dataConfig = fileConfig.readlines()
        for data in dataConfig:
            data = data.split('=')
            if data[0].strip() == 'mainPath':
                global mainPath
                mainPath = data[1].strip()
            elif data[0].strip() == 'pathToExcelWithSize':
                global pathToExcelWithSize
                pathToExcelWithSize = data[1].strip()
            elif data[0].strip() == 'pathToPrint':
                global pathToPrint
                pathToPrint = data[1].strip()
            elif data[0].strip() == 'Debug':
                if data[1].lower().strip() == 'true':
                    global Debug
                    Debug = True
                else:
                    Debug = False
            elif data[0].strip() == 'pathToSizeFile':
                global pathToSizeFile
                pathToSizeFile = data[1].strip()
            elif data[0].strip() == 'listSize':
                global listSize
                listSize = [i.strip() for i in data[1].split(',')]
            elif data[0].strip() == 'tableSize':
                global tableSize
                tableSize = data[1].strip().split(',')
            elif data[0].strip() == 'startPoint':
                global startPoint
                startPoint = [i.strip() for i in data[1].strip().split(';')]
                startPoint
            elif data[0].strip() == 'XDelta':
                global XDelta
                XDelta = data[1].strip()
            elif data[0].strip() == 'YDelta':
                global YDelta
                YDelta = data[1].strip()
            elif data[0].strip() == 'pathToBug':
                global pathToBug
                pathToBug = data[1].strip()


def startChek():
    """Начальная проверка на наличие нужных каталогов"""
    errorsDirFlag = False
    errorsSizeFlag = False
    dirList = [mainPath, pathToExcelWithSize,
               pathToPrint, pathToTables, pathToConfig, pathDebug, pathToSizeFile]
    if Debug:
        print('ВНИМАНИЕ, ВКЛЮЧЁН РЕЖИМ ОТЛАДКИ')
    for dir_ in dirList:
        if not file_exists(dir_):
            if input('Ошибка при инициализации программы. Директория или файл необходимый для корректной работы "{}" не сущуствует. Создать? Да/Нет: '.format(dir_)).lower() == 'да':

                makedirs(dir_)
            else:
                errorsDirFlag = True
                continue
    if errorsDirFlag:
        input('ВНИМАНИЕ, ПРИ НАЧАЛЬНОЙ ПРОВЕРКЕ БЫЛИ ОБНАРУЖЕНЫ ОШИБКИ В ДИРЕКТОРИЯХ ИЛИ ПУТЯХ К ФАЙЛАМ ПРОГРАММЫ. ПРОГРАММА МОЖЕТ РАБОТАТЬ НЕПРАВИЛЬНО!')
    with open(pathToSizeFile, 'r') as file:
        data = file.readlines()
        if len(data) != len(listSize):
            errorsSizeFlag = True
            input('ВНИМАНИЕ, В ФАЙЛЕ КОЛИЧЕСТВО РАЗМЕРОВ В ФАЙЛЕ РАЗМЕРОВ "{}" НЕ СОВПАДАЕТ С КОЛИЧЕСТВОМ РАЗМЕРОВ В ФАЙЛЕ КОНФИГУРАЦИИ "{}", ПРОВЕРЬТЕ ОБА ФАЙЛА!'.format(
                pathToSizeFile, pathToConfig))
        for sizeApp in listSize:
            for sizeConf in data:
                if sizeApp.lower() == sizeConf.split('=')[0].strip().lower():
                    sizeName = sizeApp
                    sizePath = sizeConf.split('=')[1].strip()
                    global dataWithSizePath
                    dataWithSizePath.update({sizeName: sizePath})
        if len(dataWithSizePath) != len(sizeApp) and len(dataWithSizePath) != len(listSize):
            errorsSizeFlag = True
            input('ВНИМАНИЕ, КАКОЙ_ТО РАЗМЕР НЕ СОВПАЛ ПО НАЗВАНИЮ В ФАЙЛЕ РАЗМЕРОВ "{}" И В ФАЙЛЕ КОНФИГУРАЦИИ "{}", ПРОВЕРЬТЕ ОБА ФАЙЛА!'.format(
                pathToSizeFile, pathToConfig))
    return errorsDirFlag*errorsSizeFlag


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
    if Debug:
        with open(joinpath(pathDebug, 'getDataFromOrderFile-dataFromOrderFile.txt'), 'w', encoding='utf-8') as file:
            for line in dataFromOrderFile:
                file.write(str(line))
                file.write('\n')
            file.close()
            input('Debug-файл getDataFromOrderFile-dataFromOrderFile.txt Сохранён')
    return dataFromOrderFile


def detectPtintFronName(name):
    if Debug:
        with open(joinpath(pathDebug, 'detectPtintFronName.txt'), 'a', encoding='utf-8') as file:
            if 'прозрачный' in name.lower():
                file.writelines(name.lower().split('прозрачный')[1])
                file.close()
                return name.lower().split('прозрачный')[1].strip()
            elif 'матовый' in name.lower():
                file.writelines(name.lower().split('матовый')[1])
                file.close()
                return name.lower().split('матовый')[1].strip()
            elif 'блестки' in name.lower():
                file.writelines(name.lower().split('блестки')[1])
                file.close()
                return name.lower().split('блестки')[1].strip()
            elif 'skinshell' in name.lower():
                file.writelines(name.lower().split('skinshell')[1])
                file.close()
                return name.lower().split('skinshell')[1].strip()
            elif 'fashion' in name.lower():
                file.writelines(name.lower().split('fashion')[1])
                file.close()
                return name.lower().split('fashion')[1].strip()
            elif 'df' in name.lower():
                file.writelines(name.lower().split('df')[1])
                file.close()
                return name.lower().split('df')[1].strip()

    else:
        if 'прозрачный' in name.lower():
            return name.lower().split('прозрачный')[1].strip()
        elif 'матовый' in name.lower():
            return name.lower().split('матовый')[1].strip()
        elif 'блестки' in name.lower():
            return name.lower().split('блестки')[1].strip()
        elif 'skinshell' in name.lower():
            return name.lower().split('skinshell')[1].strip()
        elif 'fashion' in name.lower():
            return name.lower().split('fashion')[1].strip()
        elif 'df' in name.lower():
            return name.lower().split('df')[1].strip()


def detectSizeFromOrder(orderSize, orderNum, table):
    if orderSize.lower() == 'книга':
        return 'Книга'
    for size in listSize:
        if size.lower().strip() == orderSize.lower().strip():
            return size
    input('В файле обнаружен размер "{}", которого нет в списке размеров. Макеты могут быть не полные. Номер стола {}, номер задания {}.'.format(orderSize,
                                                                                                                                                 table, orderNum))
    return None


def createpathToFile(printNameAll, size):
    if '(' in printNameAll and ')' in printNameAll:
        printName = printNameAll.split('(')[1].split(')')[0]
    elif '(' in printNameAll and ')' not in printNameAll:
        printName = printNameAll.split('(')[1]
    printFileName = printName.replace('принт', 'print') + '.cdr'
    pathToFolder = dataWithSizePath[size]
    return joinpath(pathToFolder, printFileName)


def splitOrderTable(dataFromOrderFile):
    numTable = 1
    count = 0
    nameTable = 'Table_{}'
    data = []
    if dataFromOrderFile != None:
        for line in dataFromOrderFile:
            if line['Номер задания'] == '':
                with open(joinpath(pathToTables, nameTable.format(str(numTable))) + '.txt', 'w', encoding='ANSI') as file:
                    file.write('\n'.join(data))
                    file.close()
                data = []
                numTable += 1
                count = 0
                continue
            X, Y = makeLocPrint(count)
            count += 1
            printName = detectPtintFronName(line['Название'])
            size = detectSizeFromOrder(str(line['Размер'])[0:-2] if type(
                line['Размер']) == float else line['Размер'], line['Номер задания'], str(numTable))
            if size != None:
                pathToFile = createpathToFile(printName, size)
            else:
                pathToFile = pathToBug
            data.append(';'.join([
                line['Номер задания'], pathToFile, X.replace('.', ','), Y.replace('.', ',')]))
            with open(joinpath(pathToTables, nameTable.format(str(numTable))) + '.txt', 'w', encoding='ANSI') as file:
                file.write('\n'.join(data))
                file.close()


def makeLocPrint(count):
    YLocation = str(round(float(
        startPoint[1]) + float(YDelta) * float(count//11), 3))
    Xlocation = str(round(float(startPoint[0]) +
                          float(XDelta) * (10 + count//11 * 11 - count), 3))
    return (Xlocation, YLocation)


try:
    applyConfig()
except:
    input('Произошла непредвиденная ошибка при инициализации')
try:
    startChek()
except:
    input('Произошла непредвиденная ошибка при первоначальной проверке')
try:
    dataFromOrderFile = getDataFromOrderFile(pathToOrderFile)
except:
    input('Произошла непредвиденная ошибка при получении информации из файла заказа {}'.format(
        pathToOrderFile))
# try:
splitOrderTable(dataFromOrderFile)
# except:
# input('Произошла непредвиденная ошибка при работе программы')
