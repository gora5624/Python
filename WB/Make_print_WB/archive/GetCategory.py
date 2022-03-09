import os
import pandas

pathToCategory = r'G:\Картинки китай\по категориям'
pathToFileWithCategory = r'G:\Картинки китай\по категориям\Category.xlsx'


listFileCategory = []
for dir in os.listdir(pathToCategory):
    if '.xlsx' not in dir:
        listPrintIncategory = os.listdir(os.path.join(pathToCategory, dir))
        for printFile in listPrintIncategory:
            dataTMP = {'Категория': dir,
                       'Принт': printFile}
            listFileCategory.append(dataTMP)

listFileCategorypd = pandas.DataFrame(listFileCategory)
listFileCategorypd.to_excel(pathToFileWithCategory, index=False)
