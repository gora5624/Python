import requests

url = 'https://stepic.org/media/attachments/course67/3.6.2/819.txt'
r = requests.get(url)
print(len(r.text.splitlines()))
