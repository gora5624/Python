import os
import requests
from os.path import join as joinpath

url = 'https://suppliers-api.wildberries.ru/api/v2/supplies?status=ACTIVE'
main_path = r'C:\Users\Public\Documents\WBChangeStuff'
Token_path = joinpath(main_path, r'Token.txt')
with open(Token_path, 'r', encoding='UTF-8') as file:
    Token = file.read()
    file.close()

response = requests.get(url=url, headers={
                'Authorization': '{}'.format(Token)})

suppList = response.json()
suppList