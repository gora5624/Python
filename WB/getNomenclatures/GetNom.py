import requests
import pandas as pd
import time
import os


# reqUrl = 'https://suppliers-api.wildberries.ru/content/v2/get/cards/list'
# json = {
#   "settings": {
#     "sort": {
#       "ascending": False
#     },
#     "filter": {
#       "allowedCategoriesOnly": True,
#       "withPhoto": -1,
#       # 'textSearch' : '231447781'
#     #   "brands": ['2Case', '2case', 'DIGMA' , 'Mobi113', 'Realme' , 'Samsung' , 'Xiaomi', 'Honor', 'Huawei', 'Mobi115']
#     },
#     "cursor": {
#       "limit": 100
#     }
#   }
# }


# tokenK = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njg4MiwiaWQiOiI4YjEzZWUzOC03MGIxLTQ3ZjgtYTdlNC03OTIzY2Q2ZmQ3ZTciLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjEwMTA2MiwicyI6MTAsInNpZCI6IjNhOTNkZGMxLWFhNTctNWMyYi05YzVjLWRkZDIyMTg4OTQ0MCIsInVpZCI6NDUzMjI5MjB9.DXm6RuooUieyrnNdXr3FfPPdwK5uV4aiTF5SZIryJUhbQW4uScXQLEb-n8p0iM3RT6Js6aVKijiyOkawE6r76g'
# tokenA = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njk1MSwiaWQiOiIyMzUyZGFmYS05NTdhLTQ0MzAtYWFhMi1lZGM5NDZkZDY0ODEiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjUyNzczNiwicyI6MTAsInNpZCI6ImFhNDdlNDg5LTU5ZTAtNDIzMi1hMWJmLTBlMTIzOWYwNDJmMSIsInVpZCI6NDUzMjI5MjB9.j9s_VtDpTEWceEd1vUTWf6uofUuSY30q0UrR-H047qZE40sb8atwtAviABB7eoeLQdu3T69UosBdn_Bvj2-2ZQ'   
# tokenS = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njk3MiwiaWQiOiJjZWE4ZTNmYy1iYzg5LTRjYjktYmNmNy0xN2ZiNmNjNzk1MTQiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjgxOTI0NiwicyI6MTAsInNpZCI6IjBhYjhiMTA1LTA1MWYtNGVkNi04NzBiLTM5OWU3NWUxMDI4NiIsInVpZCI6NDUzMjI5MjB9.bOmPtl_ZXx-1C25-5CbftPJVQuuHzwG5iH9QUx0x8CdZCjI9ZnbFgMU1ijL-lfgn_N1JxPvojV2dBrKTpDnolw'
# tokenI = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5NzAwNywiaWQiOiI1ZWRjMWY0Ni04OWVhLTQxMzktYjVjYi1hNDM5OGUwMzUxNTMiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjExNzEwNDQsInMiOjEwLCJzaWQiOiJkOWU0OGUxZi05ZjgxLTQ1MmMtODRiYy05ZGYxZWRiMzNmNDkiLCJ1aWQiOjQ1MzIyOTIwfQ.y2sbT8zqvoM-iSxKJcsdiEphMoLRfNq8pBsIQnmGQIbc1btCIoe7Qkz65Ur91fVEqyDbQZ-Ry_1tTkgof5hKDw'
# token = tokenA

# headersRequest = {'Authorization': '{}'.format(token)}

# total = 70
# limit = 70
# data = []
# while not total < limit:
#     countTry = 0
#     while countTry < 5:
#         try:
#             r = requests.post(url=reqUrl, headers=headersRequest, json=json, timeout=120)
#             print(str(r.status_code) + ' получил')
#             if r.status_code!= 200:
#                 print('ошибка получения')
#                 countTry+=1
#                 time.sleep(5)
#                 continue
#             total = r.json()['cursor']['total']
#             data.extend(r.json()['cards'])
#             time.sleep(1.2)
#     #         tmp = {
#     #             "updatedAt": "***",
#     #             "limit": 1000,
#     #             "nmID": ***
#     # }
#             json['settings']['cursor'].update(r.json()['cursor'])
#             json
#             # for card in data:
#             #     card.update({'brand':'Xiaomi'})
#             #     if 'photos' in card:
#             #         card.pop('photos')
#             # r = requests.post(url='https://suppliers-api.wildberries.ru/content/v2/cards/update', headers=headersRequest, json=data, timeout=120)
#             # print(str(r.status_code) + ' отправил')
#             # time.sleep(1.2)
#             # if r.status_code == 413:
#             #     r = requests.post(url='https://suppliers-api.wildberries.ru/content/v2/cards/update', headers=headersRequest, json=data[0:50], timeout=120)
#             #     if r.status_code!= 200:
#             #         print('ошибка отправки2')
#             #         countTry+=1
#             #         time.sleep(5)
#             #         continue
#             #     r = requests.post(url='https://suppliers-api.wildberries.ru/content/v2/cards/update', headers=headersRequest, json=data[50:], timeout=120)
#             #     if r.status_code!= 200:
#             #         print('ошибка отправки2')
#             #         countTry+=1
#             #         time.sleep(5)
#             #         continue
#             # if r.status_code!= 200:
#             #     print('ошибка отправки')
#             #     countTry+=1
#             #     time.sleep(5)
#             #     continue
#             break
#         except: 
#             print('ошибка')
#             countTry+=1
#             time.sleep(5)
#             continue
            
# for line in data:
#     tmp = line['sizes']
#     line.update(tmp[0])
#     line.pop('sizes')
#     if 'characteristics' in line:
#       line.pop('characteristics')
# df = pd.DataFrame(data).to_csv(r'F:\data_Манвел.txt', index=False)
        
# dataK = pd.read_csv(r"F:\data_Караханян.txt")#.to_dict('records')
# dataK['skus'] = dataK['skus'].apply(eval)
# dataK = dataK.explode('skus')
# dataK['skus'] = dataK['skus'].astype(str).str.strip()
# dataA = pd.read_csv(r"F:\data_Манвел.txt")#.to_dict('records')
# filtered_data = dataA[dataA['description'].isna() | (dataA['description'] == '')]
# filtered_data.to_excel(r"F:\data_Empty.xlsx")

# dataA['skus'] = dataA['skus'].apply(eval)
# dataA = dataA.explode('skus')
# dataA['skus'] = dataA['skus'].astype(str).str.strip()
# done = pd.merge(dataK, dataA, how='inner', left_on='skus', right_on='skus')
# done

# list2case = dataWB
# with pd.ExcelWriter(r'F:\data_Ман_0.xlsx', engine='xlsxwriter', engine_kwargs={'options': {'use_zip64': True}}) as writer:
#     list2case.to_excel(writer, index=False)
# nmIDlist = dataWB.loc[:,'nmID'].values.tolist()
# vendorCodeList = dataWB['vendorCode'].values.tolist()
# errorslist = []
# dataWB.iloc[0:500000].to_excel(r'F:\data_Ман_0.xlsx', index=False)
# dataWB.iloc[500000:1000000].to_excel(r'F:\data_Ман_1.xlsx', index=False)
# dataWB.iloc[1000000:].to_excel(r'F:\data_Ман_2.xlsx', index=False)
# df = pd.DataFrame()
# for f in os.listdir(r'F:\DATA'):
#     dfData = pd.read_csv(os.path.join(r'F:\DATA', f))
#     df = pd.concat([df, dfData]) 
# df.to_csv(r'F:\DATA\all.txt')
# dfData = pd.read_csv(r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\ШК.txt", sep='\t')#.to_dict('records')
# for f in os.listdir(r'F:\цены'):
#     df = pd.read_excel(os.path.join(r'F:\цены', f))
#     df = df.merge(dfData[['Номенклатура', 'Штрихкод']], how='left', left_on='skus',right_on='Штрихкод')
#     df.to_excel(os.path.join(r'F:\цены', f), index=False)

# # for file in os.listdir(r'\\192.168.0.33\shared\_Общие документы_\Егор\Архив принтов xlsx\Книжки 3 партия\2000'):
# #     dataFile = pd.read_excel(os.path.join(r'\\192.168.0.33\shared\_Общие документы_\Егор\Архив принтов xlsx\Книжки 3 партия\2000',file)).to_dict('records')
# #     for line in dataFile:
# #         if line['nmID'] not in nmIDlist or line['Артикул товара'] not in vendorCodeList:
# #             errorslist.append({"Артикул":line['Артикул товара'],
# #                                 'nmID':line['nmID'],
# #                                 'file':file})

# # pd.DataFrame(errorslist).to_excel(r'E:\MyProduct\Python\WB\MakePrint\errors2000.xlsx', index=False)

# # dataErrors = pd.read_excel(r"E:\MyProduct\Python\WB\MakePrint\errors.xlsx")
# # listFile = dataErrors['file'].values.tolist()
# # for file in os.listdir(r'F:\Для загрузки\загрузить фото — копия'):
# #     if file in listFile:
# #         df2 = pd.read_excel(os.path.join(r'F:\Для загрузки\загрузить фото — копия', file))
# #         tmp = df2.merge(dataErrors, how='left', left_on='Артикул товара',right_on='Артикул')
# #         tmp.to_excel(os.path.join(r'F:\Для загрузки\загрузить фото — копия', file), index=False)


df = pd.read_excel(r'F:\\Под карту.xlsx')['Номенклатура'].values.tolist()
tmp = []
for i in df:
    if i not in os.listdir(r'\\192.168.0.33\shared\_Общие документы_\_Фото\Татьяна рендеры\Прозрачка'):
        tmp.append(i)

pd.DataFrame(tmp).to_excel(r'F:\\Под_создание_моделей.xlsx')