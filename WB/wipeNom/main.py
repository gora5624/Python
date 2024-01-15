import pandas as pd
import multiprocessing
import requests
import time
import pickle

# wipeListDF = pd.DataFrame(pd.read_excel(r"F:\Downloads\Новая папка (2)\tmp.xlsx")).to_dict('records')
# with open(r'D:\Python\WB\wipeNom\wipeListDict.pkl', 'wb') as wipeListDictFile:
#     pickle.dump(wipeListDF, wipeListDictFile)
#     wipeListDictFile.close()
with open(r'D:\Python\WB\wipeNom\wipeListDict.pkl', 'rb') as wipeListDictFile:
    wipeListDF = pickle.load(wipeListDictFile)
    wipeListDictFile.close()
headers = {'Authorization': '{}'.format('eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njg4MiwiaWQiOiI4YjEzZWUzOC03MGIxLTQ3ZjgtYTdlNC03OTIzY2Q2ZmQ3ZTciLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjEwMTA2MiwicyI6MTAsInNpZCI6IjNhOTNkZGMxLWFhNTctNWMyYi05YzVjLWRkZDIyMTg4OTQ0MCIsInVpZCI6NDUzMjI5MjB9.DXm6RuooUieyrnNdXr3FfPPdwK5uV4aiTF5SZIryJUhbQW4uScXQLEb-n8p0iM3RT6Js6aVKijiyOkawE6r76g')}

def wipeData(wipeListDF):
    json = []
    chrtIDList = []
    try:
        with open(r'D:\Python\WB\wipeNom\chrtIDList.pkl', 'rb') as chrtIDListFile:
            chrtIDListDone = pickle.load(chrtIDListFile)
            chrtIDListFile.close()
    except:
        chrtIDListDone = []
    try:
        with open(r'D:\Python\WB\wipeNom\chrtIDListErrors.pkl', 'rb') as chrtIDListErrorsFile:
            chrtIDListErrors = pickle.load(chrtIDListErrorsFile)
            chrtIDListErrorsFile.close()
    except:
        chrtIDListErrors = []
    try:
        with open(r'D:\Python\WB\wipeNom\badNmIDlist.pkl', 'rb') as badNmIDlistFile:
            badNmIDlist = pickle.load(badNmIDlistFile)
            badNmIDlistFile.close()
    except:
        badNmIDlist = []
    # dfTMP = pd.DataFrame({'chrtIDListDone':chrtIDListDone}).to_excel(r'D:\Python\WB\wipeNom\chrtIDListDone.xlsx', index=False)
    # # dfTMP = pd.DataFrame({'badNmIDlist':badNmIDlist}).to_excel(r'D:\Python\WB\wipeNom\badNmIDlist.xlsx', index=False)
    # dfTMP = pd.DataFrame({'chrtIDListErrors':chrtIDListErrors}).to_excel(r'D:\Python\WB\wipeNom\badNmIDlist.xlsx', index=False)
    for line in wipeListDF:
        # if (line['chrtID'] not in  chrtIDListDone) and line['nmID'] not in badNmIDlist:
        if (line['chrtID'] not in chrtIDListDone):# and (line['nmID'] not in badNmIDlist):
            sizes = [
                {
                    "chrtID": line['chrtID'],
                    #"price": 590,
                    "skus": [str(line['skus'])]
                }
            ]
            subject = line['object'] if line['object']!= 'Пленки защитные' else 'Защитная пленка'
            #if subject ==# 
            cardJson = {
                #"imtID": line['imtID'],
                "nmID": line['nmID'],
                "subject": subject,
                "vendorCode": line['vendorCode'],
                "sizes": sizes,
                "characteristics": [{"Предмет": subject}]
            }
            json.append(cardJson)
            chrtIDList.append(line['chrtID'])
        if len(json) >= 20:
            try:
                r = requests.post(url='https://suppliers-api.wildberries.ru/content/v1/cards/update', headers=headers, json=json, timeout=50)
                r
            except:
                chrtIDListErrors.extend(chrtIDList)
                with open(r'D:\Python\WB\wipeNom\chrtIDListErrors2.pkl', 'wb') as chrtIDListErrorsFile:
                    pickle.dump(chrtIDListErrors, chrtIDListErrorsFile)
                    chrtIDListErrorsFile.close()
                    chrtIDList = []
                    json = []
                    time.sleep(7)
                    continue
            #print(r.status_code)
            if r.status_code ==200:
                chrtIDListDone.extend(chrtIDList)
                with open(r'D:\Python\WB\wipeNom\chrtIDList.pkl', 'wb') as chrtIDListFile:
                    pickle.dump(chrtIDListDone, chrtIDListFile)
                    chrtIDListFile.close()
            elif r.status_code ==400:
                if 'Invalid nmID' in r.text:
                    errorJson = r.json()
                    badNmIDlist.extend([int(x) for x in errorJson['errorText'].replace('bad request; Invalid nmID','').strip().split(',')])
                    with open(r'D:\Python\WB\wipeNom\badNmIDlist.pkl', 'wb') as badNmIDlistFile:
                        pickle.dump(badNmIDlist, badNmIDlistFile)
                        badNmIDlistFile.close()
                    badNmIDlist
                    badIndex = []
                    for i, card in enumerate(json):
                        if card['nmID'] in badNmIDlist:
                            badIndex.append(i)
                    for index in reversed(badIndex):
                        json.pop(index)
                    continue
                else:
                    print(r.text)
            else:
                print(r.text)
            chrtIDList = []
            json = []
            time.sleep(6)


def changePrice(wipeListDF):
    try:
        with open(r'D:\Python\WB\wipeNom\priceDoneList.pkl', 'rb') as priceDoneListFile:
            priceDoneList = pickle.load(priceDoneListFile)
            priceDoneListFile.close()
    except:
        priceDoneList = []
    try:
        with open(r'D:\Python\WB\wipeNom\priceErrorsList.pkl', 'rb') as priceErrorsListFile:
            priceErrorsList = pickle.load(priceErrorsListFile)
            priceErrorsListFile.close()
    except:
        priceErrorsList = []
    jsonPrice = []
    jsonDiscounts = []
    priceTmp = []
    for line in wipeListDF:
        if line['nmID'] not in priceDoneList:
            json1 = {
                    "nmId": line['nmID'],
                    "price": 5000
                }
            jsonPrice.append(json1)
            json2 = {
                        "nm": line['nmID'],
                        "discount": 0
                    }
            jsonDiscounts.append(json2)
            priceTmp.append(line['nmID'])
            if len(jsonPrice)>=1000:
                try:
                    r1 = requests.post(url='https://suppliers-api.wildberries.ru/public/api/v1/updateDiscounts', json=jsonDiscounts, headers=headers, timeout=50)
                    r1
                    r2 = requests.post(url='https://suppliers-api.wildberries.ru/public/api/v1/prices', json=jsonPrice, headers=headers, timeout=50)
                    r2
                    priceDoneList.extend(priceTmp)
                except:
                    priceErrorsList.extend(priceTmp)
                    with open(r'D:\Python\WB\wipeNom\priceErrorsList.pkl', 'wb') as priceErrorsListFile:
                        pickle.dump(priceErrorsList, priceErrorsListFile)
                        priceErrorsListFile.close()
                    continue
                if r1.status_code == 200:
                    with open(r'D:\Python\WB\wipeNom\priceDoneList.pkl', 'wb') as priceDoneListFile:
                        pickle.dump(priceDoneList, priceDoneListFile)
                        priceDoneListFile.close()
                priceTmp = []
                jsonPrice = []
                jsonDiscounts = []


def wipeMediafiles(wipeListDF):
    try:
        with open(r'D:\Python\WB\wipeNom\mediaDoneList.pkl', 'rb') as mediaDoneListFile:
            mediaDoneList = pickle.load(mediaDoneListFile)
            mediaDoneListFile.close()
    except:
        mediaDoneList = []
    try:
        with open(r'D:\Python\WB\wipeNom\mediaErrorsList.pkl', 'rb') as mediaErrorsListFile:
            mediaErrorsList = pickle.load(mediaErrorsListFile)
            mediaErrorsListFile.close()
    except:
        mediaErrorsList = []
    for line in wipeListDF:
        if line['vendorCode'] not in mediaDoneList:
            jsonRequest = {
                    "vendorCode": line['vendorCode'],
                    "data": ['http://95.78.233.163:8001/wp-content/uploads/1.jpg']
                    }
            try:
                r = requests.post(url='https://suppliers-api.wildberries.ru/content/v1/media/save', json=jsonRequest, headers=headers, timeout=50)  
                r
            except:
                mediaErrorsList.append(line['vendorCode'])
                with open(r'D:\Python\WB\wipeNom\mediaErrorsList.pkl', 'wb') as mediaErrorsListFile:
                        pickle.dump(mediaErrorsList, mediaErrorsListFile)
                        mediaErrorsListFile.close()
                continue
            if r.status_code ==200:
                mediaDoneList.append(line['vendorCode'])
                with open(r'D:\Python\WB\wipeNom\mediaDoneList.pkl', 'wb') as mediaDoneListFile:
                        pickle.dump(mediaDoneList, mediaDoneListFile)
                        mediaDoneListFile.close()
            time.sleep(0.7)

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=wipeData, args=(wipeListDF,))
    # p2 = multiprocessing.Process(target=changePrice, args=(wipeListDF,))
    p3 = multiprocessing.Process(target=wipeMediafiles, args=(wipeListDF,))
    p1.start()
    # p2.start()
    p3.start()
    p1.join()
    # p2.join()
    p3.join()
    # wipeData(wipeListDF)
    # changePrice(wipeListDF)
    # wipeMediafiles(wipeListDF)