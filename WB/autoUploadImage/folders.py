from os.path import abspath, join as joinPath
import logging

logger = logging.getLogger(__name__)

pathToFolderForPhotoToUploads = r'\\192.168.0.33\shared\_Общие документы_\_Фото\для выставления на сайт'
listPathToXLSX = {
    'cardCase':[r'\\192.168.0.33\shared\_Общие документы_\Егор\Архив принтов xlsx\силикон'],
    'mate':[r'\\192.168.0.33\shared\_Общие документы_\Егор\Архив принтов xlsx\силикон'],
    'fashion':[
        r'\\192.168.0.33\shared\_Общие документы_\Егор\Архив принтов xlsx\книжки'],
    'clear':[r'\\192.168.0.33\shared\_Общие документы_\Егор\Архив принтов xlsx\силикон'],
    'skinshell':[r'\\192.168.0.33\shared\_Общие документы_\Егор\Архив принтов xlsx\SkinShell']
}

pathToPrintImageForClear = r'\\rab\uploads\Картинки для натяжки' # Путь откуда брать фотки для натяжки
pathToDoneImages = r'\\rab\uploads\Готовые принты\Силикон'
pathToTopPrintFile = abspath(joinPath(__file__, '..', r'topPrint.xlsx'))
pathToDoneCase = r'\\192.168.0.33\shared\_Общие документы_\_Фото\Выставлено прогой'

try:
    logger.info(f"Paths set: {pathToFolderForPhotoToUploads}, {pathToPrintImageForClear}, {pathToDoneImages}, {pathToTopPrintFile}, {pathToDoneCase}")
except Exception as e:
    logger.error(f"Error setting paths: {e}")