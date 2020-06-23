from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup

driver = webdriver.Chrome(
    executable_path=r'D:\tmp\python\python_parsing\parsing_site\chromedriver.exe')
driver.get(
    "https://argo-ivanovo.ru/tekstil-i-uniforma-horeca/kostjum-zhenskij-povara-40-60-tkan-tisi")
driver.find_element_by_xpath("//*[@itemprop='image']").click()
soup = BeautifulSoup(driver.page_source, 'lxml')
url_image = soup.find('div', class_='slide current').find('img')['src']
print(url_image)
# driver.close()
