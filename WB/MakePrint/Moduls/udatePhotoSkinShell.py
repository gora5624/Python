import re
import requests
import multiprocessing
import sys
import pandas
import time
import os


def makeUrls(oldUrl, printName):
    urls = []
    namePrintsImage = ['1.png','2.png','3.png','4.png','6.png','7.png']
    mainPartUrl = re.sub(r"\(Принт .*\).jpg",'',oldUrl)
    printNum = printName.replace('(Принт ','').replace(')','')
    print(printNum)
    for i in namePrintsImage:
        urls.append(mainPartUrl+printNum+'.'+i)
        #print(urls)
    return urls
    #print(mainPartUrl)



# url = re.sub(r'print.+\d\.jpg', number+'.jpg', url ).replace('Готовые принты/Силикон','Вторые картинки')
def pushPhoto(line, token, requestUrl, countTry=0):
    data = makeUrls(line['Медиафайлы'].split(';')[0], line['Принт'])
    jsonRequest = {
        "vendorCode": line['Артикул товара'],
        "data": data
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


def main():
    print('work')
    pathToFile = sys.argv[1:][0].replace('#', ' ')
    token = sys.argv[1:][1].replace('#', ' ')
    df = pandas.DataFrame(pandas.read_excel(pathToFile))
    requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/media/save'
    if __name__ == '__main__':
        pool = multiprocessing.Pool(4)
        for line in df.to_dict('records'):
                pool.apply_async(pushPhoto, args=(line, token, requestUrl,))
        pool.close()
        pool.join()

if __name__ == '__main__':
    main()
    #makeUrls(r'http://95.78.233.163:8001/wp-content/uploads/Готовые принты/Силикон/Чехол Honor 10i (Honor 20E) силикон с отк.кам. черный противоуд. SkinShell/(Принт 4213).jpg', '(Принт 4200)')
