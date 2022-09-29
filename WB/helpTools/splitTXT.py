import pandas
from os.path import abspath, join as joinPath

chunk = int(input('По сколько строк делить, число: '))
i = 0
filepath = input('Введите пусть к файлу: ')
df = pandas.DataFrame(pandas.read_table(filepath))
for j in range(0,len(df),chunk):
    df.iloc[j:j+chunk].to_excel(joinPath(abspath(filepath)).replace('.txt', '_{}.xlsx').format(i), index=False)
    i+=1