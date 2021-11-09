import os
from my_lib import write_csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import requests
from pprint import pprint
UserAgent().chrome


KeyWord = input("Введите поисквый запрос: ")

UrlIn = "https://www.wildberries.ru/catalog/0/search.aspx?search=" + \
    KeyWord.strip().replace(' ', '%20') + "&xsearch=true"

jar = requests.cookies.RequestsCookieJar()
jar.set('___wbu', '925d39a9-f012-4b88-a50f-75ef48e37d7d.1610514476',
        domain='.wildberries.ru', path='/')
jar.set('__catalogOptions', 'Sort%3APopular%26CardSize%3Ac246x328',
        domain='.wildberries.ru', path='/')
jar.set('_gcl_au', '1.1.3184062.1610514478',
        domain='.wildberries.ru', path='/')
jar.set('_gid', 'GA1.2.1232549925.1610514478',
        domain='.wildberries.ru', path='/')
jar.set('_wbauid', '3133292931610514477',
        domain='.wildberries.ru', path='/')
jar.set('stories_uid', '588321610514478028',
        domain='.wildberries.ru', path='/')
jar.set('stories_uid', '588321610514478028',
        domain='.wildberries.ru', path='/')
jar.set('.AspNetCore.Antiforgery.stpccMUKFUM', 'CfDJ8Osu4luNchBNu1VaEQaXOKGlqJc2V9b3enM__yNveoJXAI0da1kQkYxCGYq7-gHLC4woz9Ij2mYdDdG1em8Ry4tYCHYdgch1ZT7VZ9xm066-SrgIXX4SE80CuJ6DqSjJk1XS5P_LPRSGREjctR5thnw',
        domain='.www.wildberries.ru', path='/')
jar.set('BasketUID', 'c3d1a254-6a54-4d7c-bad8-05e468b615e4',
        domain='.www.wildberries.ru', path='/')
jar.set('_pk_id.1.034e', '42a598f1275aabb4.1610514479.3.1610529180.1610527181.',
        domain='.www.wildberries.ru', path='/')
jar.set('_wbSes', 'CfDJ8Osu4luNchBNu1VaEQaXOKEV327Uh2qfIrcYw5mByFReF2m4YfxFSkWhbynnda6ORaRxpOZDAoniXo%2BTZ2wVyodytgaDItyTYcpExVuCNouOkqqW8Y9K4ZWZTDyzzmI4U8PJc4lOdGBIzb%2Fkw38rroAADUR0bcZTyfFwUEv36W2b',
        domain='.www.wildberries.ru', path='/')
jar.set('route', '161a359f8bfea0a6884ef97b597f5d145bb5819a',
        domain='.www.wildberries.ru', path='/')


def get_html(url, jar, t=0):
    time.sleep(t)
    r = requests.Session()
    r.cookies.update(jar)
    r = requests.get(url, cookies=jar, headers={
                     'User-Agent': UserAgent().chrome})
    return r.text


def PaginationExist(soup):
    pagination = soup.find('div', class_='pageToInsert').find(
        'a', class_='pagination-next')
    if pagination == None:
        NextPage = False
    else:
        NextPage = True
    return NextPage


def GetData(url):
    html = get_html(url, jar)
    soup = BeautifulSoup(html, 'lxml')
    Name = soup.find(
        'div', class_='brand-and-name j-product-title').find('span', class_='name').text
    Art = soup.find(
        'div', class_='second-horizontal').find('span', class_='j-article').text
    Price = soup.find('div', class_='j-price order-block').find('span',
                                                                class_='final-cost').text.strip().replace('\xa0', ' ')
    Orders = soup.find(
        'div', class_='second-horizontal').find_all('p')
    data = {'Name': Name,
            'Art': Art,
            'Price': Price,
            'Orders': Orders}
    print(data)


def Slow(UrlIn):
    NextPage = True
    while NextPage:
        html = get_html(UrlIn, jar)
        soup = BeautifulSoup(html, 'lxml')
        StuffList = soup.find_all(
            'a', class_='ref_goods_n_p j-open-full-product-card')
        UrlListOnPage = []
        for a in StuffList:
            UrlListOnPage.append('https://www.wildberries.ru' + a.get('href'))
        for url in UrlListOnPage:
            GetData(url)
        NextPage = False


Slow(UrlIn)
