import requests
import pandas


# # Получить спиоск номенклатур
# requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/cards/list'
# token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
# jsonRequest = {
#   "sort": {
#     "limit": 1000,
#     "offset": 0,
#     "searchValue": "",
#     "sortColumn": "",
#     "ascending": False
#   }
# }
# headersRequest = {'Authorization': '{}'.format(token)}
# responce = requests.post(requestUrl, json=jsonRequest, headers=headersRequest)
# a = responce.json()
# a


# # Получить характеристики карточки
# requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/cards/filter'
# token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
# jsonRequest = {
#     "vendorCodes": "Infinix_Hot_12_Play_BP_CCM_CLR_PTT_PRNT_1080"
# }
# headersRequest = {'Authorization': '{}'.format(token)}
# responce = requests.get(requestUrl, params=jsonRequest, headers=headersRequest)
# a = responce.json()
# a
