import os
from my_lib import write_csv, get_html
from bs4 import BeautifulSoup

mainUrl = r'https://mobi711.ru/catalog/aksessuary-dlya-telefonov/'


def GetListBrandAndModels(mainUrl):
    html = get_html(mainUrl)
    soup = BeautifulSoup(html, 'lxml')
    ListBrandDiv = soup.find_all('div', class_='category-wrap')
    for Div in ListBrandDiv:
        BrandName = Div.find('div', class_='text').find('a').text
        try:
            ListModelsA = Div.find('div', class_='sub').find_all('a')
        except AttributeError:
            ListModelsA = ''
        for A in ListModelsA:
            Text = A.text
            if Text != 'Показать еще':
                ModelName = Text
                Url = A.get('href')
            data = {'Brand': BrandName,
                    'Model': ModelName,
                    'Url': Url}
            write_csv(data, 'Mobi711.csv')


def main(mainUrl):
    GetListBrandAndModels(mainUrl)


if __name__ == "__main__":
    main(mainUrl)
