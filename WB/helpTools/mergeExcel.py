import os
import pandas

mainPath = r'E:\Downloads\report_2023_5_3.xlsx'
df = pandas.DataFrame()
for file in os.listdir(mainPath):
    if not os.path.isdir(os.path.join(mainPath,file)):
        tmp = pandas.DataFrame(pandas.read_excel(os.path.join(mainPath, file)))
        try:
            tmp['Медиафайлы'] = tmp['Медиафайлы'].astype(str)
        except:
            pass
        df = pandas.concat([tmp, df], ignore_index=True, sort=False)
with pandas.ExcelWriter(os.path.join(mainPath, 'tmp.xlsx'), engine='xlsxwriter',options={'strings_to_urls': False}) as xlsxFile:
    df.to_excel(xlsxFile, index=False)

# df.to_csv(os.path.join(mainPath, 'tmp.txt'), index=False, sep='\t')
    # df.to_excel(os.path.join(mainPath, 'tmp.xlsx'), index=False)