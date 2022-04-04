from os.path import join as joinPath, abspath, exists
from os import listdir, makedirs
import multiprocessing
import sys
sys.path.append(abspath(joinPath(__file__,'../../..')))
from PIL import Image, ImageDraw, ImageFont
import copy


MAXCPUUSE = 6


diskWithPrint = 'F'
pathToSiliconMask = r'{}:\Маски силикон'.format(diskWithPrint)
lightPath = joinPath(pathToSiliconMask,'light.png')
pathToCategoryList = joinPath(pathToSiliconMask,'cat.xlsx')
pathToPrintAll = r'{}:\Картинки китай\Под натяжку общее\Все'.format(diskWithPrint)
pathToPrintWithOutBack = r'{}:\Картинки китай\Под натяжку общее\Без фона'.format(diskWithPrint)
pathToDoneImage = r'{}:\Готовые принты\Силикон'.format(diskWithPrint)
reductionDict = {'закрытой камерой': 'зак.кам.',
                 'открытой камерой': 'отк.кам.',
                 'матовый': 'мат.',
                 'прозрачный': 'проз.',
                 'с силиконовым основанием': 'с сил. вставкой',
                 'с силиконовый вставкой': 'с сил. вставкой',
                 'противоударный': 'противоуд.',
                 'переливающиеся блестки': 'жидк. блестки',
                 'с усиленными углами': 'с усил.угл.',
                 'Чехол для': 'Чехол'}
reductionDict2 = {'Чехол для': 'Чехол'}
siliconCaseColorDict = {'белый': 'WHT',
                        'бирюзовый': 'TRQ',
                        'бледно-розовый': 'PNK',
                        'бордовый': 'VNS',
                        'голубой': 'SKB',
                        'желтый': 'YLW',
                        'зеленый': 'GRN',
                        'красный': 'RED',
                        'пудра': 'PNK',
                        'розовый': 'PNK',
                        'салатовый': 'L-GRN',
                        'светло-зеленый': 'L-GRN',
                        'светло-розовый': 'PNK',
                        'светло-фиолетовый': 'PPL',
                        'серый': 'GRY',
                        'синий': 'BLU',
                        'темно-синий': 'BLU',
                        'темно-сиреневый': 'D-LLC',
                        'фиолетовый': 'PPL',
                        'хаки': 'HCK',
                        'черный': 'BLC',
                        'прозрачный': 'CLR'
                        }



def combineImage(pathToMask, pathToPrint):
    
    mainImage = Image.new('RGBA', )


def chekPath(path=str):
    # pass
    pathToDoneImage = path.replace(pathToSiliconMask, pathToDoneImage)
    if not exists(pathToDoneImage):
        makedirs(pathToDoneImage)


def createSiliconImage(pathToMask, light = None):
    if light == None:
        light = Image.open(lightPath).convert("RGBA")
        flagMP = True
    else:
        flagMP = False
    if "проз." in pathToMask.lower() or "прозрачный" in pathToMask.lower():
        pathToPrintFolder = pathToPrintAll
    else:
        pathToPrintFolder = pathToPrintWithOutBack
    chekPath(pathToMask)
    if flagMP:
        pool = multiprocessing.Pool(MAXCPUUSE)
        for imagePrint in listdir(pathToPrintFolder):
            pathToPrint = joinPath(pathToPrintFolder, imagePrint)
            pool.apply_async(combineImage, args=(pathToMask, pathToPrint,))
        pool.close()
        pool.join()
    else:
        for imagePrint in listdir(pathToPrintFolder):
            pathToPrint = joinPath(pathToPrintFolder, imagePrint)
            combineImage(pathToMask, pathToPrint)

def createAllSiliconImage(pathToSiliconMask):
    pool = multiprocessing.Pool(MAXCPUUSE)
    light = Image.open(lightPath).convert("RGBA")
    for i in range(8):
        pool.apply_async(createSiliconImage, args=('',light,))
    pool.close()