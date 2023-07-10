import re
import requests
import multiprocessing
import sys
import pandas
import time
import os

# url = re.sub(r'print.+\d\.jpg', number+'.jpg', url ).replace('Готовые принты/Силикон','Вторые картинки')
def pushPhoto(line, token, requestUrl, countTry=0):
    if 'Артикул товара' in list(line.keys()):
        url = line['Медиафайлы'].split(';')
        data = [url[0]]
        # for i in range(1,6,1):
        #     data.append(re.sub(r'print.+\d\.jpg', str(i)+'.jpg', url ).replace('Готовые принты/Силикон','Вторые картинки'))
        jsonRequest = {
            "vendorCode": line['Артикул товара'],
            #"data": line['Медиафайлы'].split(';')
            "data": data
            }
        headersRequest = {'Authorization': '{}'.format(token)}
    else:
        # data = line['Медиафайлы'].split(';')
        url = line['Медиафайлы'].split(';')
        data = [url[0]]
        # for i in range(1,6,1):
        #     data.append(re.sub(r'print.+\d\.jpg', str(i)+'.jpg', url ).replace('Готовые принты/Силикон','Вторые картинки'))
        if len(data) ==3:
            tmp = [data[-1].replace('2.jpg', '3.jpg'), data[-1].replace('2.jpg', '4.jpg'), data[-1].replace('2.jpg', '5.jpg')]
            data.extend(tmp)
        jsonRequest = {
            "vendorCode": line['Артикул поставщика'],
            "data": data
            # "data": line['Медиафайлы'].split(';')
            }
        headersRequest = {'Authorization': '{}'.format(token)}
    try:
        r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest, timeout=5)  
        r
        time.sleep(1.5)
        if '"Неверный запрос: по данному артикулу не нашлось карточки товара","additionalErrors' in r.text:
            print('Не нашлось карточки товара '+jsonRequest['vendorCode'])
        if '"Внутренняя ошибка сервиса","additionalErrors' in r.text:
            print('1')
        print(r.text + ' ' + jsonRequest['vendorCode'])
    except requests.ConnectionError:
        r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest, timeout=5) 
        print(r.text)
    except requests.exceptions.SSLError:
        print('requests.ReadTimeout')
    except requests.exceptions.ReadTimeout:
        print('requests.ReadTimeout')

    except:
        print('TimeoutError')
    # if requestsVendorCode(line['Артикул товара']) != 0 and countTry < 5:
    #     countTry +=1
    #     pushPhoto(line, token, requestUrl, countTry)


def main():
    print('work')
    pathToFile = sys.argv[1:][0].replace('#', ' ')
    token = sys.argv[1:][1].replace('#', ' ')
    # if __name__ == '__main__':
    # pathToFile = r"F:\Для загрузки\Готовые принты\Силикон\Чехол книга Tecno Pova 2 черный с сил. вставкой Fashion.xlsx"
    # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjgxYjczNGVmLWI2OWUtNGRhMi1iNTBiLThkMTEyYWM4MjhkMCJ9.pU1YOOirgRe3Om-WRYT61AofToggCLbV3na7GbXKGqU'
    # else:
    # pathToFile = sys.argv[1:][0].replace('#', ' ')
    # token = sys.argv[1:][1].replace('#', ' ')
    # pathToFile = sys.argv[1:][0].replace('#', ' ')
    df = pandas.DataFrame(pandas.read_excel(pathToFile))
    requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/media/save'
    if __name__ == '__main__':
        pool = multiprocessing.Pool(4)
        for line in df.to_dict('records'):
            # if ('2098' in line['Артикул товара']) or ('1160' in line['Артикул товара']):
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

if __name__ == '__main__':
    main()
