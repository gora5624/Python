from email.header import Header
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas

class Parser():
    def __init__(self) -> None:
        pass

def paser():
    url = 'https://www.wildberries.ru/catalog/74919408/detail.aspx?targetUrl=XS'
    header = { 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    r = requests.get(url, headers=header)    
    with open(r'E:\\test.html', 'w', encoding='utf-8') as output_file:
        output_file.write(r.text)
if __name__ == '__main__':
    paser()
    pass