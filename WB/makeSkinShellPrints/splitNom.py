import requests
import pandas as pd
import time

listCardsPath = r"F:\Downloads\report_2023_8_17.xlsx\tmp.xlsx"
dfFull = pd.DataFrame(pd.read_excel(listCardsPath))
dfCase = dfFull[dfFull['Предмет']=='Чехлы для телефонов']
dfBrand= dfCase[dfCase['Бренд']=='Mobi114']
dfBrand.sort_values(by=['Артикул продавца'], inplace=True,kind='stable')
listArtVendor = dfBrand['Артикул WB'].values.tolist()
url = 'https://suppliers-api.wildberries.ru/content/v1/cards/moveNm'
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImU4NjQ1YWI5LWFjM2UtNGFkOS1hYmIyLThkMTMzMGM1YTU3NyJ9.8nz9gIHurlCVKIhruG6hY8MRBtMLvLYggVzisxgKivY'
headers = {'Authorization': '{}'.format(token)} 
for i in range(0,len(listArtVendor),30):
    countTry = 0
    while True:
        x = listArtVendor[i:i+30]
        json = {
            'nmIDs':x
        }
        try:
            r = requests.post(url=url, json=json, headers=headers, timeout=10)
            break
        except:
            countTry+=1
            if countTry <10:
                continue
            else:
                open(r'D:\Python\WB\makeSkinShellPrints\errors.txt', 'a').writelines(str(x)+'\n')
                break
    time.sleep(0.6)
    print(r.text)


