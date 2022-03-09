import os
import pandas
from my_lib import read_xlsx

pathToFileWithArtList = r'D:\tmp.xlsx'
pathToAllStuffFile = r'D:\\Список номенклатуры — копия.XLSX'
pathToDoneFile = r'D:\Done.xlsx'

listArt = read_xlsx(pathToFileWithArtList)
dataAllStuff = read_xlsx(pathToAllStuffFile)
addinAll = []
for art in listArt:
    addinLine = []
    for stuff in dataAllStuff:
        if art['Артикул'] == stuff['Артикул ИМТ']:
            if 'силикон ' in stuff['Название 1С'].lower():
                if 'силикон' not in addinLine:
                    addinLine.append('силикон')
            if 'книга ' in stuff['Название 1С'].lower():
                if 'книга' not in addinLine:
                    addinLine.append('книга')
            if 'наностекло' in stuff['Название 1С'].lower():
                if 'наностекло' not in addinLine:
                    addinLine.append('наностекло')
                    continue
            if 'стекло ' in stuff['Название 1С'].lower():
                if '3D стекло' not in addinLine:
                    addinLine.append('3D стекло')
                    continue
            if 'принт ' in stuff['Название 1С'].lower():
                if 'принт' not in addinLine:
                    addinLine.append('принт')
            if 'touch ' in stuff['Название 1С'].lower():
                if 'soft-touch' not in addinLine:
                    addinLine.append('soft-touch')
            if 'углами ' in stuff['Название 1С'].lower():
                if 'углы' not in addinLine:
                    addinLine.append('углы')
    adline = {'Артикул': art['Артикул'],
              'Свойства': (";").join(addinLine) if len(addinLine) != 0 else ''}
    addinAll.append(adline)
adlinepd = pandas.DataFrame(addinAll)
adlinepd.to_excel(pathToDoneFile, index=False)
