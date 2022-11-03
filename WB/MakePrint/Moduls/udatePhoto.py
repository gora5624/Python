import requests
import multiprocessing
import sys
import pandas
# import time


def pushPhoto(line, token, requestUrl, countTry=0):
    jsonRequest = {
        "vendorCode": line['Артикул товара'],
        "data": line['Медиафайлы'].split(';')
        }
    headersRequest = {'Authorization': '{}'.format(token), 'X-Vendor-Code': line['Артикул товара']}
    try:
        r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest, timeout=1)  
        if '"Неверный запрос: по данному артикулу не нашлось карточки товара","additionalErrors' in r.text:
            print('Не нашлось карточки товара '+jsonRequest['vendorCode'])
        if '"Внутренняя ошибка сервиса","additionalErrors' in r.text:
            print('1')
        print(r.text + ' ' + jsonRequest['vendorCode'])
    except requests.ConnectionError:
        r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest, timeout=1) 
        print(r.text)
    except requests.exceptions.ReadTimeout:
        print('requests.ReadTimeout')
    except:
        print('TimeoutError')
    if requestsVendorCode(line['Артикул товара']) != 0 and countTry < 5:
        countTry +=1
        pushPhoto(line, token, requestUrl, countTry)



def requestsVendorCode(vendoreCode):        
    url = 'https://suppliers-api.wildberries.ru/content/v1/cards/filter'
    headersRequest = {'Authorization': '{}'.format('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM')}
    json = {
  "vendorCodes": [vendoreCode
  ]
}
    countTry = 0
    while countTry <6 :
        try:
            response = requests.post(url=url, headers=headersRequest, json=json, timeout=2)
            if response.status_code == 200:
                for card in response.json()['data']:
                    if card['vendorCode'] == vendoreCode:
                        if len(card['mediaFiles']) != 0:
                            return 0
                        else:
                            return 1
        except:
            countTry+=1
            continue





print('work')
pathToFile = r'F:\Бейджи.xlsx' # sys.argv[1:][0].replace('#', ' ')
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'# sys.argv[1:][1].replace('#', ' ')
# pathToFile = r'F:\Для загрузки\Готовые принты\Силикон\Чехол iPhone 6 силикон с отк.кам. проз. под карту.xlsx'
# token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
# pathToFile = sys.argv[1:][0].replace('#', ' ')
df = pandas.DataFrame(pandas.read_excel(pathToFile))
requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/media/save'
if __name__ == '__main__':
    pool = multiprocessing.Pool()
    for line in df.to_dict('records'):
    #     pushPhoto(line, token, requestUrl)
        pool.apply_async(pushPhoto, args=(line, token, requestUrl,))
    pool.close()
    pool.join()
    # jsonRequest = {
    # "vendorCode": line['Артикул товара'],
    # "data": line['Медиафайлы']
    # }
    # headersRequest = {'Authorization': '{}'.format(token), 'X-Vendor-Code': line['Артикул товара']}
    # try:
    #     r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest)  
    #     print(r.text)
    # except requests.ConnectionError:
    #     r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest) 
    #     print(r.text)

# uplaodImage(token, pathToFile)