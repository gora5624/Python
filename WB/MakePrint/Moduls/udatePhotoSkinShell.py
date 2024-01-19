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
    # print(printNum)
    for i in namePrintsImage:
        urls.append(mainPartUrl+printNum+'.'+i)
        #print(urls)
    return urls
    #print(mainPartUrl)



# url = re.sub(r'print.+\d\.jpg', number+'.jpg', url ).replace('Готовые принты/Силикон','Вторые картинки')
def pushPhoto(line, token, requestUrl, countTry=0):
    data = makeUrls(line['Медиафайлы'].split(';')[0], line['Принт'])
    # print(data)
    # print(line['Артикул товара'])
    jsonRequest = {
        "vendorCode": line['Артикул товара'],
        "data": data
        }
    headersRequest = {'Authorization': '{}'.format(token)}
    try:
        r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest, timeout=50)
        if r.status_code ==400:
            print('Проверь ссылки {}'.format(';'.join(data)))
        r
        time.sleep(0.7)
        if '"Неверный запрос: по данному артикулу не нашлось карточки товара","additionalErrors' in r.text:
            print('Не нашлось карточки товара '+jsonRequest['vendorCode'])
        if '"Внутренняя ошибка сервиса","additionalErrors' in r.text:
            print('1')
        if 'не удалось' in r.text.lower():
            pass
            #print(r.text + ' ' + jsonRequest['vendorCode'])
        else:
            pass
    except requests.ConnectionError:
        r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest, timeout=5) 
        print(r.text)
    except requests.exceptions.SSLError:
        print('requests.ReadTimeout')
    except requests.exceptions.ReadTimeout:

        print('requests.ReadTimeout'+ ' ' + jsonRequest['vendorCode'])

    except:
        print('TimeoutError')

def checkImage(art, token):
    time.sleep(0.6)
    requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/cards/cursor/list'
    headersRequest = {'Authorization': '{}'.format(token)}
    json = {
            "sort": {
                "cursor": {
                "limit": 1
                },
                "filter": {
                "textSearch": str(art),
                "withPhoto": -1,
                "allowedCategoriesOnly": True
                }
            }
            }
    r = requests.post(url=requestUrl, json=json, headers=headersRequest)
    try:
        urlListCount = len(r.json()['data']['cards'][0]['mediaFiles'])
        if urlListCount==6:
            return True
        else:
            return False
    except:
        return False

    
    pass


def udatePhotoSkinShellMain(path, token):
    print(path)
    pathToFile = path#sys.argv[1:][0].replace('#', ' ')
    token = token# sys.argv[1:][1].replace('#', ' ')
    # pathToFile = r"F:\Для загрузки\Готовые принты\Силикон\Чехол Honor X8a силикон с зак.кам. черный противоуд. SkinShell.xlsx"
    # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImU4NjQ1YWI5LWFjM2UtNGFkOS1hYmIyLThkMTMzMGM1YTU3NyJ9.8nz9gIHurlCVKIhruG6hY8MRBtMLvLYggVzisxgKivY'
    df = pandas.DataFrame(pandas.read_excel(pathToFile))
    requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/media/save'
    #if __name__ == '__main__':
    pool = multiprocessing.Pool(2)
    for line in df.to_dict('records'):
        #if not checkImage(line['Баркод товара'],token):
        pushPhoto(line, token, requestUrl,)
    #         pool.apply_async(pushPhoto, args=(line, token, requestUrl,))
    # pool.close()
    # pool.join()

# if __name__ == '__main__':
    # udatePhotoSkinShellMain()
    #makeUrls(r'http://95.78.233.163:8001/wp-content/uploads/Готовые принты/Силикон/Чехол Honor 10i (Honor 20E) силикон с отк.кам. черный противоуд. SkinShell/(Принт 4213).jpg', '(Принт 4200)')
