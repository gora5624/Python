from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
from wr_csv import write_csv, read_csv
import os
import time


def get_url_image(url_stuff):
    '''Функция собирает все url оригиналов фотографий с конкретной товарной позиции и возвращает список словарей.'''

    driver = webdriver.Chrome(
        executable_path=r'D:\tmp\python\python_parsing\parsing_site\chromedriver.exe')
    driver.get(url_stuff)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    name_stuff = soup.find('h1').text
    name_id = soup.find('div', class_='avatar-view').get('id')
    avatar = '\"' + str(name_id) + '\"'
    xpath = "//*[@id={}]/a/div/picture/img".format(avatar)
    time.sleep(10)
    driver.find_element_by_xpath(xpath).click()
    list_url_image = []
    url_image = ''
    time.sleep(10)
    while True:
        driver.find_element_by_xpath(
            "//*[@id='view-photo-edit-window']/div/div").click()
        soup = BeautifulSoup(driver.page_source, 'lxml')
        url_image = soup.find('div', id='photo-plate').find('img')['src']
        if url_image in list_url_image:
            break
        list_url_image.append(url_image)
    driver.close()
    data = {'name_stuff': name_stuff,
            'list_photo_url': list_url_image}
    return(data)


def get_all_stuff(name_csv_price, catalog_path):
    data = read_csv(name_csv_price)
    list_url_stuff = []
    for line in data:
        list_url_stuff.append(line['url'])
    for url in list_url_stuff:
        data = get_url_image(url)
        path_stuff_photo = os.path.join(
            catalog_path, data['name_stuff'].replace('/', 'sl'))
        os.makedirs(path_stuff_photo)
        print(data['name_stuff'])
        for i, image_url in enumerate(data['list_photo_url']):
            with open(os.path.join(path_stuff_photo, str(i) + '.jpg'), 'wb') as image_file:
                image_file.write(requests.get(
                    'http://' + image_url[2:]).content)


catalog_path = r'D:\tmp\python\python_parsing\parsing_DOKLIKE\DOKLIKE'
name_csv_price = r'D:\tmp\python\python_parsing\parsing_DOKLIKE\price_with_url.csv'


def get_html(url):
    r = requests.get(url)
    return r.text


def get_text_information(name_csv_price, catalog_path):
    data = read_csv(name_csv_price)
    for line in data:
        html = get_html(line['url'])
        soup = BeautifulSoup(html, 'lxml')
        size = soup.find_all('span', class_='nh-select__value')
        for i, j in enumerate(size):
            size[i] = j.text
        try:
            material_text = soup.find(
                'div', class_='product__desc show-for-large user-inner').find_all('p')
        except:
            material_text = ''
        if type(material_text) == list:
            for n, m in enumerate(material_text):
                material_text[n] = m.text
        data_text = {'name_stuff': line['Title'],
                     'url_stuff': line['url'],
                     'size': ','.join(size),
                     'material': ','.join(material_text) if type(material_text) == list else material_text}
        write_csv(data_text, 'DOKLIKE.csv')


get_text_information(name_csv_price, catalog_path)
