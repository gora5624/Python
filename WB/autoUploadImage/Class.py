import os
import pandas
import pickle
from multiprocessing import Process, Queue, cpu_count
from folders import pathToFolderForPhotoToUploads, listPathToXLSX, pathToTopPrintFile
from createClear import createClearMain
from createCard import createCardMain
from uploadImage import updatePhotoMain
import shutil

def scanFolder(listToken):
    listForUploads = []
    # [{'Путь':'','ИП','','Тип товара',''},{}]
    for dir_ in os.listdir(pathToFolderForPhotoToUploads):
        tmpDict = {'pathToFolder':os.path.join(pathToFolderForPhotoToUploads, dir_), 'dirName': dir_, 'listXLSX':'', 'Seller':'','typeCase':'', 'token': ''}
        seller = getSeller(dir_)
        token = listToken[seller]
        if 'под карту' in dir_.lower():
            typeCase = 'cardCase'
            listXSLX = findXLSX(dir_, typeCase)
            tmpDict.update({'typeCase':typeCase, 'listXLSX': listXSLX, 'Seller': seller, 'token': token})
            listForUploads.append(tmpDict)
        elif 'матовый' in dir_.lower():
            typeCase = 'mate'
            listXSLX = findXLSX(dir_, typeCase)
            tmpDict.update({'typeCase':typeCase, 'listXLSX': listXSLX, 'Seller': seller})
            listForUploads.append(tmpDict)
        elif 'fashion' in dir_.lower():
            typeCase = 'fashion'
            listXSLX = findXLSX(dir_, typeCase)
            tmpDict.update({'typeCase':typeCase, 'listXLSX': listXSLX, 'Seller': seller})
            listForUploads.append(tmpDict)
        elif ' проз' in dir_.lower():
            typeCase = 'clear'
            listXSLX = findXLSX(dir_, typeCase)
            tmpDict.update({'typeCase':typeCase, 'listXLSX': listXSLX, 'Seller': seller})
            listForUploads.append(tmpDict)
        elif 'skinshell' in dir_.lower():
            typeCase = 'skinshell'
            listXSLX = findXLSX(dir_, typeCase)
            tmpDict.update({'typeCase':typeCase, 'listXLSX': listXSLX, 'Seller': seller})
            listForUploads.append(tmpDict)

    return listForUploads


def findXLSX(dir_, typeCase):
    listXLSX = []
    listPathToSearch = listPathToXLSX[typeCase]
    for path_ in listPathToSearch:
        if os.path.exists(tmp:=os.path.join(path_, dir_ + '.xlsx')):
            listXLSX.append(tmp)
    return listXLSX


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
    pass


def uploadXLSX(listToUpload):
    updatePhotoMain(listToUpload)

def createCardCase(dictToUpload):
    countPrint = 200
    printList = [x.replace('(Принт ','print ').replace(')','.png') for x in pandas.DataFrame(pandas.read_excel(pathToTopPrintFile))[0:countPrint]['Принт'].values.tolist()]
    createCardMain(dictToUpload, printList)

def createMate(dictToUpload):
    pass

def createClear(dictToUpload):
    countPrint = 200
    printList = [x.replace('(Принт ','print ').replace(')','.png') for x in pandas.DataFrame(pandas.read_excel(pathToTopPrintFile))[0:countPrint]['Принт'].values.tolist()]
    createClearMain(dictToUpload, printList)

def createSkinShell(dictToUpload):
    pass

def createFashion(dictToUpload):
    pass

def getSeller(dir_):
    return 'Караханян'

def getTokenList():
    return pickle.load(open(os.path.abspath(os.path.join(__file__, '..', r'token.pkl')), 'rb'))

def relocateFile(path):
    shutil.copytree(path, os.path.join(r'\\192.168.0.33\shared\_Общие документы_\_Фото\Выставлено прогой', a:=os.path.basename(path)))
    a

def saveToken():
    tmp = {
    'Караханян':'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njg4MiwiaWQiOiI4YjEzZWUzOC03MGIxLTQ3ZjgtYTdlNC03OTIzY2Q2ZmQ3ZTciLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjEwMTA2MiwicyI6MTAsInNpZCI6IjNhOTNkZGMxLWFhNTctNWMyYi05YzVjLWRkZDIyMTg4OTQ0MCIsInVpZCI6NDUzMjI5MjB9.DXm6RuooUieyrnNdXr3FfPPdwK5uV4aiTF5SZIryJUhbQW4uScXQLEb-n8p0iM3RT6Js6aVKijiyOkawE6r76g',
    'Абраамян':'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njk1MSwiaWQiOiIyMzUyZGFmYS05NTdhLTQ0MzAtYWFhMi1lZGM5NDZkZDY0ODEiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjUyNzczNiwicyI6MTAsInNpZCI6ImFhNDdlNDg5LTU5ZTAtNDIzMi1hMWJmLTBlMTIzOWYwNDJmMSIsInVpZCI6NDUzMjI5MjB9.j9s_VtDpTEWceEd1vUTWf6uofUuSY30q0UrR-H047qZE40sb8atwtAviABB7eoeLQdu3T69UosBdn_Bvj2-2ZQ',   
    'Самвел':'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njk3MiwiaWQiOiJjZWE4ZTNmYy1iYzg5LTRjYjktYmNmNy0xN2ZiNmNjNzk1MTQiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjgxOTI0NiwicyI6MTAsInNpZCI6IjBhYjhiMTA1LTA1MWYtNGVkNi04NzBiLTM5OWU3NWUxMDI4NiIsInVpZCI6NDUzMjI5MjB9.bOmPtl_ZXx-1C25-5CbftPJVQuuHzwG5iH9QUx0x8CdZCjI9ZnbFgMU1ijL-lfgn_N1JxPvojV2dBrKTpDnolw',
    'Иван':'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5NzAwNywiaWQiOiI1ZWRjMWY0Ni04OWVhLTQxMzktYjVjYi1hNDM5OGUwMzUxNTMiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjExNzEwNDQsInMiOjEwLCJzaWQiOiJkOWU0OGUxZi05ZjgxLTQ1MmMtODRiYy05ZGYxZWRiMzNmNDkiLCJ1aWQiOjQ1MzIyOTIwfQ.y2sbT8zqvoM-iSxKJcsdiEphMoLRfNq8pBsIQnmGQIbc1btCIoe7Qkz65Ur91fVEqyDbQZ-Ry_1tTkgof5hKDw'
    }
    pickle.dump(tmp, open(os.path.abspath(os.path.join(__file__, '..', r'token.pkl')), 'wb'))
# saveToken()
# listForUploads = scanFolder()