from urllib import request
import aiohttp
import asyncio
import pandas
import time
import requests

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjgxYjczNGVmLWI2OWUtNGRhMi1iNTBiLThkMTEyYWM4MjhkMCJ9.pU1YOOirgRe3Om-WRYT61AofToggCLbV3na7GbXKGqU'
warehouseId = 10237
url = 'https://suppliers-api.wildberries.ru/api/v3/stocks/{}'
df = pandas.DataFrame(pandas.read_excel(r"C:\Users\Георгий\Documents\stoks.xlsx"))
data = {'stocks':[]}
for line in df.to_dict('records'):
    data['stocks'].append({
      "sku": str(line['Баркод']),
      "amount": line['Количество']
    })


while True:
    for i in range(0,len(data['stocks']),900):
        json_ = {'stocks':data['stocks'][i:i+900] }
        response = requests.put(url.format(warehouseId), headers={
                'Authorization': '{}'.format(token)}, json=json_)
        if response.status_code != 204:
            # print('Возникла ошибка. STATUS CODE: ' + str(response.status_code) + ' TEXT: ' + response.text)
            if response.status_code == 429:
                time.sleep(5)
                response = requests.put(url.format(warehouseId), headers={
                'Authorization': '{}'.format(token)}, json=json_)
                continue
            dataTMP = response.json()[0]['data']
            for j in dataTMP:
                json_['stocks'].remove(j)
            if len(json_['stocks']) !=0:
                response = requests.put(url.format(warehouseId), headers={
                    'Authorization': '{}'.format(token)}, json=json_)
                if response.status_code != 204:
                    print('Возникла ошибка. STATUS CODE: ' + str(response.status_code) + ' TEXT: ' + response.text)
                    time.sleep(5)
            else:
                continue
    print('done')
    time.sleep(30*60)