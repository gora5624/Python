
import requests
from bs4 import BeautifulSoup
from my_lib import write_csv, read_csv, get_html
import os
import time

mainUrl = 'https://helpix.ru'
urlIn = mainUrl + '/devtyp/ebook/'


def ListBrand(urlIn):
    html = get_html(urlIn)
    soup = BeautifulSoup(html, 'lxml')
    brandDiv = soup.find_all(
        'div', class_='b-listli b-listli_big b-listli_u p-listul__listli')
    listBrandTablet = []
    for brand in brandDiv:
        nameBrand = brand.find('a').text
        char = ['\"', '\\', '/']
        for c in char:
            nameBrand = nameBrand.replace(c, '')
        urlBrand = brand.find('a').get('href')
        brandDict = {'nameBrand': nameBrand,
                     'urlBrand': urlBrand}
        listBrandTablet.append(brandDict)
    return listBrandTablet


def ListModel(mainUrl, urlBrand):
    html = get_html(urlBrand)
    soup = BeautifulSoup(html, 'lxml')
    modelSpan = soup.find_all('span', class_='brandphonename')
    listModetTablet = []
    for span in modelSpan:
        nameModel = span.find('a').text
        char = ['\"', '\\', '/']
        for c in char:
            nameModel = nameModel.replace(c, '')
        urlModel = span.find('a').get('href')
        modelDict = {'nameModel': nameModel,
                     'urlModel': urlModel}
        listModetTablet.append(modelDict)
    return listModetTablet


def GetSize(urlModel):
    html = get_html(urlModel)
    soup = BeautifulSoup(html, 'lxml')
    try:
        tab = soup.find(
            'div', class_='b-cut__content helpixcut-content').text.split(",")
    except:
        tab = None
    for el in tab:
        if "\"" in el:
            size = el.strip('\"').strip()
            break
        else:
            size = None
            continue
    return size


def GetData(brand, model, Size, mainUrl):
    dataCsv = {'Brand': brand['nameBrand'],
               'Model': model['nameModel'],
               'Size': Size if Size != None else 'None'}
    write_csv(dataCsv, 'Book.csv')


def main(mainUrl, urlIn):
    listBrand = ListBrand(urlIn)
    for brand in listBrand:
        listModel = ListModel(mainUrl, mainUrl+brand['urlBrand'])
        for model in listModel:
            Size = GetSize(mainUrl+model['urlModel'])
            GetData(brand, model, Size, mainUrl)


main(mainUrl, urlIn)
