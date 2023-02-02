from bs4 import BeautifulSoup
from  selenium import webdriver
import time
from selenium.webdriver.common.by import By
# By импортировать для selenium

# заупустить selenium и открыть станицу
browser = webdriver.Chrome()
browser.get('https://irapluskira.online/cms/system/login')
# ввести логин и пароль и нажать кнопку входа
login = browser.find_element('name', 'email')
login.send_keys('marina.pisareva.26@gmail.com')
password = browser.find_element('name','password')
password.send_keys('Marina2018')
button = browser.find_element('xpath', '//*[@id="xdget326045_1_1_1_1_1_1_1_1"]')
button.click()
# перейти на страницу профиля
time.sleep(5)
browser.get('https://irapluskira.online/teach/control/stream/view/id/600047318')
time.sleep(5)
# Найти на странице все элементы по классу
# listModuls = browser.find_element('xpath', '//div[contains(id, "xdgetr")]')
# получить Html Код из browser
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')
elList = soup.find_all('div', class_='xdget-block xdget-image modul with-link')
elList



