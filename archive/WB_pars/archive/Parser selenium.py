import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, '..\..\..\..')))
from my_mod.my_lib import write_csv
from bs4 import BeautifulSoup
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def get_html(url, t=0):
    time.sleep(t)

    r = requests.get(url)
    return r.text


def PaginationExist(soup):
    pagination = soup.find('div', class_='pageToInsert pagination__wrapper').find(
        'a', class_='pagination-next')
    if pagination == None:
        NextPage = False
    else:
        NextPage = True
    return NextPage


def Slow(UrlIn, File_name):
    NextPage = True
    while NextPage:
        html = get_html(UrlIn)
        soup = BeautifulSoup(html, 'lxml')
        StuffList = soup.find_all(
            'a', class_='ref_goods_n_p j-open-full-product-card')
        UrlListOnPage = []
        for a in StuffList:
            UrlListOnPage.append('https://www.wildberries.ru' + a.get('href'))
        for url in UrlListOnPage:
            GetData(url, File_name)
        NextPage = PaginationExist(soup)
        if NextPage:
            UrlIn = 'https://www.wildberries.ru' + soup.find('div', class_='pageToInsert').find(
                'a', class_='pagination-next').get('href')


def GetData(url, File_name):

    try:
        driver = webdriver.Chrome(
            executable_path=r'D:\tmp\my_prod\Python\python\WB_pars\chromedriver.exe')
    except:
        driver = webdriver.Chrome(
            executable_path=r'D:\tmp\my_prod\Python\python\WB_pars\chromedriver.exe')
    driver.get(url)
    time.sleep(0)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    try:
        Name = soup.find(
            'div', class_='brand-and-name j-product-title').find('span', class_='name').text
    except AttributeError:
        Name = None
    try:
        Art = soup.find(
            'div', class_='article').find('span').text
    except AttributeError:
        Art = None
    try:
        Price = soup.find('div', class_='final-price-block').find('span',
                                                                  class_='final-cost').text.strip().replace('\xa0', ' ')
    except AttributeError:
        Price = None
    try:
        Orders = soup.find(
            'p', class_='order-quantity j-orders-count-wrapper').find('span').text
    except AttributeError:
        Orders = None

    data = {'Name': Name,
            'Art': Art,
            'Price': Price,
            'Orders': Orders}
    write_csv(data, r'D:\\' + File_name + '.csv')
    driver.close()


Find = ['чехол samsung s20FE', 'чехол samsung s20 FE', 'чехол samsung s 20 FE']

for word in Find:
    File_name = KeyWord = word
    UrlIn = "https://www.wildberries.ru/catalog/0/search.aspx?search=" + \
        KeyWord.strip().replace(' ', '%20') + "&xsearch=true"
    Slow(UrlIn, File_name)
    print(File_name + ' Done')
