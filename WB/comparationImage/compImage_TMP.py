from PIL import Image, ImageChops
import os
import requests
import io
import pickle
import time
import math, operator, functools
import multiprocessing

CREATE_PICKLE = False
LOAD_LIST = True
# pathToExcel = r"F:\Downloads\проверить Фото Абраамян.xlsx"
# refImageList = [Image.open(r"\\rab\uploads\1.jpg"), Image.open(r"\\rab\uploads\2.jpg")]
# refImage1=Image.open(r"\\rab\uploads\1.jpg")
# refImage2=Image.open(r"\\rab\uploads\2.jpg")


# def deletPhoto(vendorCode):
#     token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM5NjgxZDkxLWVmYzctNGVjOC05NzIzLTgyN2JkZTY2NWFkYyJ9.j4gqyXEe0Guzr_CbKNmFRxf_zyqjjyJ6dODc4oQII2E'
#     headers = {'Authorization': '{}'.format(token)} 
#     url = 'https://suppliers-api.wildberries.ru/content/v1/media/save'
#     json = {
#     "vendorCode": vendorCode,
#     "data": [
#     ]
#     }
#     try:
#         r = requests.post(url=url, json=json, headers=headers, timeout=10)
#     except:
#          pass
#     # print(r.text)

# if CREATE_PICKLE:
#     df = pandas.DataFrame(pandas.read_excel(pathToExcel)).to_dict('records')
#     file = open(r'D:\Python\WB\comparationImage\compImage.pkl', 'wb')
#     pickle.dump(df,file)
#     file.close()
# else:
#     file = open(r'D:\Python\WB\comparationImage\compImage.pkl', 'rb')
#     df = pickle.load(file)
#     file.close()
# if LOAD_LIST:
#     file = open(r'D:\Python\WB\comparationImage\listNoPhoto.pkl', 'rb')
#     listNoPhoto = pickle.load(file)
#     # df = pandas.DataFrame(listNoPhoto).to_excel(r'D:\tmp.xlsx')
#     file.close()
#     file = open(r'D:\Python\WB\comparationImage\listWithPhoto.pkl', 'rb')
#     listWithPhoto = pickle.load(file)
#     file.close()
# else:
#     listNoPhoto = []
#     listWithPhoto = []
pathIm = r'\\192.168.0.33\shared\_Общие документы_\Егор\_Принты книги 1000_10012024\Выбрано_Новые — копия'
pathRef = r'D:\te'
def main(imageNew):
    # for imageNew in os.listdir(pathIm):
    #     if 'db' not in imageNew:
            #imageNewIO = Image.open(os.path.join(r'D:\newPrint\выбрано',imageNew)).convert('RGB')
    imageNewIO = Image.open(os.path.join(pathIm, imageNew)).convert('RGB')
    #else:continue
    for refImage in os.listdir(pathRef):
        if 'db' not in refImage:
            refImageIO = Image.open(os.path.join(pathRef,refImage)).convert('RGB')
        #else:
                #continue
            imageNewIO = imageNewIO.resize(refImageIO.size)
            h = ImageChops.difference(refImageIO, imageNewIO).histogram()
            diff = math.sqrt(functools.reduce(operator.add, map(lambda h, i: h*(i**2), h, range(256))) / (float(refImageIO.size[0]) * refImageIO.size[1]))
            if diff >50:
                continue
            else:
                os.rename(os.path.join(pathIm,imageNew), os.path.join(pathIm,refImage))
                print(' '.join([imageNew, refImage, str(diff)]))

if __name__ == '__main__':
    pool = multiprocessing.Pool(7)
    for imageNew in os.listdir(pathIm):
        if 'db' not in imageNew:
            pool.apply_async(main, args=(imageNew,))

            # main(imageNew)
    pool.close()
    pool.join()