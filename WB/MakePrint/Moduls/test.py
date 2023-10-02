import requests
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImUyZTIyZGE1LTYxYWYtNDgyMi1hMDVkLTZiNzVlMTBiNzlmMiJ9.yDq9XasZjs-oB1PapNbD_NWIH8tgWEz_WyKLvVTNgBs'
def pushPhoto(token, requestUrl):

        jsonRequest = {
            "vendorCode": 'Samsung_Galaxy_A03_PRNT_PNK_OCM_TXTBP_PNK_TXT_PRNT_2355',
            "data": []
            # "data": line['Медиафайлы'].split(';')
            }
        headersRequest = {'Authorization': '{}'.format(token)}
        try:
            # print(jsonRequest)
            #jsonRequest['data'][0]= jsonRequest['data'][0].replace("/print ","/(Принт ").replace(".jpg",").jpg")
            #print(jsonRequest)
            r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest, timeout=5)  
            r
            if '"Неверный запрос: по данному артикулу не нашлось карточки товара","additionalErrors' in r.text:
                print('Не нашлось карточки товара '+jsonRequest['vendorCode'])
            if '"Внутренняя ошибка сервиса","additionalErrors' in r.text:
                print('1')
            print(r.text + ' ' + jsonRequest['vendorCode'])
        except requests.ConnectionError:
            r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest, timeout=5) 
            print(r.text)
        except requests.exceptions.SSLError:
            print('requests.ReadTimeout')
        except requests.exceptions.ReadTimeout:
            print('requests.ReadTimeout')

        except:
            print('TimeoutError')
    # if requestsVendorCode(line['Артикул товара']) != 0 and countTry < 5:
    #     countTry +=1
    #     pushPhoto(line, token, requestUrl, countTry)

requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/media/save'

pushPhoto(token,requestUrl)