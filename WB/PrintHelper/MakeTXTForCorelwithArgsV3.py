from pandas import DataFrame, read_excel
from os.path import join as joinpath , exists, basename
from os import makedirs
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QFileDialog, QMessageBox
# from ui.chekUI import chekUIVesion, pathTouiVesionFile
# if (uiVersion:=chekUIVesion()) == '1.0':
#     from ui.ui_printHelperUI import Ui_PrintHelper
# else:
from ui.ui_printHelperUIV3 import Ui_PrintHelper
import pickle
import psutil
import warnings


pathToOrderFile = ''
mode = ''
listSize = ''
class PrintHelper(QtWidgets.QMainWindow):
    printSettMainFilePath = r'C:\Users\Public\Documents\WBHelpTools\PrintHelper\printSetMain.pkl'
    dataDefault = {
        'bigButtInt': {'bigAcsButt': True},
        'medButtInt': {'medAcsButt': True},
        'smallButtInt': {'smallAcsButt': True},
        'bigButt': {'bigSilAcsButt': True},
        'medButt': {'medSilAcsButt': True},
        'smallButt': {'smallSilAcsButt': True},
        'medButtBooks': {'medBkAcsButt': True},
        'smallButtBooks': {'smallBkAcsButt': True},
        'smallButtPlastins': {'smallPlAcsButt': True},
        'smallButtCartholders': {'sallHldAcsButt': True}
    }
    chekKeys = ['bigButtInt', 'medButtInt', 'smallButtInt', 'bigButt', 'medButt', 'smallButt', 'medButtBooks', 'smallButtBooks', 'smallButtPlastins', 'smallButtCartholders']
    def __init__(self,parent=None):
        super(PrintHelper, self).__init__(parent)
        self.ui = Ui_PrintHelper()
        self.ui.setupUi(self)
        self.ui.selectFileButt.clicked.connect(self.selectFile)
        self.ui.bigButt.clicked.connect(self.bigMode)
        self.ui.medButt.clicked.connect(self.medMode)
        self.ui.medButtBooks.clicked.connect(self.medBookMode)
        self.ui.smallButt.clicked.connect(self.smallMode)
        self.ui.smallButtBooks.clicked.connect(self.smallBookMode)
        self.ui.smallButtPlastins.clicked.connect(self.smallPlastinMode)
        self.ui.smallButtCartholders.clicked.connect(self.smallCartholderMode)
        self.ui.addSizeButt.clicked.connect(self.addSizeButt)
        self.ui.medButtBooks.setEnabled(False)
        self.ui.medButt.setEnabled(False)
        self.ui.smallButt.setEnabled(False)
        self.ui.smallButtBooks.setEnabled(False)
        self.ui.smallButtPlastins.setEnabled(False)
        self.ui.bigButt.setEnabled(False)
        self.ui.smallButtCartholders.setEnabled(False)
        self.readSett()
        # Элементы нового интерфейса
        # if uiVersion != '1.0':
        #     self.setIcon()
        #     self.updateUiSett()
        #     self.mainPageButt()
        #     self.ui.bigButtInt.clicked.connect(self.bigButtInt)
        #     self.ui.medButtInt.clicked.connect(self.medButtInt)
        #     self.ui.smallButtInt.clicked.connect(self.smallButtInt)
        #     self.ui.mainPageButt.clicked.connect(self.mainPageButt)
        #     self.ui.frameSettings.setVisible(False)
        #     self.ui.settButt.clicked.connect(self.showSett)
        #     self.ui.applySettButt.clicked.connect(self.applySett)
        #     self.ui.lineEditPass.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password) 
        self.setIcon()
        self.updateUiSett()
        self.mainPageButt()
        self.ui.bigButtInt.clicked.connect(self.bigButtInt)
        self.ui.medButtInt.clicked.connect(self.medButtInt)
        self.ui.smallButtInt.clicked.connect(self.smallButtInt)
        self.ui.mainPageButt.clicked.connect(self.mainPageButt)
        self.ui.frameSettings.setVisible(False)
        self.ui.frameSettings2.setVisible(False)
        self.ui.lineEditPass.returnPressed.connect(self.showSett)
        self.ui.settButt.clicked.connect(self.showSett)
        self.ui.applySettButt.clicked.connect(self.applySett)
        self.ui.lineEditPass.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password) 
        self.minMem = 5
        self.dataWithSizePath = {}
        self.loadsSizeFromConfig()
        # self.ui.oldNewButt.clicked.connect(self.oldNewButt)
        # if uiVersion == '1.0':
        #     self.ui.oldNewButt.setText('Переключить на новый интерфейс')
        
    def chekMem(self):
        avalMemGB = dict(psutil.virtual_memory()._asdict())['available']/1024/1024/1024
        if avalMemGB < self.minMem:
            QMessageBox.warning(self, 'Мало памяти', f'Внимание! На компьютере осталось менее {self.minMem} Гб совбодной оперативной памяти. Закройте вкладки с большими макетами в Corel иначе работа программы может быть некорректной.')


    def saveFileName(self, pathToOrderFile):
        fileToSave = r'C:\Users\Public\Documents\WBHelpTools\PrintHelper\name.txt'
        with open(fileToSave, 'w', encoding='ANSI') as file:
            file.write(basename(pathToOrderFile))
            file.close()


    def loadsSizeFromConfig(self):
        with open(r"\\192.168.0.111\shared\Отдел производство\обновления программы печати\sizesV3.pkl", 'rb') as file:
            self.dataWithSizePath = pickle.load(file)
        global dataWithSizePath
        dataWithSizePath = self.dataWithSizePath


    def addSizeButt(self):
        nameSize1C = self.ui.lineEditNameSize1C
        nemeFileSize = self.ui.lineEditNameFileSize
        pass

            


    def applySett(self):
        self.data = {
            'bigButtInt': {'bigAcsButt': self.ui.bigAcsButt.isChecked()},
            'medButtInt': {'medAcsButt': self.ui.medAcsButt.isChecked()},
            'smallButtInt': {'smallAcsButt': self.ui.smallAcsButt.isChecked()},
            'bigButt': {'bigSilAcsButt': self.ui.bigSilAcsButt.isChecked()},
            'medButt': {'medSilAcsButt': self.ui.medSilAcsButt.isChecked()},
            'smallButt': {'smallSilAcsButt': self.ui.smallSilAcsButt.isChecked()},
            'medButtBooks': {'medBkAcsButt': self.ui.medBkAcsButt.isChecked()},
            'smallButtBooks': {'smallBkAcsButt': self.ui.smallBkAcsButt.isChecked()},
            'smallButtPlastins': {'smallPlAcsButt': self.ui.smallPlAcsButt.isChecked()},
            'smallButtCartholders': {'sallHldAcsButt': self.ui.sallHldAcsButt.isChecked()}
        }
        self.updateUiSett()
        self.saveSett()
        self.ui.frameMain.setVisible(True)
        self.ui.mainPageButt.setVisible(True)
        self.ui.frameSettings.setVisible(False)
        self.ui.settButt.setVisible(True)
        self.ui.label_2.setVisible(True)
        self.ui.lineEditPass.setVisible(True)
        self.mainPageButt()


    def saveSett(self):
        with open(self.printSettMainFilePath, 'wb') as file:
            pickle.dump(self.data, file)
            file.close()
        # self.updateUiSett()


    def updateUiSett(self):
        try:
            for name, chekDict in self.data.items():
                butt = self.findChild(QtWidgets.QPushButton, name)
                chek = self.findChild(QtWidgets.QCheckBox, list(chekDict.keys())[0])
                if pathToOrderFile:
                    butt.setEnabled(list(chekDict.values())[0])
                chek.setChecked(list(chekDict.values())[0])
        except:
            QMessageBox.warning(self, 'Ошибка', 'Файл конфигурации повреждён, применены настройки по умолчанию!')
            self.data = self.dataDefault
            self.saveSett()



    def readSett(self):
        with open(self.printSettMainFilePath, 'rb') as file:
                dataTMP = pickle.load(file)
                file.close()
        self.chekSett(dataTMP)
        # self.updateChelSett()
        # self.updateUiSett()

    def chekSett(self, data):
        for key in self.chekKeys:
            try:
                if key not in data.keys():
                    QMessageBox.warning(self, 'Ошибка', 'Файл конфигурации повреждён, применены настройки по умолчанию!')
                    self.saveSett()
                    return 0
            except:
                QMessageBox.warning(self, 'Ошибка', 'Файл конфигурации повреждён, применены настройки по умолчанию!')
                self.saveSett()
                return 0
        self.data = data          


    def showSett(self):
        if self.ui.lineEditPass.text()  == '565656':
            self.mainPageButt()
            self.ui.frameMain.setVisible(False)
            self.ui.mainPageButt.setVisible(False)
            self.ui.frameSettings.setVisible(True)
            self.ui.settButt.setVisible(False)
            self.ui.label_2.setVisible(False)
            self.ui.lineEditPass.setVisible(False)
            self.ui.lineEditPass.setText('') 
        else:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Неверный пароль!')
        


    def setIcon(self):
        icon = QtGui.QIcon()
        a = joinpath(r'C:\Users\Public\Documents\WBHelpTools\PrintHelper\ui\image',r'bigButtInt.gif')
        icon.addPixmap(QtGui.QPixmap(a), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.ui.bigButtInt.setIcon(icon)
        self.ui.bigButtInt.setIconSize(QtCore.QSize(236, 130))
        self.ui.bigButtInt.setShortcut("")
        self.ui.bigButtInt.setObjectName("bigButtInt")
        a = joinpath(r'C:\Users\Public\Documents\WBHelpTools\PrintHelper\ui\image', r'medButtInt.gif')
        icon.addPixmap(QtGui.QPixmap(a), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.ui.medButtInt.setIcon(icon)
        self.ui.medButtInt.setIconSize(QtCore.QSize(119, 200))
        self.ui.medButtInt.setShortcut("")
        self.ui.medButtInt.setObjectName("medButtInt")
        a = joinpath(r'C:\Users\Public\Documents\WBHelpTools\PrintHelper\ui\image',r'smallButtInt.gif')
        icon.addPixmap(QtGui.QPixmap(a), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.ui.smallButtInt.setIcon(icon)
        self.ui.smallButtInt.setIconSize(QtCore.QSize(112, 200))
        self.ui.smallButtInt.setShortcut("")
        self.ui.smallButtInt.setObjectName("smallButtInt")

    def mainPageButt(self):
        self.ui.label_2.setText('Выберите станок')
        self.ui.frameBig.setVisible(False)
        self.ui.frameMed.setVisible(False)
        self.ui.frameSmall.setVisible(False)
        # self.ui.frameOther.setVisible(False)
        self.ui.frameMain.setVisible(True)

    def smallButtInt(self):
        self.ui.label_2.setText('Выберите программу для запуска на маленьком принтере')
        self.ui.frameSmall.setVisible(True)
        self.ui.frameMain.setVisible(False)

    def medButtInt(self):
        self.ui.label_2.setText('Выберите программу для запуска на среднем принтере')
        self.ui.frameMed.setVisible(True)
        self.ui.frameMain.setVisible(False)

    def bigButtInt(self):
        self.ui.label_2.setText('Выберите программу для запуска на большом принтере')
        self.ui.frameBig.setVisible(True)
        self.ui.frameMain.setVisible(False)

    # def oldNewButt(self):
    #     uiVersion = chekUIVesion()
    #     with open(pathTouiVesionFile, 'w') as f:
    #         if uiVersion == '1.0':
    #             f.write('2.0')
    #             self.ui.oldNewButt.setText('Вернуть старый интерфейс')
    #         else:
    #             f.write('1.0')
    #             self.ui.oldNewButt.setText('Переключить на новый интерфейс')
    #         f.close()
    #     # Показать предупреждение с текстом "готово"
    #     QMessageBox.information(self, 'Интерфейс', 'Перезапустите программу для применения')
        


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
        PrintHelper.close(self)


    def smallCartholderMode(self):
        global mode
        mode = 'smallCartholderMode'
        self.saveModePrinter(mode)
        PrintHelper.close(self)
    

    def medMode(self):
        global mode
        mode = 'medMode'
        self.saveModePrinter(mode)
        PrintHelper.close(self)

    def smallMode(self):
        global mode
        mode = 'smallMode'
        self.saveModePrinter(mode)
        PrintHelper.close(self)

    def smallBookMode(self):
        global mode
        mode = 'smallBookMode'
        self.saveModePrinter(mode)
        PrintHelper.close(self)


    def medBookMode(self):
        global mode
        mode = 'medBookMode'
        self.saveModePrinter(mode)
        PrintHelper.close(self)


    def medBookMode(self):
        global mode
        mode = 'medBookMode'
        self.saveModePrinter(mode)
        PrintHelper.close(self)
    

    def smallPlastinMode(self):
        global mode
        mode = 'smallPlastinMode'
        self.saveModePrinter(mode)
        PrintHelper.close(self)


    def selectFile(self):
        self.chekMem()
        global pathToOrderFile
        pathToOrderFile = QFileDialog.getOpenFileName(self, ("Выберите файл со списком номенклатуры"), r"\\192.168.0.111\shared\Отдел производство\Wildberries\Заказы принты\Заказы Эксель", ("Excel Files (*.xlsx)"))[0]
        if pathToOrderFile == '':
            self.createMSGError("Вы не выбрали файл номенклатурой для загрузки.")
            return 0
        self.ui.selectFileButt.setText(basename(pathToOrderFile))
        self.ui.selectFileButt.setStyleSheet("font-size:11px; font-weight: bold")
        self.ui.medButtBooks.setEnabled(True)
        self.ui.medButt.setEnabled(True)
        self.ui.smallButt.setEnabled(True)
        self.ui.smallButtBooks.setEnabled(True)
        self.ui.smallButtPlastins.setEnabled(True)
        self.ui.bigButt.setEnabled(True)
        self.ui.smallButtCartholders.setEnabled(True)
        self.updateUiSett()
        self.mainPageButt()
        self.saveFileName(pathToOrderFile)
        # self.applySett()

    def createMSGError(self,text):
        QMessageBox.warning(self, 'Ошибка', text)
        #msg.setIcon(QtWidgets.QMessageBox.Warning)
        #msg.exec_()

    
    





# pathToOrderFile = r'F:\15_4775_планки от 14.08.2022.xlsx'
# pathToOrderFile = r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\Новые\ФБС принты потерянные 06.11.2021.xlsx'
mainPath = r'C:\Users\Public\Documents\WBHelpTools\PrintHelper'
pathToPrint = r'\\192.168.0.111\shared\Отдел производство\макеты для принтера\Макеты для 6090'
pathToSizeFile = r'C:\Users\Public\Documents\WBHelpTools\PrintHelper\size.txt'
pathToSizeFileV2 = r'C:\Users\Public\Documents\WBHelpTools\PrintHelper\sizeV2.txt'
pathToBug = r'\\192.168.0.111\shared\Отдел производство\макеты для принтера\Макеты для 6090\Bug\print 0.cdr'
pathToModeFile = r"C:\Users\Public\Documents\WBHelpTools\PrintHelper\mode.txt"
pathToSizeDir = r'\\192.168.0.111\shared\Отдел производство\макеты для принтера\Макеты для 6090\Размеры принтов'
pathToFolderPrint = r'\\192.168.0.111\shared\Отдел производство\макеты для принтера\Макеты для 6090\Оригиналы'


Debug = False


pathToTables = joinpath(mainPath, 'Tables')
pathToTablesV2 = joinpath(mainPath, 'TablesV2')
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
# listSize = ['13', '13 min', '13 pm', 'L', 'M', 'MS', 'S', 'XL', 'XS', 'Книга']
# dataWithSizePath = {}
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
            # elif data[0].strip() == 'pathToSizeFileV2':
            #     global pathToSizeFileV2
            #     pathToSizeFileV2 = data[1].strip()
            # elif data[0].strip() == 'listSize':
            #     global listSize
            #     listSize = []
            #     listSize = [i.strip() for i in data[1].split(',')]
                #A = data[1].split(',')
                # for i in data[1].split(','):
                #     listSize.append(i.strip())

                # listSize
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
    dirList = [mainPath,pathToPrint, pathToTablesV2, pathToConfig, pathDebug, pathToSizeFileV2]
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
    return errorsDirFlag*errorsSizeFlag


def read_xlsx(file_path, nameList):
    '''Считывает построчно xlsx файл и возращает список словарей - если title = 'Yes', список списков - если title = 'No'
    '''
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl', message='Cannot parse header or footer so it will be ignored')
    tmp = DataFrame(read_excel(file_path)).fillna('').to_dict('records')
    # tmp = tmp
    # rd = xlrd.open_workbook(file_path)
    # # try:
    # #     sheet = rd.sheet_by_name(nameList)
    # # except:
    # #     sheet = rd.sheet_by_index(0)
    # sheet = rd.sheet_by_index(0)
    # try:
    #     Name_row = sheet.row_values(0)
    # except IndexError:
    #     return None
    # start = 1
    # data = []
    # for rownum in range(start, sheet.nrows):
    #     row = sheet.row_values(rownum)
    #     dct = {}
    #     for i, cel in enumerate(row):
    #         tmp = {Name_row[i]: cel}
    #         dct.update(tmp)
    #     data.append(dct)
    return tmp


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
    for size in list(dataWithSizePath.keys()):
        if size.lower().strip() == orderSize.lower().strip():
            return size
    input('В файле обнаружен размер "{}", которого нет в списке размеров. Макеты могут быть не полные. Номер стола {}, номер задания {}.'.format(orderSize,
                                                                                                                                                 table, orderNum))
    return None


def createpathToFile(printNameAll):
    if '(' in printNameAll and ')' in printNameAll:
        printName = printNameAll.split('(')[1].split(')')[0]
    elif '(' in printNameAll and ')' not in printNameAll:
        printName = printNameAll.split('(')[1]
    printFileName = printName.replace('принт', 'print') + '.pdf'
    # pathToFolder = dataWithSizePath[size]
    fullPath = joinpath(pathToFolderPrint, printFileName)
    if not file_exists(fullPath):
        fullPath = pathToBug
    return fullPath


def createpathToSize(size):
    # if '(' in printNameAll and ')' in printNameAll:
    #     printName = printNameAll.split('(')[1].split(')')[0]
    # elif '(' in printNameAll and ')' not in printNameAll:
    #     printName = printNameAll.split('(')[1]
    # printFileName = printName.replace('принт', 'print') + '.pdf'
    return dataWithSizePath[size]
    # fullPath = joinpath(pathToFolder, printFileName)
    # if not file_exists(fullPath):
    #     printFileName = printFileName.replace('.pdf', '.cdr')
    #     fullPath = joinpath(pathToFolder, printFileName)
    # if not file_exists(fullPath):
    #     fullPath = pathToBug
    # return fullPath


def createPathToPrintWithSize(printNameAll, size):
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
        for i, line in enumerate(dataFromOrderFile):
            orderNum = line['Номер задания']
            orderNum = orderNum if type(
                orderNum) == str else str(orderNum)[0:-2]
            if orderNum == '' and line['Размер'] == '':
                if dataFromOrderFile[i + 1]['Номер задания'] != '':
                    with open(joinpath(pathToTablesV2, nameTable.format(str(numTable))) + '.txt', 'w', encoding='ANSI') as file:
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
                    line['Размер']) == float else str(line['Размер']), orderNum, str(numTable))
                if size != None:
                    # позже добавить условие что картхолдеры, з фолд, пластины и тп по старому делать, остально по новому
                    pathToFile = createpathToFile(printName)
                    pathToSize = createpathToSize(size)
                    pathToPrintWithSize = createPathToPrintWithSize(printName, size)
                else:
                    pathToFile = pathToBug
                if mode == 'smallPlastinMode' or mode == 'smallCartholderMode':
                    data.append(';'.join([
                        orderNum, pathToFile, X.replace('.', ','), Y.replace('.', ','), line['Название'], pathToPrintWithSize]))
                else:
                    data.append(';'.join([
                        orderNum, pathToFile, X.replace('.', ','), Y.replace('.', ','), line['Название'], pathToSize]))
        with open(joinpath(pathToTablesV2, nameTable.format(str(numTable))) + '.txt', 'w', encoding='ANSI') as file:
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
    application = PrintHelper()
    application.show()
    app.exec()
    startPrintHelper()