import requests
import sys
import pandas
import time
import io
from PIL import Image, ImageChops
import math, operator, functools

# url = re.sub(r'print.+\d\.jpg', number+'.jpg', url ).replace('Готовые принты/Силикон','Вторые картинки')
countReqPMin = 100
delay = 60/countReqPMin
def pushPhoto(line, token, requestUrl, countTry=0):
    
    urlsLsit = line['Медиафайлы'].split(';')
    data = checkUrlsImage(urlsLsit)
    # data = [urlsLsit[0]]
    if len(data) == 0:
        print(line['Артикул товара'] + ' нет доступных фото для загрузки')
        return 404
    jsonRequest = {
        "vendorCode": line['Артикул товара'] if 'Артикул товара' in list(line.keys()) else line['Артикул поставщика'],
        #"data": line['Медиафайлы'].split(';')
        "data": data
        }
    headersRequest = {'Authorization': '{}'.format(token)}
    try:
        # print(jsonRequest)
        #jsonRequest['data'][0]= jsonRequest['data'][0].replace("/print ","/(Принт ").replace(".jpg",").jpg")
        #print(jsonRequest)
        r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest, timeout=50)  
        if r.status_code == 200:
            pass
            # print(r.text)
        #time.sleep(0.6)
        if '"Неверный запрос: по данному артикулу не нашлось карточки товара","additionalErrors' in r.text:
            print('Не нашлось карточки товара '+jsonRequest['vendorCode'])
        if '"Внутренняя ошибка сервиса","additionalErrors' in r.text:
            print('1')
        if '"additionalErrors":null' not in r.text:
            print(r.text + ' ' + jsonRequest['vendorCode'])
        # time.sleep(1.2)
        while not checkImage(line['Артикул товара'], token, urlsLsit) and countTry <5:
            deletPhoto(line['Артикул товара'], token)
            time.sleep(1)
            pushPhoto(line, token, requestUrl)
            time.sleep(5)
            countTry +=1
        if countTry == 5:
            print(line['Артикул товара'] + ' хз что с фото, надо проверить')

    except requests.ConnectionError:
        r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest, timeout=50) 
        print(r.text + jsonRequest['vendorCode'])
    except requests.exceptions.ReadTimeout:
        print('requests.ReadTimeout'  + jsonRequest['vendorCode'])

    except:
        print('TimeoutError')
    # if requestsVendorCode(line['Артикул товара']) != 0 and countTry < 5:
    #     countTry +=1
    #     pushPhoto(line, token, requestUrl, countTry)


def checkUrlsImage(urlList):
    urlListChecked = []
    for url in urlList:
        if requests.get(url).status_code == 200:
            urlListChecked.append(url)
            continue
        elif requests.get(url.replace('.jpg', '.png')).status_code == 200:
            urlListChecked.append(url.replace('.jpg', '.png'))
            continue
        if 'Силикон' not in url:
            url = url.replace('Вторые картинки', 'Вторые картинки/Силикон')
            if requests.get(url).status_code == 200:
                urlListChecked.append(url)
                continue
            elif requests.get(url.replace('.jpg', '.png')).status_code == 200:
                urlListChecked.append(url.replace('.jpg', '.png'))
                continue
    return urlListChecked# [i for i in urlList if requests.get(i).status_code==200]


def checkImage(art, token, refImageList):
    # time.sleep(0.6)
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
    try:
        r = requests.post(url=requestUrl, json=json, headers=headersRequest)
        urlList = r.json()['data']['cards'][0]['mediaFiles']
        urlListCount = len(urlList)
        if urlListCount<1:
            return False
        else:
            res = compImage(refImageList[0])
            return not res
    except:
        return False


def deletPhoto(vendorCode, token):
    token = token
    headers = {'Authorization': '{}'.format(token)} 
    url = 'https://suppliers-api.wildberries.ru/content/v1/media/save'
    json = {
    "vendorCode": vendorCode,
    "data": [
    ]
    }
    try:
        r = requests.post(url=url, json=json, headers=headers, timeout=10)
    except:
         pass


def compImage(link, refImageList):
    refImageList = [Image.open(refImageList[0])]#, Image.open(r"\\rab\uploads\2.jpg")]
    # refImage1=Image.open(r"\\rab\uploads\1.jpg")
    # refImage2=Image.open(r"\\rab\uploads\2.jpg")
    stuffImage=Image.open(io.BytesIO((r:=requests.get(link)).content))
    for refImage in refImageList:
        h = ImageChops.difference(refImage, stuffImage).histogram()
        diff = math.sqrt(functools.reduce(operator.add, map(lambda h, i: h*(i**2), h, range(256))) / (float(refImage.size[0]) * refImage.size[1]))
        if diff >1:
            return False
            # continue
        else:
            continue
    return True
    #     h = ImageChops.difference(refImage2, stuffImage).histogram()
    #     diff = math.sqrt(functools.reduce(operator.add, map(lambda h, i: h*(i**2), h, range(256))) / (float(refImage2.size[0]) * refImage2.size[1]))
    #     if diff > 1:
    #         return False
    #     else:
    #         return True
    # else:
    #     return True


def updatePhotoMain(pathToFile=None, token=None):
    
    if (pathToFile == None) and (token ==None):
        pathToFile = r"F:\Для загрузки\Готовые принты\Чехол Samsung Galaxy M33 5G силикон с зак.кам. проз. под карту.xlsx"
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImUyZTIyZGE1LTYxYWYtNDgyMi1hMDVkLTZiNzVlMTBiNzlmMiJ9.yDq9XasZjs-oB1PapNbD_NWIH8tgWEz_WyKLvVTNgBs'
        # pathToFile = sys.argv[1:][0].replace('#', '
    print(pathToFile)
    df = pandas.DataFrame(pandas.read_excel(pathToFile))
    requestUrl = 'https://suppliers-api.wildberries.ru/content/v2/media/save'
    #if __name__ == '__main__':
    passedTime = 1.5
    # tmp = pandas.DataFrame(pandas.read_excel(r"F:\книжки без фото.xlsx"))['Артикул продавца'].to_list()
    for line in df.to_dict('records'):
        # if line['Артикул товара'] in tmp:
            if not checkImage(line['Артикул товара'], token, line['Медиафайлы'].split(';')):
                if passedTime > 1.2:
                    startTime = time.time()
                    pushPhoto(line, token, requestUrl)
                    passedTime = time.time() - startTime
                else:
                    time.sleep(1.2-passedTime)
                    passedTime = 1.5
    print('Done')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        updatePhotoMain(sys.argv[1:][0].replace('#', ' '), sys.argv[1:][1].replace('#', ' '))
    else:
        updatePhotoMain()
