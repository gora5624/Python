import requests
import pandas
import time
import io
import logging
import math, operator, functools

from PIL import Image, ImageChops

from telegramNotifications import send_message

logger = logging.getLogger(__name__)
# url = re.sub(r'print.+\d\.jpg', number+'.jpg', url ).replace('Готовые принты/Силикон','Вторые картинки')
countReqPMin = 50
delay = 60/countReqPMin
requestUrl = 'https://suppliers-api.wildberries.ru/content/v3/media/save'


def pushPhoto(line, token):
    urlsLsit = line['Медиафайлы'].split(';')
    data = checkUrlsImage(urlsLsit)
    if not data:  # Если нет допустимых URLs, выходим
        logger.warning(f"{line['Артикул товара']} нет доступных фото для загрузки")
        send_message(f"{line['Артикул товара']} нет доступных фото для загрузки")
        # print(f"{line['Артикул товара']} нет доступных фото для загрузки")
        return
    logger.info(f"Starting photo upload for {line['nmID']}")
    jsonRequest = {
        "nmId": line['nmID'],
        "data": data
    }
    headersRequest = {'Authorization': '{}'.format(token)}
    
    with requests.Session() as session:
        try:
            r = session.post(requestUrl, json=jsonRequest, headers=headersRequest, timeout=50)  
            if r.status_code == 429:
                logger.warning("Rate limited by server, retrying in 5 seconds")
                time.sleep(5)
            if r.status_code == 200:
                logger.info(f"Upload successful for {jsonRequest['nmId']}")
            else:
                error_msg = f"Failed to upload for {line['nmID']} status code: {r.status_code}"
                logger.warning(error_msg)
        except Exception as e:
            logger.error(f"Error uploading photo for {line['nmID']}: {e}")
            send_message(f"Error uploading photo for {line['nmID']}: {e}")


def checkUrlsImage(urlList):
    urlListChecked = []
    
    with requests.Session() as session:
        for url in urlList:
            try:
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
            except Exception as e:
                logger.error(f"Error checking URL {url}: {e}")
                send_message(f"Error checking URL {url}: {e}")
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
        r = requests.post(url=url, json=jsonRequest, headers=headers, timeout=10)
        if r.status_code == 200:
            logger.info(f"Successfully deleted photo for {nmID}")
        else:
            logger.warning(f"Failed to delete photo for {nmID} with status code {r.status_code}")
    except Exception as e:
        logger.error(f"Error deleting photo for {nmID}: {e}")


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


def updatePhotoMain(dictToUpload,):
    logger.info(f"Starting photo update for {dictToUpload['dirName']}")
    dirName=dictToUpload['dirName']
    df = pandas.DataFrame(pandas.read_excel(dictToUpload['listXLSX'][0]))
    token = dictToUpload['token']
    print(f'Файл {dirName} найден, начал загрузку')
    for line in df.to_dict('records'):
        startTime = time.time()
        pushPhoto(line, token)
        time.sleep(max(0, delay - (time.time() - startTime)))
        # logger.debug(f"Processing time: {time.time() - startTime} seconds")
    logger.info('Photo update completed')

