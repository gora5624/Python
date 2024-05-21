import pandas as pd
import os


# listBar = pd.read_excel(r"\\192.168.0.111\shared\Отдел производство\Отдел Резки\Смартфоны Планшеты для резки WB\Сопоставление макетов.xlsx").fillna(0).to_dict('records')
# listOrders = pd.read_excel(r"F:\Нано.xlsx").fillna(' ')
# listOrders = listOrders.to_dict('records')

# for line in listOrders:
#     for line2 in listBar:
#         try:
#             [int(x) for x in line2['ШК'].split(',')]
#         except:
#             continue
#         if line['Штрихкод'] in [int(x) for x in line2['ШК'].split(',')]:
#             line.update({'Макет':line2['Файл']})
#             print()
# pd.DataFrame(listOrders).to_excel(r'F:\Нано2.xlsx')
# pd.DataFrame(listOrders).to_csv(r'F:\Нано2.txt')
# df = pd.DataFrame(open(r"F:\Нано3.txt", 'r').read().split('\\n')).to_csv(r"F:\Нано4.txt", sep=';')
df = pd.read_csv(r"F:\Нано4.txt", sep=';').to_excel(r"F:\Нано4.xlsx")
