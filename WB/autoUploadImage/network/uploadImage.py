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
    if not data:  # Если нет допустимых URLs, выходим
        print(f"{line['Артикул товара']} нет доступных фото для загрузки")
        return

    jsonRequest = {
        "nmId": line['nmID'],
        "data": data
    }
    headersRequest = {'Authorization': '{}'.format(token)}
    
    with requests.Session() as session:
        r = session.post(requestUrl, json=jsonRequest, headers=headersRequest, timeout=50)  
        if r.status_code == 429:
            time.sleep(5)
        if r.status_code == 200:
            print(f"Done {jsonRequest['nmId']}")


def checkUrlsImage(urlList):
    urlListChecked = []
    
    with requests.Session() as session:
        for url in urlList:
            if session.get(url).status_code == 200:
                urlListChecked.append(url)
            elif session.get(url.replace('.jpg', '.png')).status_code == 200:
                urlListChecked.append(url.replace('.jpg', '.png'))
            else:
                silicone_url = url.replace('Вторые картинки', 'Вторые картинки/Силикон')
                if session.get(silicone_url).status_code == 200:
                    urlListChecked.append(silicone_url)
                elif session.get(silicone_url.replace('.jpg', '.png')).status_code == 200:
                    urlListChecked.append(silicone_url.replace('.jpg', '.png'))
    return urlListChecked


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
        return len(urlList) > 0 and not compImage(urlList[0])
    except Exception as e:
        print(f"Error checking image: {e}")
        return False
    

def deletPhoto(nmID, token):
    headers = {'Authorization': '{}'.format(token)} 
    url = 'https://suppliers-api.wildberries.ru/content/v3/media/save'
    jsonRequest = {"nmId": nmID, "data": []}
    try:
        requests.post(url=url, json=jsonRequest, headers=headers, timeout=10)
    except Exception as e:
        print(f"Error deleting photo: {e}")


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

