import requests
import pandas
import multiprocessing
import time
import json
# -*- coding: utf-8 -*-


def requestsVendorCode():        
    url = 'https://suppliers-api.wildberries.ru/content/v1/cards/filter'
    headersRequest = {'Authorization': '{}'.format('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM')}
    json = {
  "vendorCodes": ['CARTHOLDER_2_RING_FRT_PRNT_2100'
  ]
}
    response = requests.post(url=url, headers=headersRequest, json=json, timeout=2)
    if response.status_code == 200:
        for card in response.json()['data']:
            if card['vendorCode'] == 'CARTHOLDER_2_RING_FRT_PRNT_2100':
                if len(card['mediaFiles']) == 0:
                    print(card['mediaFiles'])
        # if len(response.json()['data']['cards']) !=0:
            #print(response.text)
    else:
        print(str(response.status_code))
        print(response.text)

    

if __name__ =='__main__':
    requestsVendorCode()