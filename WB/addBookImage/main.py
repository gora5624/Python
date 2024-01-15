import requests
import pandas as pd
import os
import pickle
import time
from urllib.parse import quote
# -*- coding: utf-8 -*-


samExlPath = r"F:\Downloads\Самвел.xlsx"
karExlPath = r"F:\Downloads\Караханян.xlsx"
abrExlPath = r"F:\Downloads\Абраамян.xlsx"

def createListForUploaudsImage(pathToDb, token='a'):
    vendorCodesList = pd.DataFrame(pd.read_excel(pathToDb))['Артикул продавца'].to_list()
    cardForUpdate = []
    for a in [r'\\192.168.0.33\shared\_Общие документы_\Егор\Архив принтов xlsx\книжки', r'\\192.168.0.33\shared\_Общие документы_\Егор\Архив принтов xlsx\Книжки новые повторные']:
        for exlsxFile in os.listdir(a):
            if exlsxFile.replace('.xlsx','') in os.listdir(r'\\rab\uploads\Вторые картинки'):
                cardsForAddImage = pd.DataFrame(pd.read_excel(os.path.join(a,exlsxFile))).to_dict('records')
                for line in cardsForAddImage:
                    if line['Артикул товара'] in vendorCodesList:
                        line.update({'pathToImageDir':os.path.join(r'\\rab\uploads\Вторые картинки',exlsxFile.replace('.xlsx',''))})
                        cardForUpdate.append(line)

    if 'Самвел' in pathToDb:       
        with open(r'D:\Python\WB\addBookImage\Самвел.pkl', 'wb') as file:
            pickle.dump(cardForUpdate, file)
            file.close()
        cardForUpdate
    elif 'Караханян' in pathToDb:       
        with open(r'D:\Python\WB\addBookImage\Караханян.pkl', 'wb') as file:
            pickle.dump(cardForUpdate, file)
            file.close()
        cardForUpdate
    elif 'Абраамян' in pathToDb:       
        with open(r'D:\Python\WB\addBookImage\Абраамян.pkl', 'wb') as file:
            pickle.dump(cardForUpdate, file)
            file.close()
        cardForUpdate

try:
    with open(r'D:\Python\WB\addBookImage\done.pkl', 'rb') as file:
                listDone = pickle.load(file)
                file.close()
except:
    listDone = []
try:
    with open(r'D:\Python\WB\addBookImage\errors.pkl', 'rb') as file:
                listErrors = pickle.load(file)
                file.close()
except:
    listErrors = []

def addImage(token, pathToAddImages, listImage, line):
    url=r'https://suppliers-api.wildberries.ru/content/v2/media/file'
    for i, fileImage in enumerate(listImage):  
        headersRequest = {'Authorization': '{}'.format(token), 'X-Vendor-Code':quote(line['Артикул товара']), 'X-Photo-Number':str(i+2)}
        #a = requests.post(url=url, files={'uploadfile':open(os.path.join(pathToAddImages,fileImage), 'rb')}, headers=headersRequest).request
        r = requests.post(url=url, files={'uploadfile':open(os.path.join(pathToAddImages,fileImage), 'rb')}, headers=headersRequest, timeout=50)
        r
        time.sleep(0.6)
    listDone.append(line['Артикул товара'])
    with open(r'D:\Python\WB\addBookImage\done.pkl', 'wb') as fileDone:
        pickle.dump(listDone, fileDone)
        fileDone.close()

# for i in [samExlPath, karExlPath, abrExlPath]:
#     createListForUploaudsImage(i)
listTMP = [
    {
        'path': r'D:\Python\WB\addBookImage\Караханян.pkl',
        'token': 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njg4MiwiaWQiOiI4YjEzZWUzOC03MGIxLTQ3ZjgtYTdlNC03OTIzY2Q2ZmQ3ZTciLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjEwMTA2MiwicyI6MTAsInNpZCI6IjNhOTNkZGMxLWFhNTctNWMyYi05YzVjLWRkZDIyMTg4OTQ0MCIsInVpZCI6NDUzMjI5MjB9.DXm6RuooUieyrnNdXr3FfPPdwK5uV4aiTF5SZIryJUhbQW4uScXQLEb-n8p0iM3RT6Js6aVKijiyOkawE6r76g'
    },
    {
        'path': r'D:\Python\WB\addBookImage\Самвел.pkl',
        'token': 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njk3MiwiaWQiOiJjZWE4ZTNmYy1iYzg5LTRjYjktYmNmNy0xN2ZiNmNjNzk1MTQiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjgxOTI0NiwicyI6MTAsInNpZCI6IjBhYjhiMTA1LTA1MWYtNGVkNi04NzBiLTM5OWU3NWUxMDI4NiIsInVpZCI6NDUzMjI5MjB9.bOmPtl_ZXx-1C25-5CbftPJVQuuHzwG5iH9QUx0x8CdZCjI9ZnbFgMU1ijL-lfgn_N1JxPvojV2dBrKTpDnolw'
    },
    {
        'path': r'D:\Python\WB\addBookImage\Абраамян.pkl',
        'token': 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njk1MSwiaWQiOiIyMzUyZGFmYS05NTdhLTQ0MzAtYWFhMi1lZGM5NDZkZDY0ODEiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjUyNzczNiwicyI6MTAsInNpZCI6ImFhNDdlNDg5LTU5ZTAtNDIzMi1hMWJmLTBlMTIzOWYwNDJmMSIsInVpZCI6NDUzMjI5MjB9.j9s_VtDpTEWceEd1vUTWf6uofUuSY30q0UrR-H047qZE40sb8atwtAviABB7eoeLQdu3T69UosBdn_Bvj2-2ZQ'
    },
]
for tmp in listTMP:
    with open(tmp['path'], 'rb') as file:
            cardForUpdate = pickle.load(file)
            file.close()
    #pathToAddImages = cardForUpdate[0]['pathToImageDir']
    for line in cardForUpdate:
        if line['Артикул товара'] not in listDone:
            try:
                listImage = os.listdir(line['pathToImageDir'])
                addImage(tmp['token'], line['pathToImageDir'], listImage, line)
            except:
                listErrors.append(line['Артикул товара'])
                with open(r'D:\Python\WB\addBookImage\errors.pkl', 'wb') as fileErrors:
                   pickle.dump(listErrors, fileErrors)
                   fileErrors.close()
                continue