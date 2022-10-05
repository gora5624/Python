import pandas
from datetime import datetime
import os

# pathToFileWithBarcodes = r'\\192.168.0.111\shared\_Общие документы_\Заказы вайлд\BrakHelp\ШК для брака.xlsx'
pathToTXTFileWithBarcods = r'\\192.168.0.111\shared\_Общие документы_\Заказы вайлд\BrakHelp\ШК.txt'
pathToTXTFileWithNomenclatures = r'\\192.168.0.111\shared\_Общие документы_\Заказы вайлд\BrakHelp\Список стандартный поиск номенклатура.txt'
counter = r'\\192.168.0.111\shared\_Общие документы_\Заказы вайлд\BrakHelp\counter.txt'
branFileName = r'Файл_брака_номер_{}_от_{}_{}.xlsx'

print('Получение данных о штрихкодах...')
# df = pandas.DataFrame(pandas.read_excel(pathToFileWithBarcodes))
dfBarcodes = pandas.DataFrame(pandas.read_table(pathToTXTFileWithBarcods))
dfNomenclatures = pandas.DataFrame(pandas.read_table(pathToTXTFileWithNomenclatures))
while True:
    with open(counter, 'r') as file:
        count = int(file.read())
    file.close()
    dataBrac = []
    caseListTMP = pandas.DataFrame(columns=['Номер задания','Количество','Этикетка'])
    while True:
        barcod = input('Отсканируйте ШК чехла, 0 чтобы завершить и создать файл: ')
        if barcod == '0':
            break
        elif barcod == '':
            continue
        nomenclaturesName = dfBarcodes[dfBarcodes.Штрихкод == int(barcod)]['Номенклатура'].values.tolist()
        printName = dfBarcodes[dfBarcodes.Штрихкод == int(barcod)]['Характеристика'].values.tolist()
        if len(nomenclaturesName) == 0:
            print('ШК не найден')
            continue
        try:
            size = dfNomenclatures[dfNomenclatures.Наименование == nomenclaturesName[0]]['Размер чехла'].values.tolist()[0]
        except:
            print('Не удалось определить размер для {}'.format(nomenclaturesName[0]))
            size = 'Неизвестно, проверьте базу'
        try:
            cod = dfNomenclatures[dfNomenclatures.Наименование == nomenclaturesName[0]]['Код'].values.tolist()[0]
            nomenclaturesNameFull = dfNomenclatures[dfNomenclatures.Наименование == nomenclaturesName[0]]['Наименование для печати'].values.tolist()[0]
        except:    
            print('Не удалось определить код для {}'.format(nomenclaturesName[0]))
            cod = 'Неизвестно, проверьте базу'
        dataTmp = {
            'Номер задания':'1',
            'Количество':'1',
            'Этикетка':'1',
            'ШК': barcod,
            'Название': nomenclaturesNameFull + ' ' + printName[0],
            'Размер': size,
            'Код': cod
        }
        dataBrac.append(dataTmp)
        # caseListTMP = pandas.concat((caseListTMP,tmp), ignore_index=True)
        # caseListTMP = caseListTMP.drop(['name','print'], axis=1)
        # caseListTMP['Номер задания'] = '1'
        # caseListTMP['Количество'] = '1'
        # caseListTMP['Этикетка'] = '1'
        # caseListTMP

    dataBracDF = pandas.DataFrame(dataBrac)
    curData = datetime.today().date().strftime(r"%d.%m.%Y")
    curTime = datetime.today().time().strftime(r"%H.%M.%S")
    # caseListTMP.to_excel(os.path.join(os.path.join(r'\\192.168.0.111\shared\_Общие документы_\Заказы вайлд\Браки', branFileName.format(str(count),curData, curTime))), index=False)
    dataBracDF.to_excel(os.path.join(os.path.join(r'\\192.168.0.111\shared\_Общие документы_\Заказы вайлд\Браки', branFileName.format(str(count),curData, curTime))), index=False)
    print('Файл создан в \\192.168.0.111\shared\_Общие документы_\Заказы вайлд\Браки')
    with open(counter, 'w') as file:
        file.write(str(count + 1))
    file.close()