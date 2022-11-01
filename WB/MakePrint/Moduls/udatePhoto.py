import requests
import multiprocessing
import sys
import pandas
# import time


def pushPhoto(line, token, requestUrl):
    jsonRequest = {
        "vendorCode": line['Артикул товара'],
        "data": [line['Медиафайлы']]
        }
    headersRequest = {'Authorization': '{}'.format(token), 'X-Vendor-Code': line['Артикул товара']}
    try:
        r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest, timeout=1)  
        if '"Неверный запрос: по данному артикулу не нашлось карточки товара","additionalErrors' in r.text:
            print('Не нашлось карточки товара '+jsonRequest['vendorCode'])
        print(r.text + ' ' + jsonRequest['vendorCode'])
    except requests.ConnectionError:
        r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest, timeout=1) 
        print(r.text)
    except TimeoutError:
        
        pass


print('work')
pathToFile = sys.argv[1:][0].replace('#', ' ')
token = sys.argv[1:][1].replace('#', ' ')
# pathToFile = r'F:\Для загрузки\Готовые принты\Силикон\Чехол iPhone 6 силикон с отк.кам. проз. под карту.xlsx'
# token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
# pathToFile = sys.argv[1:][0].replace('#', ' ')
df = pandas.DataFrame(pandas.read_excel(pathToFile))
requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/media/save'
if __name__ == '__main__':
    pool = multiprocessing.Pool(8)
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