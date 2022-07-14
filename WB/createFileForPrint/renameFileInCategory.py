import os
import pandas

pathToCategoryFolder = r'E:\новый китай по категориям'

data = pandas.DataFrame(pandas.read_excel(r'E:\принты новые pdf\rename.xlsx'))
for dir in os.listdir(pathToCategoryFolder):
    if not os.path.isdir(os.path.join(pathToCategoryFolder,dir)):
        continue
    for file in os.listdir(os.path.join(pathToCategoryFolder,dir)):
        os.rename(os.path.join(pathToCategoryFolder,dir,file), os.path.join(pathToCategoryFolder,dir, file.replace('.pdf','.jpg')))
        # a = data.to_dict('records')
        # for i in data.to_dict('records'):
        #     if i['src'].replace(' копия.pdf','.jpg') == file:
        #         os.rename(os.path.join(pathToCategoryFolder,dir,i['src'].replace(' копия.pdf','.jpg')), os.path.join(pathToCategoryFolder,dir, i['dst']))
