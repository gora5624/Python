import requests
import pandas
import time
import io
from PIL import Image, ImageChops
import math, operator, functools

# url = re.sub(r'print.+\d\.jpg', number+'.jpg', url ).replace('Готовые принты/Силикон','Вторые картинки')
countReqPMin = 50
delay = 60/countReqPMin
requestUrl = 'https://suppliers-api.wildberries.ru/content/v3/media/save'


def pushPhoto(line, token):
    urlsLsit = line['Медиафайлы'].split(';')
    data = checkUrlsImage(urlsLsit)
    # if len(data) == 0:
    #     print(line['Артикул товара'] + ' нет доступных фото для загрузки')
    #     # return 404
    jsonRequest = {
        "nmId": line['nmID'],
        "data": data
        }
    headersRequest = {'Authorization': '{}'.format(token)}
    r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest, timeout=50)  
    if r.status_code == 429:
        time.sleep(5)
    if r.status_code == 200:
        print(r'Done ' + str(jsonRequest['nmId']))


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


def checkImage(art, token):
    requestUrl = 'https://suppliers-api.wildberries.ru/content/v3/cards/cursor/list'
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
            res = compImage(urlList[0])
            return not res
    except:
        return False


def deletPhoto(nmID, token):
    token = token
    headers = {'Authorization': '{}'.format(token)} 
    url = 'https://suppliers-api.wildberries.ru/content/v3/media/save'
    jsonRequest = {
        "nmId": nmID,
        "data": []
        }
    try:
        r = requests.post(url=url, json=jsonRequest, headers=headers, timeout=10)
        r
    except:
         pass


def compImage(link):
    refImageList = [Image.open(r"\\rab\uploads\1.jpg"), Image.open(r"\\rab\uploads\2.jpg")]
    stuffImage=Image.open(io.BytesIO((r:=requests.get(link)).content))
    for refImage in refImageList:
        h = ImageChops.difference(refImage, stuffImage).histogram()
        diff = math.sqrt(functools.reduce(operator.add, map(lambda h, i: h*(i**2), h, range(256))) / (float(refImage.size[0]) * refImage.size[1]))
        if diff >1:
            continue
        else:
            return True
    return False


def updatePhotoMain(dictToUpload):
    print(dictToUpload['dirName'])
    df = pandas.DataFrame(pandas.read_excel(dictToUpload['listXLSX'][0]))
    token = dictToUpload['token']
    for line in df.to_dict('records'):
            startTime = time.time()
            pushPhoto(line, token)
            time.sleep(max(0, delay - (time.time() - startTime)))
    print('Done')

