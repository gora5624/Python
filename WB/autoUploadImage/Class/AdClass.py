import os
import shutil
import logging

from folders import pathToFolderForPhotoToUploads, listPathToXLSX, pathToDoneCase
from network.uploadImage import updatePhotoMain

logger = logging.getLogger(__name__)

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
    logger.info(f"Scanning complete. {len(listForUploads)} items found.")
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
    logger.info(f"Uploading XLSX files for {listToUpload['dirName']}")
    updatePhotoMain(listToUpload)


def getSeller(dir_):
    return 'Караханян'


def relocateFile(path):
    try:
        shutil.copytree(path, os.path.join(pathToDoneCase, os.path.basename(path)))
        logger.info(f"File relocated for {os.path.basename(path)}")
    except Exception as e:
        logger.error(f"Error relocating file for {os.path.basename(path)}: {e}")
        # print(f"Error relocating file: {e}")
    # shutil.copytree(path, os.path.join(r'\\192.168.0.33\shared\_Общие документы_\_Фото\Выставлено прогой', a:=os.path.basename(path)))


# saveToken()
# listForUploads = scanFolder()