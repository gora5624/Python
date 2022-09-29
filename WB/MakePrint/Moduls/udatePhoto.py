import requests
import multiprocessing
import sys
import pandas
# import time

print('work')
pathToFile = sys.argv[1:][0].replace('#', ' ')
token = sys.argv[1:][1].replace('#', ' ')
# pathToFile = r'F:\Для загрузки\Готовые принты\Силикон\Чехол iPhone 6 силикон с отк.кам. проз. под карту.xlsx'
# token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
def uplaodImage(token, pathToFile):
    #pathToFile = sys.argv[1:][0].replace('#', ' ')
    df = pandas.DataFrame(pandas.read_excel(pathToFile))
    requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/media/save'
    pool = multiprocessing.Pool(4)
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


def pushPhoto(line, token, requestUrl):
    jsonRequest = {
        "vendorCode": line['Артикул товара'],
        "data": [line['Медиафайлы']]
        }
    headersRequest = {'Authorization': '{}'.format(token), 'X-Vendor-Code': line['Артикул товара']}
    try:
        r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest)  
        print(r.text)
    except requests.ConnectionError:
        r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest) 
        print(r.text)
if __name__ == '__main__':
    uplaodImage(token, pathToFile)
# uplaodImage(token, pathToFile)