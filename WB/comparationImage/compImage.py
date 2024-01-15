from PIL import Image, ImageChops
import pandas
import requests
import io
import pickle
import time
import math, operator, functools

CREATE_PICKLE = False
LOAD_LIST = True
pathToExcel = r"F:\Downloads\проверить Фото Абраамян.xlsx"
refImageList = [Image.open(r"\\rab\uploads\1.jpg"), Image.open(r"\\rab\uploads\2.jpg")]
# refImage1=Image.open(r"\\rab\uploads\1.jpg")
# refImage2=Image.open(r"\\rab\uploads\2.jpg")


def deletPhoto(vendorCode):
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM5NjgxZDkxLWVmYzctNGVjOC05NzIzLTgyN2JkZTY2NWFkYyJ9.j4gqyXEe0Guzr_CbKNmFRxf_zyqjjyJ6dODc4oQII2E'
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
    file = open(r'D:\Python\WB\comparationImage\compImage.pkl', 'wb')
    pickle.dump(df,file)
    file.close()
else:
    file = open(r'D:\Python\WB\comparationImage\compImage.pkl', 'rb')
    df = pickle.load(file)
    file.close()
if LOAD_LIST:
    file = open(r'D:\Python\WB\comparationImage\listNoPhoto.pkl', 'rb')
    listNoPhoto = pickle.load(file)
    # df = pandas.DataFrame(listNoPhoto).to_excel(r'D:\tmp.xlsx')
    file.close()
    file = open(r'D:\Python\WB\comparationImage\listWithPhoto.pkl', 'rb')
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
        if r.status_code != 404:
            stuffImage=Image.open(stuffImage)
        else:
            print(urls['Баркод товара'])
            # if urls not in listNoPhoto:
            listNoPhoto.append(urls)
            deletPhoto(urls['Артикул продавца'])
            file = open(r'D:\Python\WB\helpTools\listNoPhoto.pkl', 'wb')
            pickle.dump(listNoPhoto,file)
            file.close()
            continue
        for refImage in refImageList:
            h = ImageChops.difference(refImage, stuffImage).histogram()
            diff = math.sqrt(functools.reduce(operator.add, map(lambda h, i: h*(i**2), h, range(256))) / (float(refImage.size[0]) * refImage.size[1]))
            if diff >1:
                continue
            else:
                print(urls['Баркод товара'])
                # if urls not in listNoPhoto:
                listNoPhoto.append(urls)
                deletPhoto(urls['Артикул продавца'])
                file = open(r'D:\Python\WB\helpTools\listNoPhoto.pkl', 'wb')
                pickle.dump(listNoPhoto,file)
                file.close()
                break
        if diff >1:
            listWithPhoto.append(urls)
            file = open(r'D:\Python\WB\helpTools\listWithPhoto.pkl', 'wb')
            pickle.dump(listWithPhoto,file)
            file.close()
    time.sleep(1)