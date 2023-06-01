import pandas as pd
from os.path import basename

filePath = r"F:\Downloads\писарев.xlsx"
df = pd.DataFrame(pd.read_excel(filePath))
df.insert(2,column='ШК все',value='')
for model in df.loc[:, 'Модель']:
    listModels = df.loc[df['Модель']==model]['ШК'].values.tolist()
    strModels = ','.join(str(x) for x in listModels)
    df.loc[df['Модель']==model, ['ШК все']] = strModels
df.to_excel(filePath.replace(basename(filePath), 'New.xlsx'), index=False)
