from logging.config import dictConfig
import os
import pandas


startCount = 3134
pathToRename = r'E:\принты новые pdf'

listTMP = []
for i, file in enumerate(os.listdir(pathToRename)):
    dictTmp = {'src':file,
                'dst': "print {}.pdf".format(str(startCount + i))}
    os.rename(os.path.join(pathToRename, file), os.path.join(pathToRename,"print {}.pdf".format(str(startCount + i))))
    listTMP.append(dictTmp)

pd = pandas.DataFrame(listTMP)
pd.to_excel(os.path.join(pathToRename, r'rename.xlsx'))
