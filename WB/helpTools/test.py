import requests
import pandas

url = 'https://suppliers-api.wildberries.ru/api/v3/supplies/WB-GI-29424994'
headersGetCard = {'Authorization': '{}'.format('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y')}
r = requests.delete(url=url, headers=headersGetCard)
r