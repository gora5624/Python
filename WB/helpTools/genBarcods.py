import requests
import time
import pandas

def generate_bar_WB(count):
        listBarcode = []
        countTry = 0
        url = "https://suppliers-api.wildberries.ru/content/v1/barcodes"
        headers = {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'}

        while count > 5000:
            
            while True and countTry < 10:
                json = {
                        "count": 5000
                        }
                try:
                    r = requests.post(url, json=json, headers=headers)
                    listBarcode.extend(r.json()['data'])
                    if not r.json()['error']:
                        count -= 5000
                        break
                except:
                    print(
                        'Ошибка получения ШК. count = {}, пытаюсь повторно получить.'.format(count))
                    print(r.rext)
                    countTry += 1
                    time.sleep(10)
                    continue
        while True and countTry < 10:
            json = {
                        "count": count
                        }
            try:
                r = requests.post(url, json=json, headers=headers)
                listBarcode.extend(r.json()['data'])
                if not r.json()['error']:
                    break
            except:
                print(
                    'Ошибка получения ШК. count = {}, пытаюсь повторно получить.'.format(count))
                countTry += 1
                time.sleep(10)
                continue

        return listBarcode


pd = pandas.DataFrame(generate_bar_WB(240))
pd.to_excel(r'E:\barcodes.xlsx')
