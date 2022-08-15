
from bs4 import BeautifulSoup
import pandas
import requests
import multiprocessing
import asyncio
import aiohttp



def parserPageWithGadget(url, result):
        tmpDict = {}
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        name = soup.find('h1', class_='b-title p-content__title').text
        tmpDict.update({'Название': name.strip()})
        print(name.strip())
        try:
            tableLines = soup.find('div', class_='b-cut helpixcut p-content__helpixcut').find_all('tr')
        except:
            tableLines = []
        if tableLines != []:
            for line in tableLines:
                try:
                    nameAdd = line.find('td', class_='b-devSpecTab__td b-devSpecTab__td_name')
                    if nameAdd != None:
                        nameAdd = nameAdd.text.replace(':','')
                    else:
                        continue
                    valueAdd = line.find('td', class_='b-devSpecTab__td b-devSpecTab__td_value')
                    if valueAdd != None:
                        valueAdd = valueAdd.text
                    else:
                        continue
                except:
                    continue
                tmpDict.update({nameAdd:valueAdd})
        try:
            desc = soup.find('div', class_='b-devLead p-content__devLead')
            if desc!= None:
                desc = desc.text
            else:
                desc = ''
            tmpDict.update({'Описание': desc.strip()})
        except AttributeError:
            tmpDict.update({'Описание': 'Нет'})
        tmpDict.update({'Ссылка': url})
        result.append(tmpDict)




def startTasksForParsing(urlList, pool):
    
    manager = multiprocessing.Manager()
    result = manager.list()
    for url in urlList:
        pool.apply_async(parserPageWithGadget, args=(url, result,))
    return result


async def getUrlList(url):
    urlList = []
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            if response.status != 200:
                        print('error')
                        print(await response.text())
            soup = BeautifulSoup(html, 'lxml')
            listBrand = soup.find_all('a', class_='b-listli__link b-listli__link_u')
            for brand in listBrand:
                urlBrand = 'https://helpix.ru/' +  brand.get('href')
                #print(urlBrand)
                async with session.get(urlBrand) as response:
                    if response.status != 200:
                        print('error')
                        print(await response.text())
                    html = await response.text()
                    soup = BeautifulSoup(html, 'lxml')
                    listYears = soup.find_all('div', class_='brandyea')
                    for year in listYears:
                        if int(year.find('div', class_='brandyeaheader').text) > 2015:
                            year = soup.find_all('span', class_='brandphonename')
                            for model in year:
                                urlList.append('https://helpix.ru/' + model.find('a').get('href'))
    return urlList




gadgetsTypeList = [
{
    'Наименовение': 'Телефоны',
    'Ссылка': 'https://helpix.ru/devtyp/phone_gsm/'
},
{
    'Наименовение': 'Планшеты',
    'Ссылка': 'https://helpix.ru/devtyp/pad/'
},
{
    'Наименовение': 'Читалки (Электронные книги)',
    'Ссылка': 'https://helpix.ru/devtyp/ebook/'
}
]
if __name__ == '__main__':
    for gadget in gadgetsTypeList:
        loop = asyncio.get_event_loop()
        urlList = loop.run_until_complete(getUrlList(gadget['Ссылка']))
        pool = multiprocessing.Pool()
        result = startTasksForParsing(urlList, pool)
        pool.close()
        pool.join()
        df = pandas.DataFrame(list(result))
        df.to_excel('E:\\{}.xlsx'.format(gadget['Наименовение']), index=False)
print('done')