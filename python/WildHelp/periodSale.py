from my_lib import read_xlsx
from my_lib import write_csv


file_path = input("Введите полный путь к файлу: ")
data = read_xlsx(file_path)
dataNew = {}
for line in data:
    Art = line['Артикул WB']
    period = line['Неделя года']
    if Art not in dataNew.keys():
        tmp = {Art: {}}
        dataNew.update(tmp)
        if period not in dataNew[Art].keys():
            tmp2 = {period: line['Заказанные товары, шт.']}
            dataNew[Art].update(tmp2)
    elif Art in dataNew.keys():
        if period not in dataNew[Art].keys():
            tmp2 = {period: line['Заказанные товары, шт.']}
            dataNew[Art].update(tmp2)
        elif period in dataNew[Art].keys():
            dataNew[Art][period] = dataNew[Art][period] + \
                line['Заказанные товары, шт.']
final = []
for lineNew in dataNew:
    Art = lineNew
    countPer = len(dataNew[lineNew])
    tmp = 0
    for linePer in dataNew[lineNew]:
        tmp = tmp + dataNew[lineNew][linePer]
    dataFinal = {'Артикул WB': Art,
                 'Заказы': tmp/countPer}
    final.append(dataFinal)
pathout = input("Введите путь для выходного файла: ")
for lineFin in final:
    write_csv(lineFin, pathout + '\Продажи за период.csv')
