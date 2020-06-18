import requests
from bs4 import BeautifulSoup
import os
import csv


def get_html(url):
    '''Возвращает HTML код страницы по адресу url'''

    r = requests.get(url)
    return r.text
