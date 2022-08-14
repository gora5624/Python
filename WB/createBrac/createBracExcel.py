import pandas
from datetime import datetime
import os

pathToFileWithBarcodes = r'\\192.168.0.111\shared\_Общие документы_\Заказы вайлд\BrakHelp\ШК для брака.xlsx'
counter = r'\\192.168.0.111\shared\_Общие документы_\Заказы вайлд\BrakHelp\counter.txt'
branFileName = r'Файл_брака_номер_{}_от_{}_{}.xlsx'

print('Получение данных о штрихкодах...')
df = pandas.DataFrame(pandas.read_excel(pathToFileWithBarcodes))
while True:
    with open(counter, 'r') as file:
        count = int(file.read())
    file.close()

    caseListTMP = pandas.DataFrame(columns=['Номер задания','Количество','Этикетка'])
    while True:
        barcod = input('Отсканируйте ШК чехла, 0 чтобы завершить и создать файл: ')
        if barcod == '0':
            break
        elif barcod == '':
            continue
        tmp = df[df.ШК == int(barcod)]
        if len(tmp) == 0:
            print('ШК не найден')
            continue
        caseListTMP = pandas.concat((caseListTMP,tmp), ignore_index=True)
        caseListTMP = caseListTMP.drop(['name','print'], axis=1)
        caseListTMP['Номер задания'] = '1'
        caseListTMP['Количество'] = '1'
        caseListTMP['Этикетка'] = '1'
        caseListTMP


    curData = datetime.today().date().strftime(r"%d.%m.%Y")
    curTime = datetime.today().time().strftime(r"%H.%M.%S")
    caseListTMP.to_excel(os.path.join(os.path.join(r'\\192.168.0.111\shared\_Общие документы_\Заказы вайлд\Браки', branFileName.format(str(count),curData, curTime))), index=False)
    print('Файл создан в \\192.168.0.111\shared\_Общие документы_\Заказы вайлд\Браки')
    with open(counter, 'w') as file:
        file.write(str(count + 1))
    file.close()