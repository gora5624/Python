import os
import base64
import fpdf
import requests
from os.path import join as joinpath
import PyPDF2
import pandas

Token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjgyYTU2OGZlLTgyNTctNGQ2Yi05ZTg1LTJkYTgxMTgxYWI3MSJ9.ROCdF7eOfTZA-atpsLGTAi15yDzHk2UMes05vwjZwn4'

Url = r'https://suppliers-api.wildberries.ru/api/v2/supplies?status=ON_DELIVERY'

response = requests.get(Url, headers={
    'Authorization': '{}'.format(Token)})

outListPath = r'D:\skikers.xlsx'
q = response.json()
listSup = []
for supp in q['supplies']:
    id_ = supp['supplyId']
    Url2 = r'https://suppliers-api.wildberries.ru/api/v2/supplies/{}/orders'
    response2 = requests.get(Url2.format(id_), headers={
        'Authorization': '{}'.format(Token)})
    while response2.status_code != 200:
        response2 = requests.get(Url2.format(id_), headers={
            'Authorization': '{}'.format(Token)})
        print('error2')
    a = response2.json()
    for ord in a['orders']:
        ord.update(Supp=id_)
    listSup.extend(a['orders'])
listSup
listStik = []
for order in listSup:
    Url3 = r'https://suppliers-api.wildberries.ru/api/v2/orders/stickers'
    json = {"orderIds": [
            int(order['orderId'])]
            }

    response3 = requests.post(Url3, headers={
        'Authorization': '{}'.format(Token)}, json=json)
    while response3.status_code != 200:
        response3 = requests.post(Url3, headers={
            'Authorization': '{}'.format(Token)}, json=json)
        print('error3')
    d = response3.json()
    d['data'][0].update(Supp=order['Supp'])
    listStik.extend(d['data'])
listStikpd = pandas.DataFrame(listStik)
listStikpd.to_excel(outListPath, index=False)
