import os
import pandas

dataFromWB = pandas.DataFrame(pandas.read_csv(r'E:\tmp.txt',sep='\t'))
# dataFromWB.to_csv(r'F:\Downloads\report_2022_10_1\tmp.txt',index=None,sep='\t')
dataBarcodes = pandas.DataFrame(pandas.read_table(r'C:\Users\Георгий\Desktop\ШК.txt'))
modelsList = os.listdir(r'F:\Для загрузки\Готовые принты\Силикон')

for model in modelsList:
    dataTMP = []
    listBarcodModel = dataBarcodes[dataBarcodes.Номенклатура == model+'.']
    listBarcodModel
    for line in listBarcodModel.to_dict('recodrs'):
        if line['Характеристика']!= '(Принт 0)':
            data = {
                'Артикул товара':dataFromWB[dataFromWB.Баркод == line['Штрихкод']]['Артикул поставщика'].values.tolist()[0],
                'Медиафайлы': 'http://95.78.233.163:8001/wp-content/uploads/Готовые принты/Силикон/{}/{}.jpg'.format(model, line['Характеристика'])
            }
            dataTMP.append(data)
    pd = pandas.DataFrame(dataTMP)
    pd.to_excel(os.path.join(r'F:\Для загрузки\Готовые принты\Силикон',model + '.xlsx'), index=False)