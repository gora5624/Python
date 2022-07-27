import os
import pandas

mainPath = r'C:\Users\Георгий\Downloads\report_2022_7_25аб'
df = pandas.DataFrame()
for file in os.listdir(mainPath):
    tmp = pandas.DataFrame(pandas.read_excel(os.path.join(mainPath, file)))
    df = pandas.concat([tmp, df], ignore_index=True, sort=False)
df.to_excel(os.path.join(mainPath, 'tmp.xlsx'), index=False)