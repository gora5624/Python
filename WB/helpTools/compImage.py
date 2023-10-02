from PIL import Image, ImageChops
import pandas
import requests
import io
import pickle
import time
import math, operator, functools

CREATE_PICKLE = False
LOAD_LIST = True
pathToExcel = r"F:\Downloads\книжки.xlsx"
refImage1=Image.open(r"\\rab\uploads\1.jpg")
refImage2=Image.open(r"\\rab\uploads\2.jpg")


def deletPhoto(vendorCode):
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImU4NjQ1YWI5LWFjM2UtNGFkOS1hYmIyLThkMTMzMGM1YTU3NyJ9.8nz9gIHurlCVKIhruG6hY8MRBtMLvLYggVzisxgKivY'
    headers = {'Authorization': '{}'.format(token)} 
    url = 'https://suppliers-api.wildberries.ru/content/v1/media/save'
    json = {
    "vendorCode": vendorCode,
    "data": [
    ]
    }
    try:
        r = requests.post(url=url, json=json, headers=headers, timeout=10)
    except:
         pass
    # print(r.text)

if CREATE_PICKLE:
    df = pandas.DataFrame(pandas.read_excel(pathToExcel)).to_dict('records')
    file = open(r'D:\Python\WB\helpTools\compImage.pkl', 'wb')
    pickle.dump(df,file)
    file.close()
else:
    file = open(r'D:\Python\WB\helpTools\compImage.pkl', 'rb')
    df = pickle.load(file)
    file.close()
if LOAD_LIST:
    file = open(r'D:\Python\WB\helpTools\listNoPhoto.pkl', 'rb')
    listNoPhoto = pickle.load(file)
    # df = pandas.DataFrame(listNoPhoto).to_excel(r'D:\tmp.xlsx')
    file.close()
    file = open(r'D:\Python\WB\helpTools\listWithPhoto.pkl', 'rb')
    listWithPhoto = pickle.load(file)
    file.close()
else:
    listNoPhoto = []
    listWithPhoto = []
for urls in df:#['Медиафайлы'].to_list():
    listNo = [i['Артикул продавца'] for i in listNoPhoto]
    listWith = [i['Артикул продавца'] for i in listWithPhoto]
    if (urls['Артикул продавца'] not in list(listNo)) and (urls['Артикул продавца'] not in list(listWith)):
        link = urls['Медиафайлы']
        #link = 'https://basket-07.wb.ru/vol1084/part108448/108448230/images/big/1.webp'
        barcode = urls['Баркод товара']
        try:
            stuffImage = io.BytesIO((r:=requests.get(link)).content)
        except:
            continue
        # print(str(r.status_code) + ' ' + str(barcode))
        stuffImage=Image.open(stuffImage)
        h = ImageChops.difference(refImage1, stuffImage).histogram()
        diff = math.sqrt(functools.reduce(operator.add, map(lambda h, i: h*(i**2), h, range(256))) / (float(refImage1.size[0]) * refImage1.size[1]))
        if diff >1:
            h = ImageChops.difference(refImage2, stuffImage).histogram()
            diff = math.sqrt(functools.reduce(operator.add, map(lambda h, i: h*(i**2), h, range(256))) / (float(refImage2.size[0]) * refImage2.size[1]))
        else:
            listWithPhoto.append(urls)
        if diff <1:
            print(urls['Баркод товара'])
            # if urls not in listNoPhoto:
            listNoPhoto.append(urls)
            deletPhoto(urls['Артикул продавца'])
            file = open(r'D:\Python\WB\helpTools\listNoPhoto.pkl', 'wb')
            pickle.dump(listNoPhoto,file)
            file.close()
        else:
            listWithPhoto.append(urls)
            file = open(r'D:\Python\WB\helpTools\listWithPhoto.pkl', 'wb')
            pickle.dump(listWithPhoto,file)
            file.close()
        time.sleep(1)