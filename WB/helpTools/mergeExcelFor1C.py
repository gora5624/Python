from genericpath import isdir
import os
import pandas

mainPath = r'\\rab\Диск для принтов сервак Егор\для 1с'
df = pandas.DataFrame()
dbNodenclatures = pandas.DataFrame(pandas.read_table(r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\Список стандартный поиск номенклатура.txt'))
data = []
for file in os.listdir(mainPath):
    if not isdir(os.path.join(mainPath, file)):
        tmp = pandas.DataFrame(pandas.read_excel(os.path.join(mainPath, file)))
        # print(file[len(file.replace('.xlsx',''))-4:].replace('.xlsx',''))
        for line in tmp.to_dict('records'):
            if file[len(file.replace('.xlsx',''))-4:].replace('.xlsx','') == 'проз':
                # a = file.replace('.xlsx','').replace('проз','проз.')
                # a = a.replace('проз','проз.')
                name = file.replace('.xlsx','').replace('проз','проз.')
            elif file[len(file.replace('.xlsx',''))-3:].replace('.xlsx','') == 'мат':
                name = file.replace('.xlsx','').replace('мат','мат.')
            else:
                name = file.replace('.xlsx','')
            try:
                fullName = dbNodenclatures[dbNodenclatures['Наименование'] == name]['Наименование для печати'].values.tolist()[0]
                size = dbNodenclatures[dbNodenclatures['Наименование'] == name]['Размер чехла'].values.tolist()[0]
            except:
                fullName = name
                for word in [('зак.кам.','закрытой камерой'), ('отк.кам.','открытой камерой'), ('проз.','прозрачный'), ('мат.','матовый')]:
                    fullName = fullName.replace(word[0],word[1])
                size = ''
            dataTMP = {
                'Баркод':line['Баркод товара'],
                'Группа':'Чехол производство (принт)',
                'Основная характеристика':line['Принт'],
                'Название 1С':name,
                'Название полное':fullName,
                'Размер Печать':size
            }
            data.append(dataTMP)
#with pandas.ExcelWriter(os.path.join(mainPath, 'tmp.xlsx'), engine='xlsxwriter',options={'strings_to_urls': False}) as xlsxFile:
    #df.to_excel(xlsxFile, index=False)
datadf = pandas.DataFrame(data)
datadf.to_excel(os.path.join(mainPath, 'Чехол производство создать.xlsx'), index=False)
# df.to_csv(os.path.join(mainPath, 'tmp.txt'), index=False, sep='\t')
    # df.to_excel(os.path.join(mainPath, 'tmp.xlsx'), index=False)