from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
from my_lib import write_csv, read_csv, get_html
import os
import time


def get_list_catalog_url(url_in):
    html = get_html(url_in)
    soup = BeautifulSoup(html, 'lxml')
    list_catalog_url = soup.find_all(
        'div', class_='col-md-4 col-sm-6 col-xs-12 redisign-category item')
    for j, url in enumerate(list_catalog_url):
        list_catalog_url[j] = url_in + url.find('a').get('href')
    return list_catalog_url


def get_list_stuff_on_pages(list_catalog_url):
    list_stuff = []
    for q, catalog_url in enumerate(list_catalog_url):
        html_catalog = get_html(catalog_url)
        soup = BeautifulSoup(html_catalog, 'lxml')
        text_about_page = soup.find(
            'div', class_='col-lg-6 col-xs-12 text-right results').text.split(' ')
        for i, text in enumerate(text_about_page):
            if text == '(всего':
                max_page = int(text_about_page[i+1])
                break
        list_stuff_div = soup.find_all(
            'div', class_='product-list-item xs-100 sm-100 md-100 lg-100 xl-100')
        category_name = soup.find('h1').text
        for stuff in list_stuff_div:
            url_stuff = stuff.find('h4').find('a').get('href')
            name_stuff = stuff.find('h4').find('a').text
            data_tmp = {'category_name': category_name,
                        'name_stuff': name_stuff,
                        'url_stuff': url_stuff}
            list_stuff.append(data_tmp)
        for page in range(1, max_page):
            url_page = catalog_url + '?page={}'.format(page+1)
            html_page = get_html(url_page)
            soup = BeautifulSoup(html_page, 'lxml')
            list_stuff_div = soup.find_all(
                'div', class_='product-list-item xs-100 sm-100 md-100 lg-100 xl-100')
            for stuff in list_stuff_div:
                url_stuff = stuff.find('h4').find('a').get('href')
                name_stuff = stuff.find('h4').find('a').text
                data_tmp = {'category_name': category_name,
                            'name_stuff': name_stuff,
                            'url_stuff': url_stuff}
                list_stuff.append(data_tmp)
    return list_stuff


def get_stuff_info(list_stuff):
    for stuff in list_stuff:
        url_stuff = stuff['url_stuff']
        html_stuff = get_html(url_stuff)
        soup = BeautifulSoup(html_stuff, 'lxml')
        text_info = soup.find('div', id='test').find_all('li')
        size, color, cloth = '', '', ''
        for text_ in text_info:
            cur_line_name = text_.find('span', class_='opts-lab').text
            cur_line_val = text_.find('span', class_='opts-val').text
            if cur_line_name == 'Размер:':
                size = cur_line_val
            elif cur_line_name == 'Цвет:':
                color = cur_line_val
            elif cur_line_name == 'Ткань:':
                cloth = cur_line_val
        data_stuff = {'category_name': stuff['category_name'],
                      'name_stuff': stuff['name_stuff'],
                      'url_stuff': stuff['url_stuff'],
                      'size': size,
                      'color': color,
                      'cloth': cloth}
        print(data_stuff)
        write_csv(data_stuff, r'D:\tmp\python\python_parsing\parsing_ARGO\argo.csv')


def get_information():
    data = {'name_stuff': name_stuff,
            'url_stuff': stuff_url,
            'size': size,
            'color': color,
            'cloth': cloth}
    driver_new.quit()
    print(data)
    write_csv(
        data, r'D:\tmp\python\python_parsing\parsing_ARGO\ARGO.csv')


url_in = 'https://argo-ivanovo.ru/'
list_catalog_url = get_list_catalog_url(url_in)
list_stuff = get_list_stuff_on_pages(list_catalog_url)
get_stuff_info(list_stuff)
