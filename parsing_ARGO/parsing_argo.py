from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
from my_lib import write_csv, read_csv, get_html
import os
import time


def get_information(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    list_catalog = soup.find_all(
        'div', class_='col-md-4 col-sm-6 col-xs-12 redisign-category item')
    list_catalog_url = []
    for catalog in list_catalog:
        url_catalog = catalog.find('a').get('href')
        list_catalog_url.append(url_catalog)
    print('list_catalog_url: ', list_catalog_url)
    for url_catalog in list_catalog_url:
        html = get_html(url + url_catalog)
        soup = BeautifulSoup(html, 'lxml')
        max_page = soup.find(
            'div', class_='col-lg-6 col-xs-12 text-right results').text.split(' ')
        print('url_catalog: ', url_catalog)
        print('max_page: ', max_page)
        for i, page in enumerate(max_page):
            if page == '(всего':
                max_page = int(max_page[i+1])
                print('break')
                break
        for j in range(max_page):
            url_catalog_full = url + url_catalog + '?page={}'.format(j+1)
            html = get_html(url_catalog_full)
            soup = BeautifulSoup(html, 'lxml')
            stuff_on_page_list = soup.find_all(
                'div', class_='product-grid-item col-lg-4 col-md-6 col-sm-6 col-xs-12 display-icon block-button')
            print('stuff_on_page_list: ', stuff_on_page_list)
            for stuff in stuff_on_page_list:
                print('stuff: ', stuff)
                stuff_url = stuff.find('a').get('href')
                html_stuff = get_html(stuff_url)
                soup = BeautifulSoup(html_stuff, 'lxml')
                text_inf = soup.find(
                    'ul', class_='list-unstyled description').find('div', id_='test').find_all('li')
                print('6')
                for n in text_inf:
                    if n.find('span', class_='opts-lab') == 'Размер:':
                        size = n.find('span', class_='opts-val')
                    elif n.find('span', class_='opts-lab') == 'Цвет:':
                        color = n.find('span', class_='opts-val')
                    elif n.find('span', class_='opts-lab') == 'Ткань:':
                        cloth = n.find('span', class_='opts-val')
                    name_stuff = soup.find('h1').text
                    print('7')
                data = {'name_stuff': name_stuff,
                        'url_stuff': stuff_url,
                        'size': size,
                        'color': color,
                        'cloth': cloth}
                write_csv(
                    data, r'D:\tmp\python\python_parsing\parsing_ARGO\ARGO.csv')


url_in = 'https://argo-ivanovo.ru/'
get_information(url_in)
