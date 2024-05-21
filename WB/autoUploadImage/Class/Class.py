import os
import shutil

from folders import pathToFolderForPhotoToUploads, listPathToXLSX, pathToDoneCase
from network.uploadImage import updatePhotoMain

def scanFolder(listToken):
    listForUploads = []
    # [{'Путь':'','ИП','','Тип товара',''},{}]
    for dir_ in os.listdir(pathToFolderForPhotoToUploads):
        tmpDict = {
            'pathToFolder': os.path.join(pathToFolderForPhotoToUploads, dir_), 
            'dirName': dir_, 
            'listXLSX': '', 
            'Seller': '', 
            'typeCase': '', 
            'token': ''
        }
        seller = getSeller(dir_)
        token = listToken[seller]
        typeCase, listXSLX = identifyTypeAndXLSX(dir_, seller)
        tmpDict.update({'typeCase':typeCase, 'listXLSX': listXSLX, 'Seller': seller, 'token': token})
        listForUploads.append(tmpDict)

    return listForUploads


def identifyTypeAndXLSX(dir_, seller):
    conditions = {
        'cardCase': 'под карту',
        'mate': 'матовый',
        'fashion': 'fashion',
        'clear': ' проз',
        'skinshell': 'skinshell'
    }
    for type_case, condition in conditions.items():
        if condition in dir_.lower():
            list_xlsx = findXLSX(dir_, type_case)
            return type_case, list_xlsx
    return '', []


def findXLSX(dir_, typeCase):
    listXLSX = []
    for path_ in listPathToXLSX[typeCase]:
        if os.path.exists(tmp:=os.path.join(path_, dir_ + '.xlsx')):
            listXLSX.append(tmp)
    return listXLSX



def uploadXLSX(listToUpload):
    updatePhotoMain(listToUpload)


def getSeller(dir_):
    return 'Караханян'


def relocateFile(path):
    try:
        shutil.copytree(path, os.path.join(pathToDoneCase, os.path.basename(path)))
    except Exception as e:
        print(f"Error relocating file: {e}")
    # shutil.copytree(path, os.path.join(r'\\192.168.0.33\shared\_Общие документы_\_Фото\Выставлено прогой', a:=os.path.basename(path)))


# saveToken()
# listForUploads = scanFolder()