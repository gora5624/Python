from bs4 import BeautifulSoup
from my_lib import requests, read_xlsx
import os

urlIn = r'https://www.wildberries.ru/brands/mobi711'


def get_html(url):
    r = requests.get(url)
    return r.text


def getData(Url):
    html = get_html(Url)
    soup = BeautifulSoup(html, 'lxml')
    priceStuff =
    urlStuff =
    idStuff =
    urlImageStuff =
