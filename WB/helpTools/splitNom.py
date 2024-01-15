import requests
import pandas as pd
import time
import pickle
# listCardsPath = r"F:\Downloads\report_2023_8_17.xlsx\tmp.xlsx"
listCardsPath = r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db\DB_card Манвел.txt"
# dfFull = pd.DataFrame(pd.read_excel(listCardsPath))
dfFull = pd.DataFrame(pd.read_table(listCardsPath))
dfCase = dfFull#[dfFull['Предмет']=='Чехлы для телефонов']
dfBrand= dfCase#[dfCase['Бренд']=='Mobi114']
try:
    file = open(r'D:\Python\WB\makeSkinShellPrints\listNom.pkl', 'rb')
    listNom = pickle.load(file)
    file.close()
except:
    listNom = dfFull['Номенклатура'].unique().tolist()
    file = open(r'D:\Python\WB\makeSkinShellPrints\listNom.pkl', 'wb')
    pickle.dump(listNom, file)
    file.close()
url = 'https://suppliers-api.wildberries.ru/content/v1/cards/moveNm'
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM5NjgxZDkxLWVmYzctNGVjOC05NzIzLTgyN2JkZTY2NWFkYyJ9.j4gqyXEe0Guzr_CbKNmFRxf_zyqjjyJ6dODc4oQII2E'
headers = {'Authorization': '{}'.format(token)} 
try:
    file = open(r'D:\Python\WB\makeSkinShellPrints\done.pkl', 'rb')
    listDone = pickle.load(file)

    file.close()
except:
    listDone = []
try:
    file = open(r'D:\Python\WB\makeSkinShellPrints\errors.pkl', 'rb')
    listErrors = pickle.load(file)
    file.close()
except:
        listErrors = []
for nom in listNom:
    dfNom = dfFull[dfFull['Номенклатура']==nom]
    dfNom.sort_values(by=['vendorCode'], inplace=True,kind='stable')
    dfNom = dfNom[~dfNom['nmID'].isin(listDone)]
    listArtVendor = dfNom['nmID'].values.tolist()
    for i in range(0,len(listArtVendor),30):
        countTry = 0
        while True:
            x = listArtVendor[i:i+30]
            json = {
                'nmIDs':x
            }
            try:
                r = requests.post(url=url, json=json, headers=headers, timeout=10)
                if r.status_code == 200:
                    listDone.extend(x)
                    file = open(r'D:\Python\WB\makeSkinShellPrints\done.pkl', 'wb')
                    pickle.dump(listDone, file)
                    file.close()
                elif r.status_code == 400 and "Все карточки находятся в одной группе" in r.text:
                    listDone.extend(x)
                    file = open(r'D:\Python\WB\makeSkinShellPrints\done.pkl', 'wb')
                    pickle.dump(listDone, file)
                    file.close()
                else:
                    file = open(r'D:\Python\WB\makeSkinShellPrints\errors.pkl', 'wb')
                    listErrors.extend(x)
                    pickle.dump(listErrors, file)
                    file.close()
                break
            except:
                countTry+=1
                if countTry <10:
                    continue
                else:
                    file = open(r'D:\Python\WB\makeSkinShellPrints\errors.pkl', 'wb')
                    listErrors.extend(x)
                    pickle.dump(listErrors, file)
                    file.close()
                    break
        time.sleep(60)
        print(r.text)


