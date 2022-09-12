import numpy
import pandas
import numpy
import os

chunk = 100
i = 0
df = pandas.DataFrame(pandas.read_excel(r'F:\создать 3\Книга1.xlsx'))
for j in numpy.array_split(df, len(df)//chunk):
    j.to_excel(r'F:\создать 3\создать_{}.xlsx'.format(i), index=False)
    i+=1