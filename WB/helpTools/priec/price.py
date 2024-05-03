import requests
import pandas as pd
import os
import time

class priceMod:
    def __init__(self):
        self.urlPushPrice = 'https://discounts-prices-api.wb.ru/api/v2/upload/task'
        # self.urlPushDiscount = 'https://suppliers-api.wildberries.ru/public/api/v1/updateDiscounts'
        self.nmIdList = nmIdList
        self.headers = {'Authorization': token}
        self.discount = discount
        self.price = price


def pushPrice(listPrice, f):
    jsonPrice = []
    listPrice = listPrice.to_dict('records')
    if f == 'Манвел цены.xlsx':
        token = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njk1MSwiaWQiOiIyMzUyZGFmYS05NTdhLTQ0MzAtYWFhMi1lZGM5NDZkZDY0ODEiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjUyNzczNiwicyI6MTAsInNpZCI6ImFhNDdlNDg5LTU5ZTAtNDIzMi1hMWJmLTBlMTIzOWYwNDJmMSIsInVpZCI6NDUzMjI5MjB9.j9s_VtDpTEWceEd1vUTWf6uofUuSY30q0UrR-H047qZE40sb8atwtAviABB7eoeLQdu3T69UosBdn_Bvj2-2ZQ'
    if f =='Караханян цены.xlsx':
        token = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njg4MiwiaWQiOiI4YjEzZWUzOC03MGIxLTQ3ZjgtYTdlNC03OTIzY2Q2ZmQ3ZTciLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjEwMTA2MiwicyI6MTAsInNpZCI6IjNhOTNkZGMxLWFhNTctNWMyYi05YzVjLWRkZDIyMTg4OTQ0MCIsInVpZCI6NDUzMjI5MjB9.DXm6RuooUieyrnNdXr3FfPPdwK5uV4aiTF5SZIryJUhbQW4uScXQLEb-n8p0iM3RT6Js6aVKijiyOkawE6r76g'
    if f == 'Самвел цены.xlsx':
        token = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njk3MiwiaWQiOiJjZWE4ZTNmYy1iYzg5LTRjYjktYmNmNy0xN2ZiNmNjNzk1MTQiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjgxOTI0NiwicyI6MTAsInNpZCI6IjBhYjhiMTA1LTA1MWYtNGVkNi04NzBiLTM5OWU3NWUxMDI4NiIsInVpZCI6NDUzMjI5MjB9.bOmPtl_ZXx-1C25-5CbftPJVQuuHzwG5iH9QUx0x8CdZCjI9ZnbFgMU1ijL-lfgn_N1JxPvojV2dBrKTpDnolw'

    
    headers = {'Authorization': token}
    urlPushPrice = 'https://discounts-prices-api.wb.ru/api/v2/upload/task'
    for str_ in listPrice:
        json = {
                    "nmId": str_['nmID'],
                    "price": str_['price'],
                    "discount": str_['discount']
                }
        jsonPrice.append(json)
    countTry = 0
    for i in range(0,len(jsonPrice),1000):
        while countTry <5:
            r = requests.post(url=urlPushPrice, json={'data': jsonPrice[i:i+1000]}, headers=headers)
            time.sleep(1)
            if r.status_code == 200:
                print('Цены установлены успешно')
                break
            elif 'No goods for process' in r.text:
                print('Цены уже установлены')
                break
            else:
                countTry+=1
                print('Ошибка установки цен')
                continue


for f in os.listdir(r'F:\cltjkfnm'):
    if '~' not in f:
        listPrice = pd.read_excel(os.path.join(r'F:\cltjkfnm', f))
        pushPrice(listPrice, f)