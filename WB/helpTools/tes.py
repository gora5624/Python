from urllib import response
import requests

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
url = 'https://suppliers-api.wildberries.ru/api/v2/orders/stickers'
json = {
  "orderIds": [
    479776624
  ]
}
headers = {'Authorization': token}
responce = requests.post(url=url, json=json, headers=headers)
responce