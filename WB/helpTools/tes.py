# from ast import Import
# import pandas as pd
# from os.path import basename
# import re

# filePath = r"F:\Downloads\Стекло производство 8.xlsx"
# df = pd.DataFrame(pd.read_excel(filePath))
# df.insert(2,column='ШК все',value='')
# df.insert(2,column='Модель',value='')
# for model in df.loc[:, 'Название 1С']:
#     if "мат" in model:
#        modelTMP = re.sub(r'.*9H ','',model.replace(' матовая',''))
#     elif "глян" in model:
#        modelTMP = re.sub(r'.*9H ','',model.replace(' глянцевая',''))
#     df.loc[df['Название 1С']==model, ['Модель']] = modelTMP
#     # listModels = df.loc[df['Модель']==modelTMP]['Баркод'].values.tolist()
#     # strModels = ','.join(str(x) for x in listModels)
#     # df.loc[df['Модель']==modelTMP, ['ШК все']] = strModels
# for model in df.loc[:, 'Модель']:
#     # df.loc[df['Модель']==model, ['ШК все']] = modelTMP
#     listModels = df.loc[df['Модель']==model]['Баркод'].values.tolist()
#     strModels = ','.join(str(x) for x in listModels)
#     df.loc[df['Модель']==model, ['ШК все']] = strModels
# df.to_excel(filePath.replace(r'.xlsx', r'_new.xlsx'), index=False)

# # # import os
# # # import shutil
# # # import pandas as pd


# # # path_ = r'\\192.168.0.111\shared\_Общие документы_\Буфер обмена для ПО\Принты на выбор\Выбрано'
# # # path_2 = r'\\192.168.0.111\shared\_Общие документы_\Буфер обмена для ПО\Принты на выбор\Новая папка'
# # # list_ = pd.DataFrame(pd.read_excel(r"D:\Книга1.xlsx")).to_dict('list')['Name']
# # # for file in os.listdir(path_):
# # #     if file not in list_ and 'db' not in file:
# # #         shutil.copy(os.path.join(path_,file), os.path.join(path_2,file))


# # import os
# # import shutil

# # list_0 = os.listdir(r'\\192.168.0.111\shared\_Общие документы_\Буфер обмена для ПО\Принты на выбор\Топ 200')
# # for i in list_0:
# #     shutil.copy(os.path.join(r'F:\новые принты',i.split('_')[0],i.split('_')[1].replace('png','pdf')), os.path.join(r'F:\новые принты\top_200',i.replace('png','pdf') ))


# import requests
# import pandas as pd

# token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjNhZmUzMzMzLWFmYjEtNDI5Yi1hN2Q1LTE1Yjc4ODg4MmU5MSJ9.kWUDkHkGrtD8WxE9sQHto5B7L3bQh-XRDf7EeZQiw7A'
# json = {
#   #"targetIMT": 152838929,
#   "nmIDs": [
#     102252434
#   ]
# }
# url='https://suppliers-api.wildberries.ru/content/v1/cards/moveNm'
# headers = {'Authorization': '{}'.format(token)}
# json2 ={
#   "vendorCodes": ["iPhone_SE_2_BP_OCM_CLR_HLD_CLD_PRNT_1972"],
#   "allowedCategoriesOnly": True
# }
# url2='https://suppliers-api.wildberries.ru/content/v1/cards/filter'
# r = requests.post(url=url, json=json, headers=headers)
# print(r.text)
# r = r.json()['data']
# r
# #pd.DataFrame(r).to_excel(r'D:\tmp2.xlsx', index=False)

# import pandas as pd
# import os

# list_ = pd.DataFrame(pd.read_excel(r"\\192.168.0.33\shared\_Общие документы_\Егор\Все принты\SkinShell\Топ 200 без лака\имена.xlsx")).to_dict('list')

# for file in os.listdir(r'F:\Downloads'):
#     try:
#       nameNew = 'print ' + str(list_['new'][list_['orig'].index(file.replace('cdr','png'))]) + '.cdr'
#       os.rename(os.path.join(r'F:\Downloads',file), os.path.join(r'F:\Downloads',nameNew))
#       continue
#     except:
#         pass
#     try:
#       nameNew = 'print ' + str(list_['new'][list_['orig'].index(file.replace('_gloss.png','.png'))]) + '_gloss.png'
#       os.rename(os.path.join(r'F:\Downloads',file), os.path.join(r'F:\Downloads',nameNew))
#     except:
#         pass

# from PIL import Image
# import os
# for prPath in os.listdir(r'F:\Downloads\top_200_varnish_ready_effect\Done'):
#     imgBack = Image.open(r"D:\2.png")
#     pr = Image.open(os.path.join(r'F:\Downloads\top_200_varnish_ready_effect\Done', prPath))
#     pr = pr.resize((520,1141))
#     pr=pr.rotate(13.5,expand=True)
#     imgBack.paste(pr,(393,185),pr)
#     #imgBack.show()
#     imgBack.save(r'D:\test3\{}'.format(str(prPath)))

import photoshop.api as ps


app = ps.Application()
app.displayDialogs = ps.DialogModes.DisplayNoDialogs
#app.displayDialogs = ps.
png_doc = app.open(r"D:\newPrint\print 5001.png")
# startRulerUnits = app.preferences.rulerUnits
# if png_doc.activeLayer.kind != ps.LayerKind.TextLayer:
#     x2 = (png_doc.width * png_doc.resolution) / 2
#     y2 = png_doc.height * png_doc.resolution
#     sel_area = ((0, 0), (x2, 0), (x2, y2), (0, y2))
#     png_doc.selection.select(sel_area, ps.SelectionType.ReplaceSelection, 0, False)

#     png_doc.selection.copy()
#     app.preferences.rulerUnits = ps.Units.Pixels
#     #pasteDoc = doc.add(x2, y2, doc.resolution, "Paste Target")

png_doc.activeLayer = png_doc.layers[0]
png_doc.width
png_doc.height
png_doc.resizeImage(png_doc.width*(1277/png_doc.height) ,1277)
png_doc.activeLayer.copy()

doc = app.load(r"\\192.168.0.33\shared\_Общие документы_\Егор\книги_test.psd")
doc.paste()
png_doc.close()
layer_index = 1
doc.activeLayer = doc.layers[layer_index]
doc.activeLayer.move(doc.layers[layer_index + 2], ps.ElementPlacement.PlaceBefore)
a = doc.activeLayer.bounds
x,y = 371,669
x2,y2 = (a[2]-a[0])/2+a[0], (a[3]-a[1])/2+a[1]
doc.activeLayer.translate(x-x2, y-y2)
# doc.activeLayer.resize(100,100,ps.AnchorPosition.BottomCenter)
# doc.selection.resize(100,100,ps.AnchorPosition.BottomCenter)

# if startRulerUnits != app.preferences.rulerUnits:
#     app.preferences.rulerUnits = startRulerUnits





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
# options = ps.JPEGSaveOptions(quality=5)
# # # save to jpg
# jpg = 'd:/hello_world.jpg'
# # doc.saveAs(jpg, options, asCopy=True)
# app.doJavaScript(f'alert("save to jpg: {jpg}")')