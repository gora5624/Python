from genericpath import isdir
from os.path import join as joinPath, abspath, exists
from shutil import copyfile
from os import listdir, makedirs
import multiprocessing
import sys
sys.path.append(abspath(joinPath(__file__,'../../..')))
from PIL import Image
import time
from copy import copy


maxCPUUse = 6


diskWithPrint = 'F'
pathToSiliconMaskFolder = r'{}:\Маски силикон'.format(diskWithPrint)
pathToCategoryList = joinPath(pathToSiliconMaskFolder,'cat.xlsx')
pathToPrintAll = r'{}:\Картинки китай\Принты со светом\Все'.format(diskWithPrint)
pathToPrintWithOutBack = r'{}:\Картинки китай\Принты со светом\Без фона'.format(diskWithPrint)
pathToSecondImagesFolder = r'{}:\Для загрузки\Вторые картинки\Силикон'.format(diskWithPrint)
pathToDoneSiliconImage = r'{}:\Для загрузки\Готовые принты\Силикон'.format(diskWithPrint)
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


def getSizeAndPos(image):
    # image = Image.open(pathToMask).convert("RGBA")
    size = image.size
    for xLeft in range(25, size[0]):
        rgba = image.getpixel((xLeft, 600))
        if rgba[3] != 255:
            break
        xLeft += 1
    for xRight in reversed(range(size[0]-20)):
        rgba = image.getpixel((xRight, 600))
        if rgba[3] != 255:
            break
        xRight += 1
    line = int((xRight - xLeft)/2) + xLeft
    for yTop in range(50, size[1]):
        rgba = image.getpixel((line, yTop))
        if rgba[3] != 255:
            break
        yTop += 1
    for yBott in reversed(range(size[1]-20)):
        rgba = image.getpixel((line, yBott))
        if rgba[3] != 255:
            break
        yBott += 1
    return (xLeft-5, xRight+5, yTop-5, yBott+5)


def combineImage(imageMask, imagePrintPath, imageBack, printsize, printPaste, pathToSave, pathToPrintFolder):
    imagePrint = Image.open(joinPath(pathToPrintFolder, imagePrintPath)).convert('RGBA').resize(printsize)
    imageBackNew = copy(imageBack)
    # size = imageMask.size
    imageBackNew.paste(imagePrint,printPaste,imagePrint)
    imagePrint.close()
    imageBackNew = Image.alpha_composite(imageBackNew,imageMask)
    imageBackNew = imageBackNew.convert('RGB')
    # imageBackNew = imageBackNew.resize((size[0]//3, size[1]//3))
    imageBackNew.save(joinPath(pathToSave,imagePrintPath.replace('print','(Принт').replace('.png',').jpg')),"JPEG",optimize=True, progressive=True, quality=70)

def chekPath(path=str):
    fullpathToDoneSiliconImage = path.replace(pathToSiliconMaskFolder, pathToDoneSiliconImage)
    if not exists(fullpathToDoneSiliconImage):
        makedirs(fullpathToDoneSiliconImage)


def createSiliconImage(pathToMaskFolder, countCPU):
    if "проз." in pathToMaskFolder.lower() or "прозрачный" in pathToMaskFolder.lower():
        pathToPrintFolder = pathToPrintAll
    else:
        try:
            pathToSecondImageFolder = pathToMaskFolder.replace(pathToSiliconMaskFolder,pathToSecondImagesFolder)
            chekPath(pathToSecondImageFolder)
            secondImage = Image.open(joinPath(pathToMaskFolder, '2.jpg'))
            secondImage = secondImage.resize((secondImage.size[0]//3, secondImage.size[1]//3))
            secondImage.save(joinPath(pathToSecondImageFolder, '2.jpg'),"JPEG",optimize=True, progressive=True, quality=70)
        except:
            print('Не удалось скопировать 2е фото для {}'.format(pathToMaskFolder))
        pathToPrintFolder = pathToPrintWithOutBack
    chekPath(pathToMaskFolder)
    pathToMask = joinPath(pathToMaskFolder,'mask.png')
    #xLeft, xRight, yTop, yBott = getSizeAndPos(imageMask)
    imageMask = Image.open(pathToMask).convert('RGBA')
    size = imageMask.size
    pathToBack = pathToMask.replace('mask.png', 'fon.png')
    imageBack = Image.open(pathToBack).convert('RGBA').resize((size[0]//3, size[1]//3))
    imageMask = imageMask.resize((size[0]//3, size[1]//3))
    xLeft, xRight, yTop, yBott = getSizeAndPos(imageMask)
    printsize = (xRight-xLeft, yBott-yTop)
    printPaste = (xLeft, yTop)
    pathToSave = pathToMaskFolder.replace(pathToSiliconMaskFolder, pathToDoneSiliconImage)
    if countCPU != 1:
        pool = multiprocessing.Pool(countCPU)
        imageMaskN = copy(imageMask)
        imageBackN = copy(imageBack)
        for imagePrintName in listdir(pathToPrintFolder):
            pool.apply_async(combineImage, args=(imageMaskN, imagePrintName, imageBackN, printsize, printPaste, pathToSave, pathToPrintFolder,))
            #combineImage(imageMask, imagePrint, imageBack, printsize, printPaste, pathToSave, pathToPrintFolder)
        imageMask.close()
        imageBack.close()
        pool.close()
        pool.join()
    else:
        for imagePrintName in listdir(pathToPrintFolder):
            combineImage(imageMask, imagePrintName, imageBack, printsize, printPaste, pathToSave, pathToPrintFolder)


def createAllSiliconImage(pathToSiliconMask, maxCPUUse):
    start_time = time.time()
    #i = 0
    pool = multiprocessing.Pool(maxCPUUse)
    for  model in listdir(pathToSiliconMask):
        pathToModel = joinPath(pathToSiliconMask, model)
        if isdir(pathToModel):
            for color in listdir(pathToModel):
                pathToColor = joinPath(pathToModel,color)
                pool.apply_async(createSiliconImage, args=(pathToColor,1))
    pool.close()
    pool.join()
    #             p = multiprocessing.Process(target=createSiliconImage, args=(pathToColor,1))
    #             p.start()
    #             i+=1
    #             if i == maxCPUUse:
    #                 i = 0
    #                 p.join()
    # p.join()
    print("--- %s seconds ---" % (time.time() - start_time))