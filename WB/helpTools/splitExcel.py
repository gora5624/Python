from ntpath import join
import numpy
import pandas
import numpy
from os.path import abspath, join as joinPath

chunk = int(input('По сколько делить, число: '))
i = 0
filepath = input('Введите пусть к файлу: ')
df = pandas.DataFrame(pandas.read_table(filepath,sep='\t'))
for j in numpy.array_split(df, len(df)//chunk):
    j.to_excel(joinPath(abspath(filepath),'..','split_{}.xlsx'.format(i)), index=False)
    i+=1