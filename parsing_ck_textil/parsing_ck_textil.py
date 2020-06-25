import requests
from bs4 import BeautifulSoup
from my_lib import write_csv, read_csv, get_html
import os
import time


def get_catalog_url(url_in):
    html = get_html(url_in)
    soup = BeautifulSoup(html, 'lxml')
    url_list_ul = soup.find('ul', class_='nav navbar-nav').find_all('li')
    catalog = []
    for url in url_list_ul:
        catalog_name = url.find('a').text
        catalog_url = url.find('a').get('href')
        catalog_dict = {'catalog_name': catalog_name,
                        'catalog_url': catalog_url}
        catalog.append(catalog_dict)
    return catalog


def get_max_page(url_page='', html=''):
    if not url_page == '':
        html_new = get_html(url_page)
    elif not html == '':
        html_new = html
    soup = BeautifulSoup(html_new, 'lxml')
    pagination = soup.find('div', class_='pagination_wrap row').text.split(' ')
    for i, page in enumerate(pagination):
        if page == '(всего':
            max_page = int(pagination[i+1])
            break
    return max_page


def get_stuff_on_page(page_catalog_url):
    list_stuff_on_page = []
    html = get_html(page_catalog_url)
    soup = BeautifulSoup(html, 'lxml')
    list_stuff = soup.find_all('div', class_='product-thumb transition')
    catalog_name = soup.find('h1').text
    for stuff in list_stuff:
        url = stuff.find('div', class_='caption').find('a').get('href')
        stuff_name = stuff.find(
            'div', class_='caption').find('a').text.replace('"', '')
        data = {'catalog_name': catalog_name,
                'stuff_name': stuff_name,
                'stuff_url': url}
        list_stuff_on_page.append(data)
        write_csv(data, 'ck.csv')
    return list_stuff_on_page


def get_stuff_url(url_in):
    list_stuff_on_site = []
    catalog = get_catalog_url(url_in)
    for category in catalog:
        max_page = get_max_page(category['catalog_url'])
        for page in range(1, max_page+1):
            stuff_on_page = get_stuff_on_page(
                category['catalog_url'] + '?page={}'.format(page))
            list_stuff_on_site.extend(stuff_on_page)
    return list_stuff_on_site


def get_stuff_info(list_stuff_on_site):
    for stuff in list_stuff_on_site:
        html = get_html(stuff['stuff_url'])
        with open('0.html', 'w', encoding='utf-8') as f:
            f.write(html)
            f.close()
        soup = BeautifulSoup(html, 'lxml')
        try:
            descr = soup.find('div', id='tab-description').text
        except AttributeError:
            descr = ''
        try:
            atr = soup.find(
                'div', id='tab-specification').find('div', class_='attribute').text
        except AttributeError:
            atr = ''
        try:
            size_span = soup.find('div', class_='option row').find(
                'tbody').find_all('span', class_='size-title')
        except AttributeError:
            size_span = []
        size_span = soup.find('div', class_='option row').find(
            'tbody').find_all('span', class_='size-title')
        size = []
        for size_tmp in size_span:
            size.append(size_tmp.text)
            ','.join(size)
        data = {'catalog_name': stuff['catalog_name'],
                'stuff_name': stuff['stuff_name'],
                'stuff_url': stuff['stuff_url'],
                'descr': descr.replace('\n', ' ').replace('\r', ' '),
                'size': size,
                'atr': atr.replace('\n', ' ').replace('\r', ' ')}
        main_dir = r'D:\tmp\python\python_parsing\parsing_ck_textil'
        write_csv(
            data, r'D:\tmp\python\python_parsing\parsing_ck_textil\ck_textil.csv')
        try:
            image_tag_a_list = soup.find(
                'div', class_='MagicToolboxSelectorsContainer').find_all('a')
        except AttributeError:
            image_tag_a_list = soup.find(
                'div', class_='MagicToolboxContainer selectorsBottom minWidth').find_all('a')
        image_dir = os.path.join(
            main_dir, stuff['catalog_name'], stuff['stuff_name']).replace(' ', '_')
        os.makedirs(image_dir)
        for i, image_tmp in enumerate(image_tag_a_list):
            image_tmp.get('href')
            image_url = 'https://' + image_tmp.get('href')[2:]
            with open(os.path.join(image_dir, '{}.jpg'.format(i)), 'wb') as file:
                file.write(requests.get(image_url).content)
        write_csv(data, os.path.join(image_dir, 'info.csv'))


url_in = 'https://ck-textil.ru/'
#list_stuff_on_site = get_stuff_url(url_in)
list_stuff_on_site = read_csv('ck.csv')
get_stuff_info(list_stuff_on_site)
