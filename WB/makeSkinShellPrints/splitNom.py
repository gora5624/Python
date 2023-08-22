import requests
import pandas as pd
import time
import pickle

listCardsPath = r"F:\Downloads\report_2023_8_17.xlsx\tmp.xlsx"
listCardsPath = r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Манвел.txt"
# dfFull = pd.DataFrame(pd.read_excel(listCardsPath))
dfFull = pd.DataFrame(pd.read_table(listCardsPath))
dfCase = dfFull#[dfFull['Предмет']=='Чехлы для телефонов']
dfBrand= dfCase#[dfCase['Бренд']=='Mobi114']
dfBrand.sort_values(by=['vendorCode'], inplace=True,kind='stable')
listArtVendor = dfBrand['nmID'].values.tolist()
url = 'https://suppliers-api.wildberries.ru/content/v1/cards/moveNm'
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM5NjgxZDkxLWVmYzctNGVjOC05NzIzLTgyN2JkZTY2NWFkYyJ9.j4gqyXEe0Guzr_CbKNmFRxf_zyqjjyJ6dODc4oQII2E'
headers = {'Authorization': '{}'.format(token)} 

try:
    with open(r'D:\Python\WB\makeSkinShellPrints\done.pkl', 'rb') as file:
        listDone = pickle.load(file)
        file.close()
except:
    listDone = []
for done in listDone:
    listArtVendor.remove(done)
try:
    with open(r'D:\Python\WB\makeSkinShellPrints\done.pkl', 'wb') as file:
        for i in range(0,len(listArtVendor),1):
            countTry = 0
            while True:
                x = listArtVendor[i:i+1]
                json = {
                    'nmIDs':x
                }
                try:
                    r = requests.post(url=url, json=json, headers=headers, timeout=10)
                    listDone.extend(x)
                    pickle.dump(listDone, file)
                    # file.close()
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
        file.close()
except:
    file.close()


