from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from os.path import abspath as absPath, join as joinPath
import pickle
import time

ua = dict(DesiredCapabilities.CHROME)
options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('window-size=1920x935')
browser = webdriver.Chrome(r'E:\MyProduct\Python\WB\feedbackAnswer\webdriver\chromedriver.exe',chrome_options=options)
cookies = pickle.load(open(absPath(joinPath(__file__,'..',"cookies.pkl")), "rb"))
browser.get('https://seller.wildberries.ru')
for cookie in cookies:
    try:
        browser.add_cookie(cookie) 
    except:
        continue
countTry = 0
try:
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "Login-phone--80x8j")))
    while countTry < 60:
        try:
            WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "InfoCard__1wbqiBmqlO")))
            break
        except:
            continue
    pickle.dump(browser.get_cookies() , open(absPath(joinPath(__file__,'..',"cookies.pkl")),"wb"))
except:
    cookies = pickle.load(open(absPath(joinPath(__file__,'..',"cookies.pkl")), "rb"))
    for cookie in cookies:
        browser.add_cookie(cookie) 
browser.get('https://seller.wildberries.ru/feedback-question/feedbacks/not-answered-feedbacks')
while True:
    pageWrapper = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "pageWrapper__tk9IiBi5QL")))
    WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "mobileCardHeader__1H3XUnuq9T")))
    feedBacks = browser.find_elements(By.CLASS_NAME, 'cardWrapper__2iHsWat1U2')
    time.sleep(2)
    for feedBack in feedBacks:
        rating = 0
        stars = feedBack.find_element(By.CLASS_NAME, 'classContentInfo').find_element(By.CLASS_NAME, 'starsList__18YOcFSKCP').find_elements(By.CLASS_NAME, 'star__1xa8BiJKn7')
        for star in stars:
            pos = star.find_element(By.TAG_NAME, 'div').get_attribute('class')
            if pos == 'starActive__3Io2s_fNwy one__2zmjnX6XEW':
                rating+=1
        if rating == 5:
            feedBack.find_element(By.CLASS_NAME, 'cardAnswerContainer').find_element(By.TAG_NAME, 'button').click()
            text = feedBack.find_element(By.NAME, 'text-area')
            text.send_keys('Спасибо за Ваш отзыв. Рады что Вам понравился наш товар. Ваш отзыв очень важен для нас!')
            #feedBack.find_element(By.CLASS_NAME, 'cardAnswerContainer').find_element(By.TAG_NAME, 'button').click()
            buttons = feedBack.find_element(By.CLASS_NAME, 'cardAnswerContainer').find_elements(By.TAG_NAME, 'button')
            for button in buttons:
                if button.text == 'Ответить':
                    button.click()
    browser.find_element(By.CLASS_NAME, 'paginationBoxViewMobile__H7SNJYS9ib').find_element(By.TAG_NAME, 'button').click()
    time.sleep(3)