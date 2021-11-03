from os.path import join as joinpath
from os.path import basename
from os import listdir

from my_lib import read_xlsx
import xlrd


mainPath = r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд'


def read_xlsx(file_path, title='Yes'):
    nameList = 'основной' if 'стекла' not in file_path else [
        '3D_стекла', 'глянец', 'матовые', 'камеры']
    rd = xlrd.open_workbook(file_path)
    if type(nameList) == str:
        try:
            sheet = rd.sheet_by_name(nameList)
        except:
            data = []
            return data
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
    elif type(nameList) == list:
        data = []
        for name in nameList:
            try:
                sheet = rd.sheet_by_name(name)
            except:
                return data
            if title == 'Yes':
                try:
                    Name_row = sheet.row_values(0)
                except IndexError:
                    continue
                start = 1
            elif title == 'No':
                Name_row = None
                start = 0
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


def findLineOrder(fileOrder, stiker):
    for line in fileOrder:
        try:
            if line['Этикетка'] == stiker:
                print((line['Название'], line['ШК'], line['Номер задания']))
                return True
        except:
            return False
    return False


def findFileOrder(dir_, stiker):
    for file in listdir(dir_):
        if '.xls' in file and "$" not in file:
            data = read_xlsx(joinpath(dir_, file))
            if findLineOrder(data, stiker):
                print(basename(file))
                return True
    return False


def findDirOrder(stiker):
    dirListForFind = [joinpath(mainPath, r'Новые'),
                      joinpath(mainPath, r'В работе'),
                      joinpath(mainPath, r'Отработано')]
    for dir_ in dirListForFind:
        if findFileOrder(dir_, stiker):
            print(dir_)
            return True
    return False


def getStiker():
    stikerTMP = str(input('Введите стикер: '))
    stiker = (stikerTMP[0:6] + ' ' + stikerTMP[6:]
              ) if ' ' not in stikerTMP else stikerTMP
    return stiker


if __name__ == '__main__':
    stiker = getStiker()
    print('Идёт поиск...')
    findDirOrder(stiker)
    input('Нажмите Enter для выхода')
