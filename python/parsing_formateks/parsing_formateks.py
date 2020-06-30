import requests
from bs4 import BeautifulSoup
from my_lib import write_csv, read_csv, get_html
import os
import time


def get_catalog(utl_in):
    catalog = []
    html = get_html(url_in)
    soup = BeautifulSoup(html, 'lxml')
    catalog_div = sopu.find('div', class_='column-aside',
                            id='aside').find('ul', class_='menu').find_all('li', class_='menu__item')
    for catalog_tmp in catalog_div:
        catalog_url = catalog_tmp.find('a').get('htef')
        catalog_name = catalog_tmp.find('a').text
        data = {'catalog_name': catalog_name,
                'catalog_url': catalog_url}
        catalog.append(data)
    return(catalog)


def max_page():
    pass


def get_stuff_on_page(url_catalog):
    for item in url_catalog:
        for page in range(item['max_page']):
            if page == 0:
                html = get_html(item['url'])
            else:
                html = get_html(item['url'] + '/page-{}'.format(page+1))
            soup = BeautifulSoup(html, 'lxml')
            with open('0.html', 'w', encoding='utf-8') as f:
                f.write(html)
                f.close()

            stuff_div = soup.find(
                'div', class_='catalog-collection cleared').find_all('h3')
            for stuff in stuff_div:
                stuff_url = 'http://formateks.ru' + stuff.find('a').get('href')
                stuff_name = stuff.find('a').text
                data = {'catalog_name': item['catalog_name'],
                        'stuff_name': stuff_name,
                        'stuff_url': stuff_url}
                write_csv(data, 'formarket.csv')


def get_all_stuff(list_stuff):
    list_dir = []
    for stuff in list_stuff:
        html = get_html(stuff['stuff_url'])
        soup = BeautifulSoup(html, 'lxml')
        with open('0.html', 'w', encoding='utf-8') as file:
            file.write(html)
            file.close()
        try:
            descr = soup.find(
                'div', class_='block-text block-type-catalogitem-text textcontent').find('p').text
        except:
            descr = ''
        try:
            url_image = soup.find(
                'div', class_='block-picture').find('a').get('href')
        except:
            continue
        catalog_name = stuff['catalog_name']
        stuff_name = stuff['stuff_name'].replace('"', '')
        stuff_url = stuff['stuff_url']
        data = {'catalog_name': catalog_name,
                'stuff_name': stuff_name,
                'stuff_url': stuff_url,
                'stuff_descr': descr}
        main_dir = r'D:\tmp\python\python_parsing\parsing_formateks'
        new_dir = os.path.join(main_dir, catalog_name,
                               stuff_name).replace(' ', '_').lower()

        if new_dir in list_dir:
            new_dir = new_dir + '_1'
        else:
            list_dir.append(new_dir)
        os.makedirs(new_dir)
        write_csv(data, os.path.join(new_dir, 'info.csv'))
        write_csv(data, os.path.join(main_dir, 'formarket.csv'))
        with open(os.path.join(new_dir, '0.jpg'), 'wb') as file:
            file.write(requests.get(url_image).content)
            file.close()


url_catalog = [
    {'url': 'http://formateks.ru/katalog-uniforma-dlja-personala/dlya-prodavtcov',
     'max_page': 3,
     'catalog_name': 'Одежда для продавцов'},
    {'url': 'http://formateks.ru/katalog-uniforma-dlja-personala/dlya-parikmakherov',
     'max_page': 1,
     'catalog_name': 'Одежда для парикмахеров'}
]
# get_stuff_on_page(url_catalog)
list_stuff = read_csv('formarket.csv')

get_all_stuff(list_stuff)
