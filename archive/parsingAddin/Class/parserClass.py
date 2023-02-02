import requests
import pandas
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class Parser():
    def __init__(self, searchRequest, sorting, pages) -> None:
        self.searchRequest = searchRequest
        self.sorting = self.setSorting(sorting)
        self.pages = int(pages)
        self.url = 'https://www.wildberries.ru/catalog/0/search.aspx?page={}&sort={}&search={}'
        self.urlList = []
        self.caseLIstWithAddin = []


    def setSorting(self, sorting):
        if sorting == 'По популярности':
            return 'popular'
        elif sorting == 'По рейтингу':
            return 'rate'
        elif sorting == 'По возрастанию цены':
            return 'priceup'
        elif sorting == 'По убыванию цены':
            return 'pricedown'
        elif sorting == 'По скидке':
            return 'sale'
        elif sorting == 'По обновлению':
            return 'newly'
        # elif sorting == 'По всем, по порядку':
        #     return ['popular', 'rate', 'priceup', 'pricedown', 'sale', 'newly']


    def parserMain(self):
        for page in range(self.pages): 
            urlListTMP = self.getListUrlCaseOnPage(page)
            if urlListTMP != None:
                self.urlList.extend(urlListTMP)
            else:
                break
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x935')
        browser = webdriver.Chrome(r'E:\MyProduct\Python\WB\parsingAddin\chromedriver.exe', chrome_options=options)
        for urlCase in self.urlList:
            self.getAddinCase(urlCase, browser)
        pd = pandas.DataFrame(self.caseLIstWithAddin)
        pd.to_excel(r'F:\\{}.xlsx'.format(self.searchRequest), index=False)


    def getListUrlCaseOnPage(self, page):   
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x935')
        browser = webdriver.Chrome(r'E:\MyProduct\Python\WB\parsingAddin\chromedriver.exe', chrome_options=options)
        a = self.url.format(str(page+1), self.sorting, self.searchRequest.replace('  ',' ').replace(' ','+'))
        browser.get(self.url.format(str(page+1), self.sorting, self.searchRequest.replace('  ',' ').replace(' ','+')))
        noCaseElement = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "catalog-page__text")))
        if 'По Вашему запросу ничего не найдено.' in noCaseElement.text:
            return None
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-card__wrapper")))
        urlOnPageList = [a.find_element(By.TAG_NAME,  'a').get_attribute('href') for a in browser.find_element(By.CLASS_NAME,  'product-card-list').find_elements(By.CLASS_NAME,  'product-card__wrapper')]
        self.searchRequest
        return urlOnPageList       


    def getAddinCase(self, urlCase, browser):
        # options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # options.add_argument('window-size=1920x935')
        # options.add_argument('log-level=2')
        # browser = webdriver.Chrome(r'E:\MyProduct\Python\WB\parsingAddin\chromedriver.exe', chrome_options=options)
        browser.get(urlCase)
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "main__container")))
        #ищем имя
        try:
            # name = WebDriverWait(browser, timeout=5).until(lambda d: d.find_element(By.CLASS_NAME,  'product-page__header' ).find_element(By.TAG_NAME, 'h1').text)
            name = browser.find_element(By.CLASS_NAME, 'main__container').find_element(By.CLASS_NAME, 'product-page__header-wrap').find_element(By.CLASS_NAME,  'product-page__header' ).find_element(By.TAG_NAME, 'h1').text
        except:
            name = ''
        #ищем описание
        try:
            # desc = WebDriverWait(browser, timeout=5).until(lambda d: d.find_element(By.CLASS_NAME,  'collapsable__text' ).text)
            desc = browser.find_element(By.CLASS_NAME, 'main__container').find_element(By.CLASS_NAME, 'details-section__inner-wrap').find_element(By.CLASS_NAME,  'collapsable__text' ).text
        except:
            desc = ''
        try:
            # productNmId = WebDriverWait(browser, timeout=5).until(lambda d: d.find_element(By.ID,  'productNmId' ).get_attribute("innerText").strip())
            productNmId = browser.find_element(By.CLASS_NAME, 'main__container').find_element(By.CLASS_NAME, 'product-article').find_element(By.ID,  'productNmId' ).get_attribute("innerText").strip()
        except:
            productNmId = ''
        try:
            # urlDivs = WebDriverWait(browser, timeout=5).until(lambda d: d.find_element(By.CLASS_NAME, 'swiper-wrapper'))
            urlDivs = browser.find_element(By.CLASS_NAME, 'main__container').find_element(By.CLASS_NAME, 'swiper-wrapper')
        except:
            urlDivs = []
        try:
            urlPhotoList = []
            # urlDivs = WebDriverWait(browser, timeout=5).until(lambda d: d.find_elements(By.TAG_NAME, 'img'))
            urlDivs = browser.find_elements(By.TAG_NAME, 'img')
            for div in urlDivs:
                urlPhotoList.append(div.get_attribute('src'))
        except:
            pass
        #ищем остальное
        try:
            # addin = WebDriverWait(browser, timeout=5).until(lambda d: d.find_elements(By.CSS_SELECTOR, "tr.product-params__row"))
            addin = browser.find_element(By.CLASS_NAME, 'main__container').find_element(By.CLASS_NAME, 'product-page__options').find_elements(By.CSS_SELECTOR, "tr.product-params__row")
            addinNameList = []
            addinDict = {
                'productNmId': productNmId,
                'name': name,
                'desc': desc,
                'photoUrls': urlPhotoList}
            for tr in addin:
                nameAddin = tr.find_element(By.TAG_NAME, 'th').get_attribute("innerText").strip()
                valueAddin = tr.find_element(By.TAG_NAME, 'td').get_attribute("innerText").strip()
                if (nameAddin != "") and (nameAddin not in addinNameList):
                    addinNameList.append(nameAddin)
                    addinDict.update({nameAddin: valueAddin})
        except:
            addin = ''
        self.caseLIstWithAddin.append(addinDict)


if __name__ == '__main__':
    parser = Parser("Чехол Redmi 9T", 'По популярности', '5')
    parser.parserMain()
    pass