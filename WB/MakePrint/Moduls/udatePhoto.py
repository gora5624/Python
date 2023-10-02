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
        # if len(data) ==3:
        #     tmp = [data[-1].replace('2.jpg', '3.jpg'), data[-1].replace('2.jpg', '4.jpg'), data[-1].replace('2.jpg', '5.jpg')]
        #     data.extend(tmp)
        jsonRequest = {
            "vendorCode": line['Артикул поставщика'],
            "data": data
            # "data": line['Медиафайлы'].split(';')
            }
        headersRequest = {'Authorization': '{}'.format(token)}
    try:
        # print(jsonRequest)
        #jsonRequest['data'][0]= jsonRequest['data'][0].replace("/print ","/(Принт ").replace(".jpg",").jpg")
        #print(jsonRequest)
        r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest, timeout=50)  
        r
        #time.sleep(0.6)
        if '"Неверный запрос: по данному артикулу не нашлось карточки товара","additionalErrors' in r.text:
            print('Не нашлось карточки товара '+jsonRequest['vendorCode'])
        if '"Внутренняя ошибка сервиса","additionalErrors' in r.text:
            print('1')
        if '"additionalErrors":null' not in r.text:
            print(r.text + ' ' + jsonRequest['vendorCode'])
        while countTry <5:
            if not checkImage(line['Артикул товара'], token):
                deletPhoto(line['Артикул товара'], token)
                time.sleep(1)
                pushPhoto(line, token, requestUrl)
                time.sleep(5)
            if checkImage(line['Артикул товара'], token):
                break
            else:
                countTry+=1
                continue

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
        urlListCount = len(urlList:=r.json()['data']['cards'][0]['mediaFiles'])
        if urlListCount<0:
            return False
        elif urlListCount==1:
            return complImage(urlList[0])
        else:
            return True
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


def complImage(link):
    refImage1=Image.open(r"\\rab\uploads\1.jpg")
    refImage2=Image.open(r"\\rab\uploads\2.jpg")
    stuffImage = io.BytesIO((r:=requests.get(link)).content)
    stuffImage=Image.open(stuffImage)
    h = ImageChops.difference(refImage1, stuffImage).histogram()
    diff = math.sqrt(functools.reduce(operator.add, map(lambda h, i: h*(i**2), h, range(256))) / (float(refImage1.size[0]) * refImage1.size[1]))
    if diff >1:
        h = ImageChops.difference(refImage2, stuffImage).histogram()
        diff = math.sqrt(functools.reduce(operator.add, map(lambda h, i: h*(i**2), h, range(256))) / (float(refImage2.size[0]) * refImage2.size[1]))
    else:
        return False
    if diff <1:
        return False
    else:
        return True


def updatePhotoMain(pathToFile=None, token=None):
    
    if (pathToFile == None) and (token ==None):
        pathToFile = r"F:\Для загрузки\Готовые принты\Силикон\Чехол Samsung Galaxy M33 5G силикон с зак.кам. проз. под карту.xlsx"
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImUyZTIyZGE1LTYxYWYtNDgyMi1hMDVkLTZiNzVlMTBiNzlmMiJ9.yDq9XasZjs-oB1PapNbD_NWIH8tgWEz_WyKLvVTNgBs'
        # pathToFile = sys.argv[1:][0].replace('#', '
    print(pathToFile)
    df = pandas.DataFrame(pandas.read_excel(pathToFile))
    requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/media/save'
    #if __name__ == '__main__':
    passedTime = 1
    tmp = pandas.DataFrame(pandas.read_excel(r"F:\книжки без фото.xlsx"))['Артикул продавца'].to_list()
    for line in df.to_dict('records'):
        if line['Артикул товара'] in tmp:
            if passedTime > 0.7:
                startTime = time.time()
                pushPhoto(line, token, requestUrl)
                passedTime = time.time() - startTime
            else:
                time.sleep(0.7-passedTime)
                passedTime = 1
    print('Done')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        updatePhotoMain(sys.argv[1:][0].replace('#', ' '), sys.argv[1:][1].replace('#', ' '))
    else:
        updatePhotoMain()
