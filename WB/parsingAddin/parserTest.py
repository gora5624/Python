from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pandas
import asyncio
import time
start_time = time.time()
sem = asyncio.Semaphore(3)

async def parser(stufList, url):
    async with sem:
        # browser = webdriver.PhantomJS(r'C:\Users\Георгий\Downloads\phantomjs-2.1.1-windows\bin\phantomjs.exe')
        browser = webdriver.Chrome('E:\MyProduct\Python\WB\parsingAddin\chromedriver.exe')
        browser.get(url)
        #ищем имя
        await asyncio.sleep(5)
        try:
            # name = WebDriverWait(browser, timeout=5).until(lambda d: d.find_element(By.CLASS_NAME,  'product-page__header' ).find_element(By.TAG_NAME, 'h1').text)
            name = browser.find_element(By.CLASS_NAME,  'product-page__header' ).find_element(By.TAG_NAME, 'h1').text
        except:
            name = ''
        #ищем описание
        try:
            # desc = WebDriverWait(browser, timeout=5).until(lambda d: d.find_element(By.CLASS_NAME,  'collapsable__text' ).text)
            desc = browser.find_element(By.CLASS_NAME,  'collapsable__text' ).text
        except:
            desc = ''
        try:
            # productNmId = WebDriverWait(browser, timeout=5).until(lambda d: d.find_element(By.ID,  'productNmId' ).get_attribute("innerText").strip())
            productNmId = browser.find_element(By.ID,  'productNmId' ).get_attribute("innerText").strip()
        except:
            productNmId = ''
        try:
            # urlDivs = WebDriverWait(browser, timeout=5).until(lambda d: d.find_element(By.CLASS_NAME, 'swiper-wrapper'))
            urlDivs = browser.find_element(By.CLASS_NAME, 'swiper-wrapper')
        except:
            pass
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
            addin = browser.find_elements(By.CSS_SELECTOR, "tr.product-params__row")
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
        stufList.append(addinDict)

async def start():
    stufList = []
    urlList = ['https://www.wildberries.ru/catalog/89152484/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/84900530/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/74919705/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/74919145/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/74918243/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/74916523/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/74919705/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/74919145/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/74918243/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/74916523/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/74919705/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/74919145/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/89152484/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/84900530/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/74919705/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/74919145/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/74918243/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/74916523/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/74919705/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/74919145/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/74918243/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/74916523/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/74919705/detail.aspx?targetUrl=XS', 'https://www.wildberries.ru/catalog/74919145/detail.aspx?targetUrl=XS']
    tasks = [asyncio.ensure_future(parser(stufList, url)) for url in urlList]
    # for url in urlList:
    #     tasks.append(asyncio.create_task(parser(stufList, url)))
    await asyncio.gather(*tasks)
    #return stufListtmp

loop = asyncio.get_event_loop()
loop.run_until_complete(start())
# stufListtmp = asyncio.run(start())
print("--- %s seconds ---" % (time.time() - start_time))
# stufListpd = pandas.DataFrame(stufListtmp)
# stufListpd.to_excel(r'F:\\123.xlsx', index=False)