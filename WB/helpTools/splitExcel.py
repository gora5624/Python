import numpy
import pandas
import numpy
import os

chunk = 7000
i = 0
df = pandas.DataFrame(pandas.read_excel(r'C:\Users\Георгий\Downloads\Абраамян\Книга1.xlsx'))
for j in numpy.array_split(df, len(df)//chunk):
    j.to_excel(r'C:\Users\Георгий\Downloads\Абраамян\{}.xlsx'.format(i), index=False)
    i+=1