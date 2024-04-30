import os
import pandas as pd

mainPath = r'F:\Для загрузки\заполнть баркоды'
dfWithBarcods = pd.read_table(r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Манвел.txt").loc[:,['sku', 'vendorCode']]
for file in os.listdir(mainPath):
    if '.xlsx' in file:
        dfCase = pd.read_excel(os.path.join(mainPath,file))
        tmp = dfCase.merge(dfWithBarcods, how='left', left_on='Артикул товара', right_on='vendorCode')
        dfCase.loc[tmp['sku'].notnull(), 'Баркод товара'] = tmp['sku']
        # dfWithBarcodsNew = dfWithBarcods[~dfWithBarcods.isin()].loc[:,'vendorCode' == dfCase['Артикул товара']]
        # dfCase['Баркод товара'] = dfWithBarcods['sku']
        dfCase.to_excel(os.path.join(mainPath,file),index=False)
        # test = dfCase.loc[dfCase['Артикул товара'].isin(dfWithBarcods['vendorCode']), ['Баркод товара']] = dfWithBarcods.loc[dfWithBarcods['vendorCode'].isin(dfCase['Артикул товара']),['sku']]
        # test
        # dfCaseNew = dfCase['Баркод товара'] = dfWithBarcods.loc
        # dfCaseNew.drop('vendorCode')
        # dfCaseNew.to_excel(os.path.join(mainPath,file),index=False)
# __Error__ {"data":null,"error":true,"errorText":"Failed to update, nm 80493992 can not be found","additionalErrors":{}}