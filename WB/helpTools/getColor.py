from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import copy


# http = requests.get('https://novoplast.ua/base/pantone')
# soup = BeautifulSoup('http', 'lxml')
# a = soup.find_all('path')
# a


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x935')
browser = webdriver.Chrome(r'E:\MyProduct\Python\WB\feedbackAnswer\webdriver\chromedriver.exe',chrome_options=options)
browser2 = webdriver.Chrome(r'E:\MyProduct\Python\WB\feedbackAnswer\webdriver\chromedriver.exe',chrome_options=options)
browser.get('https://novoplast.ua/base/pantone')
elementTMP = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "col-lg-12")))
#ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
divs = browser.find_elements(By.CSS_SELECTOR, "[style='overflow:scroll;']")
with open('E:\colors.txt', 'w') as file:
    for div in divs:
        a = div.find_element(By.TAG_NAME, 'embed').get_attribute('src')
        browser2.get(a)
        tspans = browser2.find_elements(By.TAG_NAME, "tspan")
        for tspan in tspans:
            text = tspan.text
            if 'C:' in text and 'M:' in text and 'Y' in text and 'K:' in text:
                file.writelines(text+'\n')
file.close()
