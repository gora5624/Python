import pandas

from folders import pathToTopPrintFile
from createClear import createClearMain
from createCard import createCardMain

def createImage(dictToUpload):
    if dictToUpload['typeCase'] == 'cardCase':
        createCardCase(dictToUpload)
    elif dictToUpload['typeCase'] == 'mate':
        createMate(dictToUpload)
    elif dictToUpload['typeCase'] == 'clear':
        createClear(dictToUpload)
    elif dictToUpload['typeCase'] == 'skinshell':
        createSkinShell(dictToUpload)
    elif dictToUpload['typeCase'] == 'fashion':
        createFashion(dictToUpload)


def createCardCase(dictToUpload):
    countPrint = 200
    printList = [x.replace('(Принт ','print ').replace(')','.png') for x in pandas.DataFrame(pandas.read_excel(pathToTopPrintFile))[0:countPrint]['Принт'].values.tolist()]
    createCardMain(dictToUpload, printList)

def createMate(dictToUpload):
    # пока не нужно 
    pass

def createClear(dictToUpload):
    countPrint = 200
    printList = [x.replace('(Принт ','print ').replace(')','.png') for x in pandas.DataFrame(pandas.read_excel(pathToTopPrintFile))[0:countPrint]['Принт'].values.tolist()]
    createClearMain(dictToUpload, printList)

def createSkinShell(dictToUpload):
    # пока не нужно 
    pass

def createFashion(dictToUpload):
    # пока не нужно 
    pass