import pandas as pd
from os.path import basename

filePath = r"F:\Downloads\8 партия_ производство общее.xlsx"
df = pd.DataFrame(pd.read_excel(filePath))
df.insert(2,column='ШК все',value='')
for model in df.loc[:, 'Модель']:
    listModels = df.loc[df['Модель']==model]['ШК'].values.tolist()
    strModels = ','.join(str(x) for x in listModels)
    df.loc[df['Модель']==model, ['ШК все']] = strModels
df.to_excel(filePath.replace(basename(filePath), 'New.xlsx'), index=False)

# # # import os
# # # import shutil
# # # import pandas as pd


# # # path_ = r'\\192.168.0.111\shared\_Общие документы_\Буфер обмена для ПО\Принты на выбор\Выбрано'
# # # path_2 = r'\\192.168.0.111\shared\_Общие документы_\Буфер обмена для ПО\Принты на выбор\Новая папка'
# # # list_ = pd.DataFrame(pd.read_excel(r"D:\Книга1.xlsx")).to_dict('list')['Name']
# # # for file in os.listdir(path_):
# # #     if file not in list_ and 'db' not in file:
# # #         shutil.copy(os.path.join(path_,file), os.path.join(path_2,file))


# # import os
# # import shutil

# # list_0 = os.listdir(r'\\192.168.0.111\shared\_Общие документы_\Буфер обмена для ПО\Принты на выбор\Топ 200')
# # for i in list_0:
# #     shutil.copy(os.path.join(r'F:\новые принты',i.split('_')[0],i.split('_')[1].replace('png','pdf')), os.path.join(r'F:\новые принты\top_200',i.replace('png','pdf') ))


# import requests
# import pandas as pd

# token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjNhZmUzMzMzLWFmYjEtNDI5Yi1hN2Q1LTE1Yjc4ODg4MmU5MSJ9.kWUDkHkGrtD8WxE9sQHto5B7L3bQh-XRDf7EeZQiw7A'
# json = {
#   #"targetIMT": 152838929,
#   "nmIDs": [
#     102252434
#   ]
# }
# url='https://suppliers-api.wildberries.ru/content/v1/cards/moveNm'
# headers = {'Authorization': '{}'.format(token)}
# json2 ={
#   "vendorCodes": ["iPhone_SE_2_BP_OCM_CLR_HLD_CLD_PRNT_1972"],
#   "allowedCategoriesOnly": True
# }
# url2='https://suppliers-api.wildberries.ru/content/v1/cards/filter'
# r = requests.post(url=url, json=json, headers=headers)
# print(r.text)
# r = r.json()['data']
# r
# #pd.DataFrame(r).to_excel(r'D:\tmp2.xlsx', index=False)