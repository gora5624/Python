import requests
from bs4 import BeautifulSoup
from my_lib import write_csv, read_csv, get_html
import os
import time


def get_image(price):
    price_argo = read_csv(price)
    list_image_dir = []
    i = 1
    for stuff in price_argo:
        html = get_html(stuff['url_stuff'])
        soup = BeautifulSoup(html, 'lxml')
        try:
            image_list = soup.find(
                'div', id='product-gallery').find_all('a')
        except:
            image_list = soup.find('div', class_='image-border').find_all('a')
        image_list_url = []
        for image in image_list:
            url_image = image.get('href')
            if url_image in image_list_url:
                break
            image_list_url.append(url_image)
        dir_for_image = os.path.join(
            r'D:\tmp\python\python_parsing\parsing_ARGO', 'image', stuff['category_name'], stuff['name_stuff']).replace(' ', '_').replace('"', '')
        while dir_for_image in list_image_dir:
            dir_for_image = dir_for_image + '_' + str(i)
            i += 1
        os.makedirs(dir_for_image)
        list_image_dir.append(dir_for_image)
        for i, image in enumerate(image_list_url):
            if image == '':
                continue
            with open(os.path.join(dir_for_image, '{}.jpg'.format(i)), 'wb') as image_file:
                image_file.write(requests.get(image).content)
        write_csv(stuff, dir_for_image + '\info.csv')


price = r'D:\tmp\python\python_parsing\parsing_ARGO\argo.csv'
get_image(price)

'''
html = get_html(
    'https://argo-ivanovo.ru/golovnye-ubory/pilotka-dlja-prodavtsa-tkan-nejlon-100-poliefir')
soup = BeautifulSoup(html, 'lxml')
with open('0.html', 'w', encoding='utf-8') as f:
    f.write(html)
'''
