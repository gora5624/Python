import requests
import pandas
import asyncio
import aiohttp
from aiohttp import ClientConnectorError
import json

# def getListNomenclatures(token, modelListCard):
#       requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/cards/list'
#       headersRequest = {'Authorization': '{}'.format(token)}
#       dataCard = []
#       for i in range(0,modelListCard*3,1000):
#           jsonRequest = {
#                   "sort": {
#                   "limit": 1000,
#                   "offset": i,
#                   "sortColumn": "updateAt",
#                   "ascending": False
#                   }
#               }
#           response = requests.post(requestUrl, headers=headersRequest, json=jsonRequest).json()
#           for i in response['data']['cards']:
#             dataCard.append(i['vendorCode'])
#           # dataCard.extend(response['data']['cards'])
#       return(dataCard)

# getListNomenclatures('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w', 5313)

# # path = r'C:\Users\Георгий\Desktop\Список1.txt'
# # pd = pandas.DataFrame(pandas.read_table(path))
# # pd
# # # создать товар
# # requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/cards/upload/add'
# # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
# # # jsonRequest = {
# # #   "vendorCode": "Infinix_Hot_12_Play_BP_CCM_CLR_PTT_PRNT_1080",
# # #   "cards": [
# # #     {
# # #       "vendorCode": "Infinix_Hot_12_Play_BP_CCM_CLR_PTT_PRNT_1080_3",
# # #       "mediaFiles": ['http://95.78.233.163:8001/wp-content/uploads/Готовые принты/Силикон/Realme C35/прозрачный/(Принт 1017).jpg'],
# # #       "characteristics": [
# # #         {
# # #             'Предмет': 'Чехлы для телефонов'
# # #         }
# # #       ],
# # #       "sizes": [
# # #         {
# # #           "price": 399,
# # #           "skus": [
# # #             "2045030458629"
# # #           ]
# # #         }
# # #       ]
# # #     }
# # #   ]
# # # }
# # jsonRequest = {
# #   "vendorCode": "Infinix_Hot_12_Play_BP_CCM_CLR_PTT_PRNT_1080",
# #   "cards": [
# #     {
# #       "vendorCode": "Infinix_Hot_12_Play_BP_CCM_CLR_PTT_PRNT_1080_8",
# #       'mediaFiles': ['http://95.78.233.163:8001/wp-content/uploads/Готовые принты/Силикон/Realme C35/прозрачный/(Принт 1017).jpg'],
# #       "characteristics": [
# #         {
# #           'Рисунок': ['Композиция с красным синим и жёлтым Композиция Х Горы и море']},
# #           {'Тип чехлов': ['бампер-накладка']},
# #           {'Повод': ['день рождения', 'Подарок женщине','новый год']},
# #           {'Особенности чехла': ['Защищает ваш смартфон от падений и царапин']},
# #           {'Комплектация': ['Защитный кейс на Infinix Hot 12 Play 1 шт.']},
# #           {'Модель': ['Infinix Hot 12 Play','ИНФИНИКС Хот 12 Плэй','чехол на Infinix Hot 12 Play']},
# #           {'Вид застежки': ['без застежки']},
# #           {'Декоративные элементы': ['print']},
# #           {'Совместимость': ['Infinix Hot 12 Play','ИНФИНИКС Хот 12 Плэй','ИНФИНИКС Хот 12 Плэй','Infinix Hot 12 Play']},
# #           {'Назначение подарка': ['Детям внукам племянникам','Жене Маме Бабушке','Мужу дедушке Папе Брату Другу сыну Парню']},
# #           {'Любимые герои': ['Другие герои']},
# #           {'Материал изделия': ['силикон','ТПУ','полиуретан']},
# #           {'Производитель телефона': 'Infinix'},
# #           {'Бренд': 'Mobi711'},
# #           {'Страна производства': ['Китай']},
# #           {'Наименование': 'Защитный чехол Infinix Hot 12 Play'},
# #           {'Предмет':'Чехлы для телефонов'},
# #           {'Цвет': ['прозрачный']},
# #           {'Медиафайлы':['http://95.78.233.163:8001/wp-content/uploads/Готовые принты/Силикон/Realme C35/прозрачный/(Принт 1017).jpg']},
# #           {'Высота упаковки': 18.5},
# #           {'Ширина упаковки': 11},
# #           {'Глубина упаковки': 1.5},
# #           {'Описание': 'Прозрачная силиконовая накладка на Infinix Hot 12 Play отлично смотрится на смартфоне и надежно защищает Ваш смартфон от последствий после падений / трений. Чехол накладка не скользит в руке, бампер легко снять и надеть, совместим со всеми стеклами. Все технические отверстия идеально выверены по размерам и положению телефона. Плотное облегание телефона. Влагоотталкивающие, амортизирующие свойства материала силиконового чехла защитят телефон от влаги, пыли и механических повреждений. Аксессуар выполнен из плотного бесшовного силикона, который отличается высокой износостойкостью и практичностью.1'}
# #       ],
# #       "sizes": [
# #         {
# #           'techSize': '0',
# #           "price": 199,
# #           "skus": [
# #             "2045030458552"
# #           ]
# #         }
# #       ]
# #     }
# #   ]
# # }
# # headersRequest = {'Authorization': '{}'.format(token)}
# # responce = requests.post(requestUrl, json=jsonRequest, headers=headersRequest)
# # a = responce.json()
# # a


# # Получить характеристики карточки
# # requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/cards/filter'
# # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
# # jsonRequest = {
# #   "vendorCodes": [
# #     "iPhone_14_Plus_BP_CCM_CLR_HLD_CAC_PRNT_1269"
# #   ]
# # }
# # headersRequest = {'Authorization': '{}'.format(token)}
# # responce = requests.post(requestUrl, json=jsonRequest, headers=headersRequest)
# # card = responce.json()
# # nmID = card['data'][0]['nmID']
# # chrtID = card['data'][0]['sizes'][0]['chrtID']


# # # Получить список карточек
# # requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/cards/list'
# # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
# # offset = 0
# # dataCard = []
# # while True:
# #   offset+=1000
# #   jsonRequest = {
# #     "sort": {
# #       "limit": 1000,
# #       "offset": offset,
# #       "sortColumn": "updateAt",
# #       "ascending": False
# #     }
# #   }
# #   headersRequest = {'Authorization': '{}'.format(token)}
# #   responce = requests.post(requestUrl, json=jsonRequest, headers=headersRequest)
# #   card = responce.json()['data']#['cards']
# #   if len(card) < 1000:
# #     dataCard.extend(card)
# #     break
# #   else:
# #     dataCard.extend(card)
# # dataCardpd = pandas.DataFrame(dataCard)
# # dataCardpd.to_excel(r'E:\nomenclatures.xlsx', index=False)

# async def asyncRequest(requestUrl, headersRequest, jsonRequest, dataCard, session):
#   while True:
#     #try:
      
#         async with session.post(requestUrl, headers=headersRequest, json=jsonRequest) as response: 
#           if response.status == 429:
#               print(response.status)
#               print(await response.text())
#               await asyncio.sleep(5)
#               #await session.close()
#               continue
#           elif response.status == 200:
#               print('Успешно')
#               a = json.loads(await response.text())['data']['cards']
#               dataCard.extend(a)
#               break
#           else:
#               #print(await response.text())
#               #await session.close()
#               break
#               #await asyncio.sleep(5)
#               #continue
#     # except ClientConnectorError:
#     #     continue



# async def getTakskForGetNomenclatures():
#   requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/cards/list'
#   token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
#   headersRequest = {'Authorization': '{}'.format(token)}
#   #offset = 0
#   dataCard = []
#   tasks = []
#   async with aiohttp.ClientSession() as session:
#     for i in range(0,800000,1000):
#       jsonRequest = {
#         "sort": {
#           "limit": 1000,
#           "offset": i,
#           "sortColumn": "updateAt",
#           "ascending": False
#         }
#       }
#       tasks.append(asyncio.create_task(asyncRequest(requestUrl, headersRequest, jsonRequest, dataCard, session)))
#       #data = await asyncRequest(requestUrl, headersRequest, jsonRequest)
#     await asyncio.wait(tasks)
#   return dataCard
#     # if len(data) < 1000:
#     #   dataCard.extend(data)
#     #   break
#     # else:
#     #   dataCard.extend(data)



# def startGetNomenclarures():
#   loop = asyncio.get_event_loop()
#   pd = pandas.DataFrame(loop.run_until_complete(getTakskForGetNomenclatures()))
#   pd.to_excel(r'E:\nomenclatures.xlsx', index=False)

# if __name__ == '__main__':
#   startGetNomenclarures()




# # # Загрузить фото
# # requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/media/save'
# # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
# # jsonRequest = {
# #   "vendorCode": 'Infinix_Hot_12_Play_BP_CCM_CLR_PTT_PRNT_1080_8',
# #   "data": [
# #     "http://95.78.233.163:8001/wp-content/uploads/Готовые принты/Силикон/Чехол iPhone 14 Plus силикон с зак.кам. проз. под карту/(Принт 1002).jpg"
# #   ]
# # }
# # headersRequest = {'Authorization': '{}'.format(token), 'X-Vendor-Code': 'Infinix_Hot_12_Play_BP_CCM_CLR_PTT_PRNT_1080_8'}
# # responce = requests.post(requestUrl, json=jsonRequest, headers=headersRequest)
# # a = responce.json()
# # print(responce.text)
# # a



# редактировать товар
requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/cards/update'
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
jsonRequest = [
    {
      'nmID': 23179290,
      "vendorCode": "00-00096611Герб_Принт_8",
      "characteristics": [
        # {
        #   'Рисунок': ['Композиция с красным синим и жёлтым Композиция Х Горы и море']},
        #   {'Тип чехлов': ['бампер-накладка']},
        #   {'Повод': ['день рождения', 'Подарок женщине','новый год']},
        #   {'Особенности чехла': ['Защищает ваш смартфон от падений и царапин']},
        #   {'Комплектация': ['Защитный кейс на Infinix Hot 12 Play 1 шт.']},
        #   {'Модель': ['Infinix Hot 12 Play','ИНФИНИКС Хот 12 Плэй','чехол на Infinix Hot 12 Play']},
        #   {'Вид застежки': ['без застежки']},
          {'Декоративные элементы': ['С рисунком. картиной принтом печатью']},
        #   {'Совместимость': ['Infinix Hot 12 Play','ИНФИНИКС Хот 12 Плэй','ИНФИНИКС Хот 12 Плэй','Infinix Hot 12 Play']},
        #   {'Назначение подарка': ['Детям внукам племянникам','Жене Маме Бабушке','Мужу дедушке Папе Брату Другу сыну Парню']},
        #   {'Любимые герои': ['Другие герои']},
        #   {'Материал изделия': ['силикон','ТПУ','полиуретан']},
        #   {'Производитель телефона': 'Infinix'},
          {'Бренд': 'Mobi711'},
        #   {'Страна производства': ['Китай']},
        #   {'Наименование': 'Защитный чехол Infinix Hot 12 Play'},
          {'Высота упаковки': 18.5},
          {'Ширина упаковки': 11},
          {'Глубина упаковки': 1.5},
          {'Предмет':'Чехлы для телефонов'},
          {'Цвет': ['прозрачный','белый']},
          {'Описание': 'Чехол Samsung A72 является отличным аксессуаром, а также украшением смартфона. Благодаря прилеганию к корпусу чехол на A 72 отлично защищает ваш телефон самсунг А72, а также очень удобен в использовании. Чехол для телефона также может стать отличным подарком на любой праздник (день рождения, новый год, 23 февраля, 8 марта) благодаря отличному дизайну и красивому виду. Чехол бампер или чехол накладка очень удобен в использовании. Данный чехол имеет рисунок нанесённый по специальной технологии ультрафиолетовой печати. Он не стирается, не выгорает на солнце и не изнашивается без специального воздействия на него. Рисунок нанесён поверх чехла. Что позволяет почувствовать его и не скрывает всю красоту принта.'}
      ],
      "sizes": [
        {
          'techSize': '0',
          'chrtID': 56562885,
          "price": 199,
          "skus": [
            "2001633954027"
          ]
        }
      ]
    }
  ]
# for i, char in enumerate(card['data'][0]['characteristics']):
#     for key in char.keys():
#         if key == 'Цвет':
#             card['data'][0]['characteristics'][i] = {'Цвет': 'прозрачный'}
#             break
# #card['data'][0]['characteristics']['Цвет'] = ['прозрачный']
# jsonRequest = card['data']
# jsonRequest.pop('imtID')
# jsonRequest.pop('mediaFiles')
# jsonRequest['sizes'][0].pop('wbSize')
headersRequest = {'Authorization': '{}'.format(token)}
responce = requests.post(requestUrl, json=jsonRequest, headers=headersRequest)
a = responce.json()
a

# # requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/directory/colors'
# # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
# # headersRequest = {'Authorization': '{}'.format(token)}
# # responce = requests.get(requestUrl, headers=headersRequest)
# # a = responce.json()['data']
# # for i in a:
# #   print(i)