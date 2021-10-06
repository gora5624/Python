import requests

url = 'https://www.wildberries.ru/catalog/15791706/detail.aspx?targetUrl=XS'
r = requests.get(url)
r.cookies
print(r.cookies)
