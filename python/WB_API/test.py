
from os.path import join as joinpath
import requests
from my_lib import read_xlsx
import pandas
import json
import multiprocessing
import uuid

main_path = r'C:\Users\Public\Documents\WBChangeStuff'
nameListStuff = r'StuffList.xlsx'
pathToListStuff = joinpath(main_path, nameListStuff)
Token_path = joinpath(main_path, r'Token.txt')
outListName = 'barcodes and art.xlsx'
outListName2 = 'barcodes and art2.xlsx'
outListPath = joinpath(main_path, outListName)
outListPath2 = joinpath(main_path, outListName2)


def getIdWithBarcod(barcod):
    id = str(uuid.uuid4())
    with open(Token_path, 'r', encoding='UTF-8') as file:
        Token = file.read()
        file.close()
    Url = 'https://suppliers-api.wildberries.ru/card/upload/file/multipart'

    while True:
        try:
            response = requests.post(Url, headers={
                'Authorization': '{}'.format(Token), 'Content-Type': 'multipart/form-data', 'X-File-Id': id}, json=datajson)
            if response.status_code == 200:
                break
            else:
                print(response.text)
                continue
        except:
            continue
    a = response.json()['result']['cards'][0]
    print(barcod)
    return response.json()['result']['cards'][0]['imtId']


getIdWithBarcod('2011689379002')
