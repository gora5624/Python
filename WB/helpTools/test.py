import requests
import pandas
import multiprocessing
import time
import json
# -*- coding: utf-8 -*-


def requestsVendorCode():        
    url = 'https://suppliers-api.wildberries.ru/content/v1/cards/cursor/list'
    headersRequest = {'Authorization': '{}'.format('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM')}
    json = {
  "sort": {
    "cursor": {
        "limit": 1000
    },
    "filter": {
      "withPhoto": -1
    },
    "sort": {
      "sortColumn": "updateAt",
      "ascending": False
    }
  }
}
    response = requests.post(url=url, headers=headersRequest, json=json, timeout=15)
    if response.status_code == 200:
        card = response.json()['data']
        card
        # for card in response.json()['data']:
        #     if card['vendorCode'] == 'OnePlus_8_Pro_проз_16Про_пр_114_Золотистая_рыба':
        #         print(card)
        #         if len(card['mediaFiles']) == 0:
        #             print(card)
        # # if len(response.json()['data']['cards']) !=0:
        #     #print(response.text)
    else:
        print(str(response.status_code))
        print(response.text)

    

def requestsVendorCode2():        
    url = 'https://suppliers-api.wildberries.ru/content/v1/cards/filter'
    headersRequest = {'Authorization': '{}'.format('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM')}
    json = {
  "vendorCodes": [
    "Realme_8i_BP_CLR_HLD_WMN_PRNT_228"
  ]
}
    response = requests.post(url=url, headers=headersRequest, json=json, timeout=15)
    if response.status_code == 200:
        card = response.json()['data']
        card
        # for card in response.json()['data']:
        #     if card['vendorCode'] == 'Realme_8i_BP_CLR_HLD_WMN_PRNT_228':
        #         print(card)
        #         if len(card['mediaFiles']) == 0:
        #             print(card)
        # # if len(response.json()['data']['cards']) !=0:
        #     #print(response.text)
    else:
        print(str(response.status_code))
        print(response.text)

if __name__ =='__main__':
    requestsVendorCode2()