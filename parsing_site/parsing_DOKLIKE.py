import requests
from bs4 import BeautifulSoup
import os
import csv


def write_csv(data, name_file='new_csv.csv', separator=';'):
    with open(name_file, 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(
            f, fieldnames=data.keys(), delimiter=separator)
        writer.writerow(data)


def get_html(url):
    '''Возвращает HTML код страницы по адресу url'''

    r = requests.get(url)
    return r.text


def get_list_main_category(html, url_main):
    '''Возвращаем список словарей с названием главных категорий и их url для последующего парсинга из них товаров.'''

    soup = BeautifulSoup(html, 'lxml')  # Парсим HTML  код страницы

    # Находим все div с нужным классом, который привязявн к категориям
    list_all_main_category = soup.find_all('div', class_='category-item__link')
    # Создаём пустой список для наполенния его словарями, содержащими название категорий и их url
    list_dict_main_category = []
    for main_category in list_all_main_category:
        # Достаём из div текст, который является названием категории
        name_category = main_category.find('a').text
        # Достаём из div url, и из переделываем его из относительнго в абсолютный
        url_category = url_main + main_category.find('a').get('href')
        dict_main_category = {'name_category': name_category,
                              'url_category': url_category}  # Упаковываем в словарь название и url
        # Упаковываем словари с список словарей
        list_dict_main_category.append(dict_main_category)
    return (list_dict_main_category)


def get_list_item(html, url_main):
    '''Возвращает список словарей с названиями моделей, их url и названиями категорий, к ктоторым они принадлежат для последующегог парсинга информации из них.'''

    # Получаем список категорий которые есть на сайте
    list_main_category = get_list_main_category(html, url_main)
    list_dict_item = []
    for main_category in list_main_category:  # Проходим по всем категориям
        html = get_html(main_category['url_category'])
        soup = BeautifulSoup(html, 'lxml')
        try:  # В некоторых категориях несколько страниц, в некоторых только одна. Если страница одна, то блога pagination нет, отлавливаем эту ошибку, чтобы знать сколько парсить страниц
            pages = int(
                len(soup.find('div', class_='pagination__pages').findChildren('a')))  # Пытаемся найти блок pagination
        except AttributeError:  # Если его нет, то отлавливаем исключение, щадаём количество страниц и идём дальше
            pages = 0
          # Создаём пустой список для заполнения товарами с сайта
        if pages > 0:  # Если страниц несколько, то идём сюда
            for page in range(pages+1):
                html_page = get_html(
                    main_category['url_category'] + '?page={}'.format(page + 1))  # Получаем HTML код страницы, с учётом количества страниц подставляя нужную цифру методом format на каджой итерации цинкла for
                soup_page = BeautifulSoup(html_page, 'lxml')
                list_item_on_page = soup_page.find_all(
                    'div', class_='product-item__link')  # Находит все товары на текущей странице и составляем список
                for item in list_item_on_page:  # Разворачиваем список и проходимся по всем элементам
                    # Получем текст из блока с товаром - это название товара
                    name_item = item.find('a').text
                    url_item = item.find('a').get(
                        'href')  # Получаем url товара
                    dict_item = {'name_item': name_item,
                                 'url_item': url_item}  # Создаем словарь с названием товара, его url и названием его категории
                    # Добаляем словари в список
                    list_dict_item.append(dict_item)
        else:  # Если только одна страница - идём сюда, и всё аналогично
            html_page = get_html(
                main_category['url_category'])
            soup_page = BeautifulSoup(html_page, 'lxml')
            list_item_on_page = soup_page.find_all(
                'div', class_='product-item__link')
            for item in list_item_on_page:
                name_item = item.find('a').text
                url_item = item.find('a').get('href')
                dict_item = {'name_item': name_item,
                             'url_item': url_item}
                list_dict_item.append(dict_item)
    for item in list_dict_item:
        write_csv(item)


url_main = 'https://odetdoctora.ru'  # Указывем адрес самого сайта
# Указываем адрес страницы входа относительно адреса сайта
url_in = url_main + '/products'
html = get_html(url_in)  # Получаем HTML код страницы входа и начинаем работу
get_list_item(html, url_main)
