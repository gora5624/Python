import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
from os.path import basename
import csv


def get_html(url):
    '''Возвращает HTML код страницы по адресу url'''

    r = requests.get(url)
    return r.text


def get_information(url):
    with open('index.html', 'r') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'lxml')
        list_photo_on_page = soup.find('div', class_='photos_container').find_all(
            'a')
        list_photo_url = []
        for photo in list_photo_on_page:
            url_photo = photo.get('href')
            list_photo_url.append(url_photo)
        for url in list_photo_url:
            html = get_html(url)
            driver = webdriver.Chrome(
                executable_path=r'D:\tmp\python\python_parsing\chromedriver.exe')
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            url_image = soup.find(
                'div', id='pv_tag_frame').find('img')['src']
            print('this is print', url_image)
            with open('1.jpg', 'wb') as f:
                f.write(requests.get(url_image).content)
            driver.quit()


url = ''
get_information(url)
