import sys
import xlrd
from os.path import join as joinpath , exists
from os import listdir, remove, makedirs
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication
from ui.ui_printHelperUI import Ui_PrintHelper
# pyuic5 D:\Rep\Python\archive\PrintHelper\ui\printHelperUI.ui -o D:\Rep\Python\archive\PrintHelper\ui\printHelperUI.py
pathToOrderFile = ''
mode = ''
w = QtWidgets.QWidget
class FBSStoks(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(FBSStoks, self).__init__(parent)
        self.ui = Ui_PrintHelper()
        self.ui.setupUi(self)
        self.ui.selectFileButt.clicked.connect(self.selectFile)
        self.ui.bigButt.clicked.connect(self.bigMode)
        #self.ui.medButt.clicked.connect(self.medMode)
        self.ui.smallButt.clicked.connect(self.smallMode)
        #self.ui.bigButt.clicked.connect(self.smallMode)
        self.ui.smallButtBooks.clicked.connect(self.smallBookMode)
        #self.ui.medButtBooks.clicked.connect(self.medBookMode)
        self.ui.smallButtPlastins.clicked.connect(self.smallPlastinMode)
        self.ui.smallButtCartholders.clicked.connect(self.smallCartholderMode)

    def saveModePrinter(self, printer):
        with open(pathToPrinterMode, 'w') as file:
            if printer == 'bigMode':
                file.write('1')
            else:
                file.write('0')


    def bigMode(self):
        global mode
        mode = 'bigMode'
        self.saveModePrinter(mode)
        w.close(self)


    def smallCartholderMode(self):
        global mode
        mode = 'smallCartholderMode'
        self.saveModePrinter(mode)
        w.close(self)
    

    def medMode(self):
        global mode
        mode = 'medMode'
        self.saveModePrinter(mode)
        w.close(self)

    def smallMode(self):
        global mode
        mode = 'smallMode'
        self.saveModePrinter(mode)
        w.close(self)

    def smallBookMode(self):
        global mode
        mode = 'smallBookMode'
        self.saveModePrinter(mode)
        w.close(self)


    def medBookMode(self):
        global mode
        mode = 'medBookMode'
        self.saveModePrinter(mode)
        w.close(self)
    

    def smallPlastinMode(self):
        global mode
        mode = 'smallPlastinMode'
        self.saveModePrinter(mode)
        w.close(self)


    def selectFile(self):
        global pathToOrderFile
        pathToOrderFile = QFileDialog.getOpenFileName(self, ("Выберите файл со списком номенклатуры"), "", ("Excel Files (*.xlsx)"))[0]
        if pathToOrderFile == '':
            self.createMSGError("Вы не выбрали файл номенклатурой для загрузки.")
            return 0

    def createMSGError(self,text):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setText(text)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.exec_()





# pathToOrderFile = r'F:\15_4775_планки от 14.08.2022.xlsx'
# pathToOrderFile = r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\Новые\ФБС принты потерянные 06.11.2021.xlsx'
mainPath = r'C:\Users\Public\Documents\WBHelpTools\PrintHelper'
pathToPrint = r'\\192.168.0.111\shared\Отдел производство\макеты для принтера\Макеты для 6090'
pathToSizeFile = r'C:\Users\Public\Documents\WBHelpTools\PrintHelper\size.txt'
pathToBug = r'\\192.168.0.111\shared\Отдел производство\макеты для принтера\Макеты для 6090\Bug\print 0.cdr'
pathToModeFile = r"C:\Users\Public\Documents\WBHelpTools\PrintHelper\mode.txt"


Debug = False


pathToTables = joinpath(mainPath, 'Tables')
pathToFileConfigSmall = joinpath(mainPath, 'configSmall.txt')
pathToFileConfigMed = joinpath(mainPath, 'configMed.txt')
pathToFileConfigBig = joinpath(mainPath, 'configBig.txt')
pathToFileConfigPlanks  = joinpath(mainPath, 'configPlank.txt')
pathToFileConfigSmallBook = joinpath(mainPath, 'configSmallBook.txt')
pathToFileConfigMedBook = joinpath(mainPath, 'configMedBook.txt')
pathToFileConfigCartholder = joinpath(mainPath, 'configCartholder.txt')

pathDebug = joinpath(mainPath, 'debug')
pathToPrinterMode= joinpath(mainPath, 'printerMode.txt')
pathToAlgleDeltaLeft= joinpath(mainPath, 'algleDeltaLeft.txt')
pathToAlgleDeltaRight= joinpath(mainPath, 'algleDeltaRight.txt')
listSize = ['13', '13 min', '13 pm', 'L', 'M', 'MS', 'S', 'XL', 'XS', 'Книга']
dataWithSizePath = {}
tableSize = ['925', '535']
startPoint = ['47.569', '92.508']
XDelta = '83'
YDelta = '175'
countCaseInTable = '11'
anlgeStartPointDelta = ['877.431', '92.508']


def file_exists(file_name):
    '''Функция возвращает True если файл по пути file_name существует и False если не существует'''

    return(exists(file_name))

def applyConfig(mode):
    if mode == 'smallMode':
        pathToConfig = pathToFileConfigSmall
        with open(pathToModeFile, 'w') as fileMode:
            fileMode.write('sil')
            fileMode.close()
    elif mode == 'smallCartholderMode':
        pathToConfig = pathToFileConfigCartholder
        with open(pathToModeFile, 'w') as fileMode:
            fileMode.write('cartholder')
            fileMode.close() 
    elif mode == 'medMode':
        pathToConfig = pathToFileConfigMed
        with open(pathToModeFile, 'w') as fileMode:
            fileMode.write('sil')
            fileMode.close() 
    elif mode == 'bigMode':
        pathToConfig = pathToFileConfigBig
        with open(pathToModeFile, 'w') as fileMode:
            fileMode.write('sil')
            fileMode.close()         
    elif mode =='smallPlastinMode':
        pathToConfig = pathToFileConfigPlanks
        with open(pathToModeFile, 'w') as fileMode:
            fileMode.write('plastin')
            fileMode.close()
    elif mode == 'smallBookMode':
        pathToConfig = pathToFileConfigSmallBook
        with open(pathToModeFile, 'w') as fileMode:
            fileMode.write('book')
            fileMode.close()
    elif mode == 'medBookMode':
        pathToConfig = pathToFileConfigMedBook
        with open(pathToModeFile, 'w') as fileMode:
            fileMode.write('book')
            fileMode.close()
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
                startPoint = [i.strip() for i in data[1].strip().split(',')]
                # startPoint
            elif data[0].strip() == 'XDelta':
                global XDelta
                XDelta = data[1].strip()
            elif data[0].strip() == 'YDelta':
                global YDelta
                YDelta = data[1].strip()
            elif data[0].strip() == 'pathToBug':
                global pathToBug
                pathToBug = data[1].strip()
            elif data[0].strip() == 'countCaseInTable':
                global countCaseInTable
                countCaseInTable = data[1].strip()
            elif data[0].strip() == 'anlgeStartPointDelta':
                global anlgeStartPointDelta
                anlgeStartPointDelta = [i.strip() for i in data[1].strip().split(',')]


def startChek(mode):
    """Начальная проверка на наличие нужных каталогов"""
    if mode == 'smallMode':
        pathToConfig = pathToFileConfigSmall
    elif mode == 'smallCartholderMode':
        pathToConfig = pathToFileConfigCartholder
    elif mode == 'medMode':
        pathToConfig = pathToFileConfigMed
    elif mode == 'bigMode':
        pathToConfig = pathToFileConfigBig
    elif mode =='smallPlastinMode':
        pathToConfig = pathToFileConfigPlanks
    elif mode =='medBookMode':
        pathToConfig = pathToFileConfigMedBook
    elif mode == 'smallBookMode':
        pathToConfig = pathToFileConfigSmallBook
    errorsDirFlag = False
    errorsSizeFlag = False
    dirList = [mainPath,pathToPrint, pathToTables, pathToConfig, pathDebug, pathToSizeFile]
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
        for file in listdir(pathToTables):
            remove(joinpath(pathToTables, file))
    return errorsDirFlag*errorsSizeFlag


def read_xlsx(file_path, nameList):
    '''Считывает построчно xlsx файл и возращает список словарей - если title = 'Yes', список списков - если title = 'No'
    '''
    rd = xlrd.open_workbook(file_path)
    try:
        sheet = rd.sheet_by_name(nameList)
    except:
        sheet = rd.sheet_by_index(0)
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
    # print(pathToOrderFile)
    dataFromOrderFile = read_xlsx(pathToOrderFile, 'Столы')
    if Debug:
        with open(joinpath(pathDebug, 'getDataFromOrderFile-dataFromOrderFile.txt'), 'w', encoding='utf-8') as file:
            for line in dataFromOrderFile:
                file.write(str(line))
                file.write('\n')
            file.close()
            input('Debug-файл getDataFromOrderFile-dataFromOrderFile.txt Сохранён')
    return dataFromOrderFile


def detectPtintFronName(name, mode):
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
        elif 'пластина' in name.lower():
            return name.lower().split('прямоугольная черная')[1].strip()
        elif 'пластина' in name.lower():
            return name.lower().split('прямоугольная черная')[1].strip()
        else:
            # a = '(Принт' + name.lower().split(' (принт')[1].strip()
            # print(a)
            return '(принт ' + name.lower().split(' (принт')[1].strip()


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
    printFileName = printName.replace('принт', 'print') + '.pdf'
    pathToFolder = dataWithSizePath[size]
    fullPath = joinpath(pathToFolder, printFileName)
    if not file_exists(fullPath):
        printFileName = printFileName.replace('.pdf', '.cdr')
        fullPath = joinpath(pathToFolder, printFileName)
    if not file_exists(fullPath):
        fullPath = pathToBug
    return fullPath


def splitOrderTable(dataFromOrderFile, mode):
    numTable = 1
    count = 0
    nameTable = 'Table_{}'
    data = []
    if dataFromOrderFile != None:
        for line in dataFromOrderFile:
            orderNum = line['Номер задания']
            orderNum = orderNum if type(
                orderNum) == str else str(orderNum)[0:-2]
            if orderNum == '' and line['Размер'] == '':
                with open(joinpath(pathToTables, nameTable.format(str(numTable))) + '.txt', 'w', encoding='ANSI') as file:
                    file.write('\n'.join(data))
                    file.close()
                data = []
                numTable += 1
                count = 0
                continue
            X, Y = makeLocPrint(count)
            count += 1
            if line['Название'] !='':
                printName = detectPtintFronName(line['Название'], mode)
                size = detectSizeFromOrder(str(line['Размер'])[0:-2] if type(
                    line['Размер']) == float else line['Размер'], orderNum, str(numTable))
                if size != None:
                    pathToFile = createpathToFile(printName, size)
                else:
                    pathToFile = pathToBug
                data.append(';'.join([
                    orderNum, pathToFile, X.replace('.', ','), Y.replace('.', ','), line['Название']]))
                with open(joinpath(pathToTables, nameTable.format(str(numTable))) + '.txt', 'w', encoding='ANSI') as file:
                    file.write('\n'.join(data))
                    file.close()


def makeLocPrint(count):
    YLocation = str(round(float(
        startPoint[1]) + float(YDelta) * float(count//int(countCaseInTable)), 3))
    Xlocation = str(round(float(startPoint[0]) +
                          float(XDelta) * (int(countCaseInTable)-1 + count//int(countCaseInTable) * int(countCaseInTable) - count), 3))
    return (Xlocation, YLocation)


def createStartAngleDeltaFile():
    xDeltaAngle = float(startPoint[0]) + float(anlgeStartPointDelta[0])
    yDeltaAngle =  float(startPoint[1]) - float(anlgeStartPointDelta[1])
    open(pathToAlgleDeltaRight, 'w').write(','.join([str(xDeltaAngle), str(yDeltaAngle)]))
    open(pathToAlgleDeltaLeft, 'w').write(','.join([str(xDeltaAngle - float(tableSize[0])), str(yDeltaAngle)]))

def startPrintHelper():
    # while True:
    #     mode = input('Для какого принтера макет? Введите если маленький  "1", если средний - "2", если планки - "3" (По умолчанию "1"): ')
    #     if mode == '1':
    #         break
    #     elif mode == '2':
    #         break
    #     elif mode == '3':
    #         break
    #     elif mode == '':
    #         mode = '1'
    #         break
    #     else:
    #         print('Некорректный ввод!')
    #         continue
    try:
        applyConfig(mode)
    except:
        input('Произошла непредвиденная ошибка при инициализации')
    try:
        startChek(mode)
        createStartAngleDeltaFile()
    except:
        input('Произошла непредвиденная ошибка при первоначальной проверке')
    try:
        dataFromOrderFile = getDataFromOrderFile(pathToOrderFile)
    except:
        input('Произошла непредвиденная ошибка при получении информации из файла заказа {}'.format(
            pathToOrderFile))
    try:
        splitOrderTable(dataFromOrderFile, mode)
    except:
        input('Произошла непредвиденная ошибка при работе программы')


if __name__ =='__main__':
    app = QtWidgets.QApplication([])
    application = FBSStoks()
    application.show()
    app.exec()
    startPrintHelper()