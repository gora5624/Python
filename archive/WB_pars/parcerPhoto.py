import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os
import sys
sys.path.insert(1, os.path.abspath(os.path.join(sys.path[0],'../..')))
from my_mod.my_lib import read_xlsx, file_exists
import multiprocessing
import time


url = 'https://www.wildberries.ru/catalog/{}/detail.aspx?targetUrl=XS'
mainDir = r'F:\\'
listForDownloadsName = r'ListPhoto.xlsx'


def get_html(url):
    while True:
        r = requests.get(url, headers={
            'User-Agent': UserAgent().chrome})
        if r.status_code == 200:
            break
        elif r.status_code == 429:
            time.sleep(1)
        elif r.status_code == 404:
            return 0

    return r.text


def getUrlImage(url):
    while True:
        # try:
        html = get_html(url)
        if html == 0:
            return 0, 0
        soup = BeautifulSoup(html, 'lxml')
        mainPhotoUrl = soup.find(
            'img', class_='photo-zoom__preview j-zoom-image hide').get('src')[2:]
        countImage = len(
            soup.find('ul', class_='swiper-wrapper').find_all('li'))
        if len(
                soup.find('ul', class_='swiper-wrapper').find_all('li')) > 1:
            print(url)
        break
        # except:
        # continue
    return mainPhotoUrl, countImage


def downloadImage(imageUrl, art, countImage):
    for i in range(1, countImage+1):
        fullUrl = r'https://' + \
            imageUrl.replace('1.jpg', '{}.jpg'.format(str(i)))
        # try:
        #     os.makedirs(r'F:\image\{}\photo'.format(art))
        # except:
        #     pass
        # with open(r'F:\image\{}\photo\{}.jpg'.format(art, str(i)), 'wb') as file:
        #     count = 0
        while True:
            count += 1
            r1 = requests.get(fullUrl.format(str(i)), headers={
                'User-Agent': UserAgent().chrome})
            #file.write(r1.content)
            if r1.status_code == 200:
                # file.close()
                break
            elif r1.status_code == 429:
                time.sleep(5)
                continue
            elif r1.status_code == 404:
                # file.close()
                break
            elif count > 10:
                print((r1.status_code, imageUrl))
                # file.close()
                break


def getImageFromList():
    pool = multiprocessing.Pool()
    for art_ in read_xlsx(os.path.join(mainDir, listForDownloadsName)):
        art = str(art_['Артикул'])[0:-2]
        folderList = os.listdir(r'F:\image')
        if art in folderList:
            continue
        else:
            pool.apply_async(bodyMain, args=(art,))
    pool.close()
    pool.join()
    # for art_ in read_xlsx(os.path.join(mainDir, listForDownloadsName)):
    #     art = str(art_['Артикул'])[0:-2]
    #     if file_exists(r'E:\image\{}\photo'.format(art)):
    #         continue
    #     else:
    #         if bodyMain(art) == 0:
    #             continue


def bodyMain(art):
    urlCase = url.format(art)
    imageUrl, countImage = getUrlImage(urlCase)
    if imageUrl == 0:
        with open(r'F:\404.txt', 'a', encoding='utf-8') as file:
            file.write(urlCase + '\n')
        return 0
    downloadImage(imageUrl, art, countImage)


if __name__ == '__main__':
    getImageFromList()
