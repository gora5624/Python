import pandas

pathToWBNom = r"F:\report_2023_2_21.xlsx\0.xlsx"
pathTo1CNom = r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\ШК.txt"

dfWB = pandas.DataFrame(pandas.read_excel(pathToWBNom))
df1C = pandas.DataFrame(pandas.read_table(pathTo1CNom, sep='\t'))
df = pandas.merge(dfWB, df1C, left_on='Баркод', right_on='Штрихкод', how='left')
df.to_excel(r"F:\report_2023_2_21.xlsx\tmp.xlsx", index=False)