
import requests
from bs4 import BeautifulSoup
from my_lib import write_csv, read_csv, get_html
import os
import time

mainUrl = 'https://helpix.ru'
urlIn = mainUrl + '/devtyp/pad/'


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


def GetImg(urlModel):
    html = get_html(urlModel)
    soup = BeautifulSoup(html, 'lxml')
    try:
        urlImg = soup.find('img', class_='b-devPic__picNew').get('src')
        nameImg = soup.find('img', class_='b-devPic__picNew').get('alt')
        size = soup.find(
            'tb', class_='b-specTabShort__td b-specTabShort__td_value').text().split("\"")[0]
        char = ['\"', '\\', '/']
        for c in char:
            nameImg = nameImg.replace(c, '')
    except:
        urlImg = None
        nameImg = None

    imgDict = {'urlImg': urlImg,
               'nameImg': nameImg}
    return imgDict


def GetData(brand, model, img, mainUrl):
    dataCsv = {'Brand': brand['nameBrand'],
               'Model': model['nameModel'],
               'Img Directory': brand['nameBrand']+'\\'+model['nameModel']+'\\'+img['nameImg']+'.jpg' if img['nameImg'] != None else 'None'}
    if img['nameImg'] != None:
        pathImg = os.path.join(
            'tablets', brand['nameBrand'], model['nameModel'])
        os.makedirs(pathImg)
        with open(os.path.join(pathImg, img['nameImg']+'.jpg'), 'wb') as imageFile:
            imageFile.write(requests.get(mainUrl+img['urlImg']).content)
            imageFile.close()
    write_csv(dataCsv, 'Tablet.csv')


def main(mainUrl, urlIn):
    listBrand = ListBrand(urlIn)
    for brand in listBrand:
        listModel = ListModel(mainUrl, mainUrl+brand['urlBrand'])
        for model in listModel:
            img = GetImg(mainUrl+model['urlModel'])
            GetData(brand, model, img, mainUrl)


main(mainUrl, urlIn)
