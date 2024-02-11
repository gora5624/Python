# # import pandas as pd
# # import re

# # filePath = input('Введите путь в файлу')#r"F:\Downloads\9_Партия_смартфоны_ПРОИЗВОДСТВО_ВА_1.xlsx"
# # df = pd.DataFrame(pd.read_excel(filePath))
# # df.insert(2,column='ШК все',value='')
# # df.insert(2,column='Модель',value='')
# # for model in df.loc[:, 'Название 1С']:
# #     if "мат" in model:
# #        modelTMP = re.sub(r'.*9H ','',model.replace(' матовая',''))
# #     elif "глян" in model:
# #        modelTMP = re.sub(r'.*9H ','',model.replace(' глянцевая',''))
# #     df.loc[df['Название 1С']==model, ['Модель']] = modelTMP
# #     # listModels = df.loc[df['Модель']==modelTMP]['Баркод'].values.tolist()
# #     # strModels = ','.join(str(x) for x in listModels)
# #     # df.loc[df['Модель']==modelTMP, ['ШК все']] = strModels
# # for model in df.loc[:, 'Модель']:
# #     # df.loc[df['Модель']==model, ['ШК все']] = modelTMP
# #     listModels = df.loc[df['Модель']==model]['Баркод'].values.tolist()
# #     strModels = ','.join(str(x) for x in listModels)
# #     df.loc[df['Модель']==model, ['ШК все']] = strModels
# # df.to_excel(filePath.replace(r'.xlsx', r'_new.xlsx'), index=False)

# # # # # import os
# # # # # import shutil
# # # # # import pandas as pd


# # # # # path_ = r'\\192.168.0.111\shared\_Общие документы_\Буфер обмена для ПО\Принты на выбор\Выбрано'
# # # # # path_2 = r'\\192.168.0.111\shared\_Общие документы_\Буфер обмена для ПО\Принты на выбор\Новая папка'
# # # # # list_ = pd.DataFrame(pd.read_excel(r"D:\Книга1.xlsx")).to_dict('list')['Name']
# # # # # for file in os.listdir(path_):
# # # # #     if file not in list_ and 'db' not in file:
# # # # #         shutil.copy(os.path.join(path_,file), os.path.join(path_2,file))


# # # # import os
# # # # import shutil

# # # # list_0 = os.listdir(r'\\192.168.0.111\shared\_Общие документы_\Буфер обмена для ПО\Принты на выбор\Топ 200')
# # # # for i in list_0:
# # # #     shutil.copy(os.path.join(r'F:\новые принты',i.split('_')[0],i.split('_')[1].replace('png','pdf')), os.path.join(r'F:\новые принты\top_200',i.replace('png','pdf') ))


# # # import requests
# # # import pandas as pd

# # # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjNhZmUzMzMzLWFmYjEtNDI5Yi1hN2Q1LTE1Yjc4ODg4MmU5MSJ9.kWUDkHkGrtD8WxE9sQHto5B7L3bQh-XRDf7EeZQiw7A'
# # # json = {
# # #   #"targetIMT": 152838929,
# # #   "nmIDs": [
# # #     102252434
# # #   ]
# # # }
# # # url='https://suppliers-api.wildberries.ru/content/v1/cards/moveNm'
# # # headers = {'Authorization': '{}'.format(token)}
# # # json2 ={
# # #   "vendorCodes": ["iPhone_SE_2_BP_OCM_CLR_HLD_CLD_PRNT_1972"],
# # #   "allowedCategoriesOnly": True
# # # }
# # # url2='https://suppliers-api.wildberries.ru/content/v1/cards/filter'
# # # r = requests.post(url=url, json=json, headers=headers)
# # # print(r.text)
# # # r = r.json()['data']
# # # r
# # # #pd.DataFrame(r).to_excel(r'D:\tmp2.xlsx', index=False)

# # # import pandas as pd
# # # import os

# # # list_ = pd.DataFrame(pd.read_excel(r"\\192.168.0.33\shared\_Общие документы_\Егор\Все принты\SkinShell\Топ 200 без лака\имена.xlsx")).to_dict('list')

# # # for file in os.listdir(r'F:\Downloads'):
# # #     try:
# # #       nameNew = 'print ' + str(list_['new'][list_['orig'].index(file.replace('cdr','png'))]) + '.cdr'
# # #       os.rename(os.path.join(r'F:\Downloads',file), os.path.join(r'F:\Downloads',nameNew))
# # #       continue
# # #     except:
# # #         pass
# # #     try:
# # #       nameNew = 'print ' + str(list_['new'][list_['orig'].index(file.replace('_gloss.png','.png'))]) + '_gloss.png'
# # #       os.rename(os.path.join(r'F:\Downloads',file), os.path.join(r'F:\Downloads',nameNew))
# # #     except:
# # #         pass

# # # from PIL import Image
# # # import os
# # # for prPath in os.listdir(r'F:\Downloads\top_200_varnish_ready_effect\Done'):
# # #     imgBack = Image.open(r"D:\2.png")
# # #     pr = Image.open(os.path.join(r'F:\Downloads\top_200_varnish_ready_effect\Done', prPath))
# # #     pr = pr.resize((520,1141))
# # #     pr=pr.rotate(13.5,expand=True)
# # #     imgBack.paste(pr,(393,185),pr)
# # #     #imgBack.show()
# # #     imgBack.save(r'D:\test3\{}'.format(str(prPath)))

# import photoshop.api as ps
# import os

# app = ps.Application()
# app.displayDialogs = ps.DialogModes.DisplayNoDialogs
# #app.displayDialogs = ps.
# for file in os.listdir(r'D:\Новые принты на книжки'):
#     if not os.path.exists(os.path.join(r'\\rab\Диск для принтов сервак Егор\книжки новые2\Черный',file.replace('.jpg.png',''))):
#         png_doc = app.open(os.path.join(r'D:\Новые принты на книжки',file))
#         startRulerUnits = app.preferences.rulerUnits
#         if png_doc.activeLayer.kind != ps.LayerKind.TextLayer:
#             x2 = (png_doc.width * png_doc.resolution) / 2
#             y2 = png_doc.height * png_doc.resolution
#             sel_area = ((0, 0), (x2, 0), (x2, y2), (0, y2))
#             png_doc.selection.select(sel_area, ps.SelectionType.ReplaceSelection, 0, False)

#             png_doc.selection.copy()
#             app.preferences.rulerUnits = ps.Units.Pixels
#             #pasteDoc = doc.add(x2, y2, doc.resolution, "Paste Target")

#         png_doc.activeLayer = png_doc.layers[0]
#         png_doc.width
#         png_doc.height
#         png_doc.resizeImage(png_doc.width*(1195/png_doc.height) ,1195)
#         png_doc.activeLayer.copy()

#         doc = app.load(r"\\192.168.0.33\shared\_Общие документы_\Егор\книги_test.psd")
#         doc.paste()
#         png_doc.close()
#         layer_index = 3
#         doc.activeLayer = doc.layers[layer_index]
#         # doc.activeLayer.move(doc.layers[layer_index + 2], ps.ElementPlacement.PlaceBefore)
#         a = doc.activeLayer.bounds
#         x,y = 839,681
#         x2,y2 = (a[2]-a[0])/2+a[0], (a[3]-a[1])/2+a[1]
#         doc.activeLayer = doc.layers[layer_index]
#         doc.activeLayer.translate(x-x2, y-y2)
#         doc.activeLayer.resize(100,100,ps.AnchorPosition.BottomCenter)
#         # doc.selection.resize(100,100,ps.AnchorPosition.BottomCenter)

#         if startRulerUnits != app.preferences.rulerUnits:
#             app.preferences.rulerUnits = startRulerUnits

        # doc.lKayers.
        # text_color = ps.SolidColor()
        # text_color.rgb.red = 0
        # text_color.rgb.green = 255
        # text_color.rgb.blue = 0
        # # new_text_layer = new_doc
        # # new_text_layer.kind = ps.LayerKind.TextLayer
        # # new_text_layer.textItem.contents = 'Hello, World!'
        # # new_text_layer.textItem.position = [160, 167]
        # # new_text_layer.textItem.size = 40
        # # new_text_layer.textItem.color = text_color
        # options = ps.PNGSaveOptions()
        # # # # save to jpg
        # jpg = os.path.join(r'\\rab\Диск для принтов сервак Егор\книжки новые2\Черный',file.replace('.jpg.png',''))
        # doc.saveAs(jpg, options, asCopy=True)
        # doc.activeLayer.remove()
# app.doJavaScript(f'alert("save to jpg: {jpg}")')

# # # import os

# # # for i in os.listdir(r'D:\Prints'):
# # #     if 'Thumbs' not in i:
# # #         fullpathold = os.path.join(r'D:\Prints',i)
# # #         a = int(i.split('.')[0])
# # #         newName = str(4200+int(i.split('.')[0]))+'.'+i.split('.')[1].replace('_label','')+'.png'
# # #         fullpathnew = os.path.join(r'D:\Prints',newName)
# # #         os.rename(fullpathold,fullpathnew)

# # from PIL import Image
# # import numpy as np

# # # Загрузите изображение
# # image = Image.open(r"D:\Case\Чехол Honor X5 силикон с зак.кам. черный противоуд. SkinShell\1_clown.png")

# # # Получите цвет пикселя по координатам x, y
# # x = 1
# # y = 1
# # color = image.getpixel((x, y))

# # # Преобразуйте изображение в массив
# # data = np.array(image)

# # # Создайте маску с тем же цветом по координатам x, y
# # mask = np.full(data.shape, color)

# # # Найдите все пиксели, где цвет пикселя совпадает с mask
# # result = (data == mask).all(-1)

# # # Преобразуйте результат обратно в изображение
# # new_image = Image.fromarray(np.uint8(result * 255) , 'L')

# # # Сохраните новое изображение
# # new_image.show()


# # import os

# # path_ = r'\\192.168.0.111\shared\Отдел производство\newPrint2\SVG'
# # for i in os.listdir(path_):
# #     if not os.path.isdir(os.path.join(path_,i)):
# #         newI = 'print_' + str(int(i.replace('print_','').replace('_edge','').replace(i[-4:],'')) + 227) + '_edge' +i[-4:]
# #         os.rename(os.path.join(path_,i),os.path.join(path_, newI))
# import requests
# import time
# import pandas as pd
# token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImU4NjQ1YWI5LWFjM2UtNGFkOS1hYmIyLThkMTMzMGM1YTU3NyJ9.8nz9gIHurlCVKIhruG6hY8MRBtMLvLYggVzisxgKivY'
# headers = {'Authorization': '{}'.format(token)} 
# url = 'https://suppliers-api.wildberries.ru/api/v3/stocks/10237'
# df = pd.DataFrame(pd.read_excel(r"\\rab\Диск для принтов сервак Егор\для 1с\Чехол производство создать — копия.xlsx"))
# list_ = df['Баркод'].to_list()
# for i in range(0,len(list_),1000):
#     json = {
# "skus": [
# str(x) for x in list_[i:i+1000]
# ]
# }
#     r = requests.delete(url=url, json=json, headers=headers, timeout=10)
#     print(r.status_code)
#     time.sleep(0.2)
# import requests
# import time
# token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImU4NjQ1YWI5LWFjM2UtNGFkOS1hYmIyLThkMTMzMGM1YTU3NyJ9.8nz9gIHurlCVKIhruG6hY8MRBtMLvLYggVzisxgKivY'
# headers = {'Authorization': '{}'.format(token)} 
# url = 'https://suppliers-api.wildberries.ru/content/v1/media/save'
# json = {
#   "vendorCode": "Xiaomi_Redmi_Note_10_Pro_BP_CLR_HLD_ANI_PRNT_3591",
#   "data": [
#   ]
# }
# r = requests.post(url=url, json=json, headers=headers, timeout=10)
# print(r.text)

# from PIL import Image, ImageChops
# import math, operator, functools

# def rmsdiff(im1, im2):
#     "Calculate the root-mean-square difference between two images"

#     h = ImageChops.difference(im1, im2).histogram()

#     # calculate rms
#     return math.sqrt(functools.reduce(operator.add,
#         map(lambda h, i: h*(i**2), h, range(256))
#     ) / (float(im1.size[0]) * im1.size[1]))

# im1 = Image.open(r"\\rab\uploads\2.webp")
# im2 = Image.open(r"\\rab\uploads\1.jpg")
# print(rmsdiff(im1, im2))


# import os
# import shutil
# import pandas

# pathToPront = r'\\rab\Диск для принтов сервак Егор\книжки новые\Черный'
# df = pandas.read_excel(r"\\192.168.0.33\shared\_Общие документы_\Егор\Top200_New\Принты_ТОП200_Книги_NEW.xlsx").to_dict('records')
# for i, image in enumerate(df):
#     fileName = image['Принт'].replace('(Принт ', 'print ').replace(')','.png')
#     if fileName in os.listdir(pathToPront):
#         shutil.copy(os.path.join(pathToPront, fileName), os.path.join(r"\\192.168.0.33\shared\_Общие документы_\Егор\Top200_New", str(i)+'.png'))
        # os.rename()

# import pandas
# import os


# def main():
    # mainPath = r'\\rab\Диск для принтов сервак Егор\для 1с — копия'
    # data = pandas.read_excel(r"\\rab\Диск для принтов сервак Егор\Маски силикон\карточки.xlsx")
    # for file in os.listdir(mainPath):
    #     if '.xlsx' in file:
    #         df = pandas.read_excel(os.path.join(mainPath, file))
    #         # data2 = data.loc['Артикул продавца' == df['Артикул товара']]
    #         df
    #         dfNew = df.merge(data, how='left', left_on='Артикул товара', right_on='Артикул продавца')
    # #         dfNew.to_excel(os.path.join(r'\\rab\Диск для принтов сервак Егор\для 1с',file),index=False)

    # pathToDB = r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\ШК.txt"
    # pathToDB = pandas.read_table(pathToDB)
    # cards = pandas.read_excel(r"\\rab\Диск для принтов сервак Егор\Маски силикон\карточки.xlsx")
    # new = cards.merge(pathToDB, how='left', left_on='Баркод', right_on='Штрихкод') 
    # # fashionList = pdBarcodes[pdBarcodes['Номенклатура'].str.lower().str.contains('fashion')]
    # new.to_excel(r'F:\new.xlsx', index=False)
    # pandas.read_excel(r"F:\Первая возна на зануление.xlsx").to_excel(r"F:\Первая возна на зануление2.xlsx")

# main()


