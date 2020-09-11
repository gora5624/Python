import os
from my_lib import write_csv, get_html
from bs4 import BeautifulSoup
from threading import Thread

# Создаём класс который делает, что нам надо. А именно раскрывает список и для каждого элемента вытаскивает инфу


class GetInfo(Thread):
    def __init__(self, ListData):
        Thread.__init__(self)
        self.ListData = ListData

    def run(self):
        GetFilmCatalog(self.ListData, num)


# точка входа на сайт
mainUrl = r'https://mobi711.ru/catalog/planshety'
# Количество потоков
num = 10

# возвращает словарей с брэндами, моделями и урлами смартфонов на сайте, для последующего парсинга


def GetListBrandAndModels(mainUrl):
    html = get_html(mainUrl)
    soup = BeautifulSoup(html, 'lxml')
    ListBrandDiv = soup.find_all('div', class_='category-wrap')
    ListData = []
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
            ListData.append(data)
            #write_csv(data, 'Mobi711Planshety.csv')
    return ListData

# получает список из предыдуущей функции и записывает всё (брэенд, модель, урл модели и урл каталога с пленками) в csv


def GetFilmCatalog(ListData, num):
    NameFile = r'D:\tmp\my_prod\Python\python\ParsingMobi711\MobiParsTab_mp.csv'
    for Data in ListData:
        html = get_html('https://mobi711.ru'+Data['Url'])
        soup = BeautifulSoup(html, 'lxml')
        try:
            DivUrlFilmCatalog = soup.find_all(
                'div', class_='category no-description')
        except AttributeError:
            DivUrlFilmCatalog = []
        if DivUrlFilmCatalog != []:
            for Div in DivUrlFilmCatalog:
                UrlFilmCatalog = 'https://mobi711.ru' + \
                    Div.find('div', class_='text').find('a').get('href')
                Name = Div.find('div', class_='text').find('a').text
                if Name == 'Защитные пленки и стекла':
                    break
                else:
                    UrlFilmCatalog = ''
                    Name = ''
        data = {'Brand': Data['Brand'],
                'Model': Data['Model'],
                'UrlModel': Data['Url'],
                'UrlFilmCatalog': UrlFilmCatalog}

        write_csv(data, NameFile)

# разделяем список, который возвращает GetListBrandAndModels на несколько списков, в зависимости от количестива заданных потоков


def SplitListData(ListData, num):
    Count = len(ListData)//num+1

    ListListData = [0] * num
    TmpList = []
    NumList = 0
    i = 1
    for data in ListData:
        i += 1
        if i <= Count:
            TmpList.append(data)
        else:
            TmpList.append(data)
            ListListData[NumList] = TmpList
            i = 0
            NumList += 1
            TmpList = []
    ListListData[NumList] = TmpList
    return ListListData


def main(mainUrl, num):
    ListData = GetListBrandAndModels(mainUrl)
    ListListData = SplitListData(ListData, num)
    for item, List in enumerate(ListListData):
        thread = GetInfo(List)
        thread.start()


if __name__ == "__main__":
    main(mainUrl, num)
