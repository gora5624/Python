import requests
import sys
import pandas
import time

# url = re.sub(r'print.+\d\.jpg', number+'.jpg', url ).replace('Готовые принты/Силикон','Вторые картинки')
countReqPMin = 100
delay = 60/countReqPMin
def pushPhoto(line, token, requestUrl, countTry=0):
    if 'Артикул товара' in list(line.keys()):
        url = line['Медиафайлы'].split(';')
        data = [url[0]]
        # for i in range(1,6,1):
        #     data.append(re.sub(r'print.+\d\.jpg', str(i)+'.jpg', url ).replace('Готовые принты/Силикон','Вторые картинки'))
        jsonRequest = {
            "vendorCode": line['Артикул товара'],
            #"data": line['Медиафайлы'].split(';')
            "data": data
            }
        headersRequest = {'Authorization': '{}'.format(token)}
    else:
        # data = line['Медиафайлы'].split(';')
        url = line['Медиафайлы'].split(';')
        data = [url[0]]
        # for i in range(1,6,1):
        #     data.append(re.sub(r'print.+\d\.jpg', str(i)+'.jpg', url ).replace('Готовые принты/Силикон','Вторые картинки'))
        # if len(data) ==3:
        #     tmp = [data[-1].replace('2.jpg', '3.jpg'), data[-1].replace('2.jpg', '4.jpg'), data[-1].replace('2.jpg', '5.jpg')]
        #     data.extend(tmp)
        jsonRequest = {
            "vendorCode": line['Артикул поставщика'],
            "data": data
            # "data": line['Медиафайлы'].split(';')
            }
        headersRequest = {'Authorization': '{}'.format(token)}
    try:
        # print(jsonRequest)
        #jsonRequest['data'][0]= jsonRequest['data'][0].replace("/print ","/(Принт ").replace(".jpg",").jpg")
        #print(jsonRequest)
        r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest, timeout=50)  
        r
        #time.sleep(0.6)
        if '"Неверный запрос: по данному артикулу не нашлось карточки товара","additionalErrors' in r.text:
            print('Не нашлось карточки товара '+jsonRequest['vendorCode'])
        if '"Внутренняя ошибка сервиса","additionalErrors' in r.text:
            print('1')
        if '"additionalErrors":null' not in r.text:
            print(r.text + ' ' + jsonRequest['vendorCode'])
    except requests.ConnectionError:
        r = requests.post(requestUrl, json=jsonRequest, headers=headersRequest, timeout=50) 
        print(r.text + jsonRequest['vendorCode'])
    except requests.exceptions.ReadTimeout:
        print('requests.ReadTimeout'  + jsonRequest['vendorCode'])

    except:
        print('TimeoutError')
    # if requestsVendorCode(line['Артикул товара']) != 0 and countTry < 5:
    #     countTry +=1
    #     pushPhoto(line, token, requestUrl, countTry)




def updatePhotoMain(pathToFile=None, token=None):
    
    if (pathToFile == None) and (token ==None):
        pathToFile = r"F:\Для загрузки\Готовые принты\Силикон\Чехол Samsung Galaxy M33 5G силикон с зак.кам. проз. под карту.xlsx"
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImUyZTIyZGE1LTYxYWYtNDgyMi1hMDVkLTZiNzVlMTBiNzlmMiJ9.yDq9XasZjs-oB1PapNbD_NWIH8tgWEz_WyKLvVTNgBs'
        # pathToFile = sys.argv[1:][0].replace('#', '
    print(pathToFile)
    df = pandas.DataFrame(pandas.read_excel(pathToFile))
    requestUrl = 'https://suppliers-api.wildberries.ru/content/v1/media/save'
    #if __name__ == '__main__':
    passedTime = 1
    tmp = pandas.DataFrame(pandas.read_excel(r"F:\книжки без фото.xlsx"))['Артикул продавца'].to_list()
    for line in df.to_dict('records'):
        if line['Артикул товара'] in tmp:
            if passedTime > 0.7:
                startTime = time.time()
                pushPhoto(line, token, requestUrl)
                passedTime = time.time() - startTime
            else:
                time.sleep(0.7-passedTime)
                passedTime = 1
    print('Done')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        updatePhotoMain(sys.argv[1:][0].replace('#', ' '), sys.argv[1:][1].replace('#', ' '))
    else:
        updatePhotoMain()
