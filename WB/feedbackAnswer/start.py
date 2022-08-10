from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

ua = dict(DesiredCapabilities.CHROME)
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x935')
browser = webdriver.Chrome(r'E:\MyProduct\Python\WB\feedbackAnswer\webdriver\chromedriver.exe',chrome_options=options)
browser.get('https://seller.wildberries.ru')
browser.add_cookie({'name':'WBToken','value':'AqilzhX0ztquDPSKxK8MQg2gVQvc5Q09us6MlmwEY1mkeJWvWTnYPEa1WEJ2g5PXlYGQB2GuOAwEUlvy4xyDuNLC_2ExuZf7hJpYYx3IMJDmAg', 'path':'/'})
browser.add_cookie({'name':'_wbauid','value':'935013321646123270', 'path':'/'})
browser.add_cookie({'name':'locale','value':'ru', 'path':'/'})
browser.add_cookie({'name':'x-supplier-id','value':'3a93ddc1-aa57-5c2b-9c5c-ddd221889440', 'path':'/'})
browser.get('https://seller.wildberries.ru/feedback-question/feedbacks/not-answered-feedbacks')

#time.sleep(10)
element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tabCount__2VcgjIsZUr")))
count = element.text
count