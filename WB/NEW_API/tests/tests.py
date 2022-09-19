import requests
import pandas


# # создать товар
# requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/cards/upload/add'
# token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
# # jsonRequest = {
# #   "vendorCode": "Infinix_Hot_12_Play_BP_CCM_CLR_PTT_PRNT_1080",
# #   "cards": [
# #     {
# #       "vendorCode": "Infinix_Hot_12_Play_BP_CCM_CLR_PTT_PRNT_1080_3",
# #       "mediaFiles": ['http://95.78.233.163:8001/wp-content/uploads/Готовые принты/Силикон/Realme C35/прозрачный/(Принт 1017).jpg'],
# #       "characteristics": [
# #         {
# #             'Предмет': 'Чехлы для телефонов'
# #         }
# #       ],
# #       "sizes": [
# #         {
# #           "price": 399,
# #           "skus": [
# #             "2045030458629"
# #           ]
# #         }
# #       ]
# #     }
# #   ]
# # }
# jsonRequest = {
#   "vendorCode": "Infinix_Hot_12_Play_BP_CCM_CLR_PTT_PRNT_1080",
#   "cards": [
#     {
#       "vendorCode": "Infinix_Hot_12_Play_BP_CCM_CLR_PTT_PRNT_1080_8",
#       'mediaFiles': ['http://95.78.233.163:8001/wp-content/uploads/Готовые принты/Силикон/Realme C35/прозрачный/(Принт 1017).jpg'],
#       "characteristics": [
#         {
#           'Рисунок': ['Композиция с красным синим и жёлтым Композиция Х Горы и море']},
#           {'Тип чехлов': ['бампер-накладка']},
#           {'Повод': ['день рождения', 'Подарок женщине','новый год']},
#           {'Особенности чехла': ['Защищает ваш смартфон от падений и царапин']},
#           {'Комплектация': ['Защитный кейс на Infinix Hot 12 Play 1 шт.']},
#           {'Модель': ['Infinix Hot 12 Play','ИНФИНИКС Хот 12 Плэй','чехол на Infinix Hot 12 Play']},
#           {'Вид застежки': ['без застежки']},
#           {'Декоративные элементы': ['print']},
#           {'Совместимость': ['Infinix Hot 12 Play','ИНФИНИКС Хот 12 Плэй','ИНФИНИКС Хот 12 Плэй','Infinix Hot 12 Play']},
#           {'Назначение подарка': ['Детям внукам племянникам','Жене Маме Бабушке','Мужу дедушке Папе Брату Другу сыну Парню']},
#           {'Любимые герои': ['Другие герои']},
#           {'Материал изделия': ['силикон','ТПУ','полиуретан']},
#           {'Производитель телефона': 'Infinix'},
#           {'Бренд': 'Mobi711'},
#           {'Страна производства': ['Китай']},
#           {'Наименование': 'Защитный чехол Infinix Hot 12 Play'},
#           {'Предмет':'Чехлы для телефонов'},
#           {'Цвет': ['прозрачный']},
#           {'Медиафайлы':['http://95.78.233.163:8001/wp-content/uploads/Готовые принты/Силикон/Realme C35/прозрачный/(Принт 1017).jpg']},
#           {'Высота упаковки': 18.5},
#           {'Ширина упаковки': 11},
#           {'Глубина упаковки': 1.5},
#           {'Описание': 'Прозрачная силиконовая накладка на Infinix Hot 12 Play отлично смотрится на смартфоне и надежно защищает Ваш смартфон от последствий после падений / трений. Чехол накладка не скользит в руке, бампер легко снять и надеть, совместим со всеми стеклами. Все технические отверстия идеально выверены по размерам и положению телефона. Плотное облегание телефона. Влагоотталкивающие, амортизирующие свойства материала силиконового чехла защитят телефон от влаги, пыли и механических повреждений. Аксессуар выполнен из плотного бесшовного силикона, который отличается высокой износостойкостью и практичностью.1'}
#       ],
#       "sizes": [
#         {
#           'techSize': '0',
#           "price": 199,
#           "skus": [
#             "2045030458552"
#           ]
#         }
#       ]
#     }
#   ]
# }
# headersRequest = {'Authorization': '{}'.format(token)}
# responce = requests.post(requestUrl, json=jsonRequest, headers=headersRequest)
# a = responce.json()
# a


# Получить характеристики карточки
requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/cards/filter'
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
jsonRequest = {
  "vendorCodes": [
    "iPhone_14_Plus_BP_CCM_CLR_HLD_CAC_PRNT_1269"
  ]
}
headersRequest = {'Authorization': '{}'.format(token)}
responce = requests.post(requestUrl, json=jsonRequest, headers=headersRequest)
card = responce.json()
nmID = card['data'][0]['nmID']
chrtID = card['data'][0]['sizes'][0]['chrtID']

# # Загрузить фото
# requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/media/save'
# token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
# jsonRequest = {
#   "vendorCode": 'Infinix_Hot_12_Play_BP_CCM_CLR_PTT_PRNT_1080_8',
#   "data": [
#     "http://95.78.233.163:8001/wp-content/uploads/Готовые принты/Силикон/Чехол iPhone 14 Plus силикон с зак.кам. проз. под карту/(Принт 1002).jpg"
#   ]
# }
# headersRequest = {'Authorization': '{}'.format(token), 'X-Vendor-Code': 'Infinix_Hot_12_Play_BP_CCM_CLR_PTT_PRNT_1080_8'}
# responce = requests.post(requestUrl, json=jsonRequest, headers=headersRequest)
# a = responce.json()
# print(responce.text)
# a



# редактировать товар
requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/cards/update'
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
# jsonRequest = [
#     {
#       'nmID': nmID,
#       "vendorCode": "Infinix_Hot_12_Play_BP_CCM_CLR_PTT_PRNT_1080_4",
#       "characteristics": [
#         # {
#         #   'Рисунок': ['Композиция с красным синим и жёлтым Композиция Х Горы и море']},
#         #   {'Тип чехлов': ['бампер-накладка']},
#         #   {'Повод': ['день рождения', 'Подарок женщине','новый год']},
#         #   {'Особенности чехла': ['Защищает ваш смартфон от падений и царапин']},
#         #   {'Комплектация': ['Защитный кейс на Infinix Hot 12 Play 1 шт.']},
#         #   {'Модель': ['Infinix Hot 12 Play','ИНФИНИКС Хот 12 Плэй','чехол на Infinix Hot 12 Play']},
#         #   {'Вид застежки': ['без застежки']},
#         #   {'Декоративные элементы': ['print']},
#         #   {'Совместимость': ['Infinix Hot 12 Play','ИНФИНИКС Хот 12 Плэй','ИНФИНИКС Хот 12 Плэй','Infinix Hot 12 Play']},
#         #   {'Назначение подарка': ['Детям внукам племянникам','Жене Маме Бабушке','Мужу дедушке Папе Брату Другу сыну Парню']},
#         #   {'Любимые герои': ['Другие герои']},
#         #   {'Материал изделия': ['силикон','ТПУ','полиуретан']},
#         #   {'Производитель телефона': 'Infinix'},
#           {'Бренд': 'Mobi711'},
#         #   {'Страна производства': ['Китай']},
#         #   {'Наименование': 'Защитный чехол Infinix Hot 12 Play'},
#           {'Предмет':'Чехлы для телефонов'},
#           {'Цвет': ['белый']},
#           {'Описание': 'Прозрачная силиконовая накладка на Infinix Hot 12 Play отлично смотрится на смартфоне и надежно защищает Ваш смартфон от последствий после падений / трений. Чехол накладка не скользит в руке, бампер легко снять и надеть, совместим со всеми стеклами. Все технические отверстия идеально выверены по размерам и положению телефона. Плотное облегание телефона. Влагоотталкивающие, амортизирующие свойства материала силиконового чехла защитят телефон от влаги, пыли и механических повреждений. Аксессуар выполнен из плотного бесшовного силикона, который отличается высокой износостойкостью и практичностью.'}
#       ],
#       "sizes": [
#         {
#           'techSize': '0',
#           'chrtID': chrtID,
#           "price": 199,
#           "skus": [
#             "2045030458630"
#           ]
#         }
#       ]
#     }
#   ]
for i, char in enumerate(card['data'][0]['characteristics']):
    for key in char.keys():
        if key == 'Цвет':
            card['data'][0]['characteristics'][i] = {'Цвет': 'прозрачный'}
            break
#card['data'][0]['characteristics']['Цвет'] = ['прозрачный']
jsonRequest = card['data']
# jsonRequest.pop('imtID')
# jsonRequest.pop('mediaFiles')
# jsonRequest['sizes'][0].pop('wbSize')
headersRequest = {'Authorization': '{}'.format(token)}
responce = requests.post(requestUrl, json=jsonRequest, headers=headersRequest)
a = responce.json()
a