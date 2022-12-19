from genericpath import isdir
from os.path import join as joinPath, abspath, exists
from os import listdir, makedirs
import multiprocessing
import sys
sys.path.append(abspath(joinPath(__file__,'../..')))
from PIL import Image
import time
from copy import copy
from shutil import copytree, ignore_patterns
from Folders import pathToMaskFolderSilicon, pathToDoneSiliconImageSilicon, pathToPrintImageFolderAllSil, pathToPrintImageFolderWithOutBackSil, pathToSecondImagesFolderSilicon, pathToUploadFolderLocal, pathToSecondImageUploadFolder

maxCPUUse = 6
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
    if 'Thumbs.db' in imagePrintPath:
        return 0
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
    fullpathToDoneSiliconImage = path.replace(pathToMaskFolderSilicon, pathToDoneSiliconImageSilicon)
    if not exists(fullpathToDoneSiliconImage):
        makedirs(fullpathToDoneSiliconImage)


def createSiliconImage(pathToMaskFolder, countCPU, addImage, mode, topPrint):
    if "проз" in pathToMaskFolder.lower():
        pathToPrintFolder = pathToPrintImageFolderAllSil    
    elif 'книга' in pathToMaskFolder.lower():
        pathToPrintFolder = pathToPrintImageFolderAllSil
    else:
        try:
            pathToSecondImageFolder = pathToMaskFolder.replace(pathToMaskFolderSilicon,pathToSecondImagesFolderSilicon)
            chekPath(pathToSecondImageFolder)
            secondImage = Image.open(joinPath(pathToMaskFolder, addImage))
            sk = int(secondImage.size[0]/900)
            secondImage = secondImage.resize((secondImage.size[0]//sk, secondImage.size[1]//sk))
            secondImage.save(joinPath(pathToSecondImageFolder, addImage),"JPEG",optimize=True, progressive=True, quality=70)
        except:
            print('Не удалось скопировать 2е фото для {}'.format(pathToMaskFolder))
        pathToPrintFolder = pathToPrintImageFolderAllSil if mode != 'all' else pathToPrintImageFolderAllSil
    chekPath(pathToMaskFolder)
    pathToMask = joinPath(pathToMaskFolder,'mask.png')
    #xLeft, xRight, yTop, yBott = getSizeAndPos(imageMask)
    imageMask = Image.open(pathToMask).convert('RGBA')
    size = imageMask.size
    pathToBack = pathToMask.replace('mask.png', 'fon.png')
    sk = int(size[0]/900)
    imageBack = Image.open(pathToBack).convert('RGBA').resize((size[0]//sk, size[1]//sk))
    imageMask = imageMask.resize((size[0]//sk, size[1]//sk))
    xLeft, xRight, yTop, yBott = getSizeAndPos(imageMask)
    printsize = (xRight-xLeft, yBott-yTop)
    printPaste = (xLeft, yTop)
    pathToSave = pathToMaskFolder.replace(pathToMaskFolderSilicon, pathToDoneSiliconImageSilicon)
    if countCPU != 1:
        pool = multiprocessing.Pool(countCPU)
        imageMaskN = copy(imageMask)
        imageBackN = copy(imageBack)
        for imagePrintName in listdir(pathToPrintFolder):
            if type(topPrint) != str:
                namePrint = imagePrintName.replace('print','(Принт').replace('.png', ')')
                if namePrint in topPrint['Принт'].values.tolist():            
                    pool.apply_async(combineImage, args=(imageMaskN, imagePrintName, imageBackN, printsize, printPaste, pathToSave, pathToPrintFolder,))
            else:
                pool.apply_async(combineImage, args=(imageMaskN, imagePrintName, imageBackN, printsize, printPaste, pathToSave, pathToPrintFolder,))
            #combineImage(imageMask, imagePrint, imageBack, printsize, printPaste, pathToSave, pathToPrintFolder)
        imageMask.close()
        imageBack.close()
        pool.close()
        pool.join()
    else:
        for imagePrintName in listdir(pathToPrintFolder):
            if type(topPrint) != str:
                namePrint = imagePrintName.replace('print','(Принт').replace('.png', ')')
                if namePrint in topPrint['Принт'].values.tolist():
                    combineImage(imageMask, imagePrintName, imageBack, printsize, printPaste, pathToSave, pathToPrintFolder)
            else:
                combineImage(imageMask, imagePrintName, imageBack, printsize, printPaste, pathToSave, pathToPrintFolder)
            


def fakeCreateSiliconImage(pathToMaskFolder, mode, topPrint):
    if "проз" in pathToMaskFolder.lower():
        pathToPrintFolder = pathToPrintImageFolderAllSil
    elif 'книга' in pathToMaskFolder.lower():
        pathToPrintFolder = pathToPrintImageFolderAllSil
    else:
        # try:
        #     pathToSecondImageFolder = pathToMaskFolder.replace(pathToMaskFolderSilicon,pathToSecondImagesFolderSilicon)
        #     # chekPath(pathToSecondImageFolder)
        #     # secondImage = Image.open(joinPath(pathToMaskFolder, addImage))
        #     # sk = int(secondImage.size[0]/900)
        #     # secondImage = secondImage.resize((secondImage.size[0]//sk, secondImage.size[1]//sk))
        #     # secondImage.save(joinPath(pathToSecondImageFolder, addImage),"JPEG",optimize=True, progressive=True, quality=70)
        # except:
        #     print('Не удалось скопировать 2е фото для {}'.format(pathToMaskFolder))
        # pathToPrintFolder = pathToPrintImageFolderWithOutBackSil if mode != 'all' else pathToPrintImageFolderAllSil
        pathToPrintFolder = pathToPrintImageFolderAllSil if mode != 'all' else pathToPrintImageFolderAllSil
    chekPath(pathToMaskFolder)
    # pathToMask = joinPath(pathToMaskFolder,'mask.png')
    #xLeft, xRight, yTop, yBott = getSizeAndPos(imageMask)
    # imageMask = Image.open(pathToMask).convert('RGBA')
    # size = imageMask.size
    # pathToBack = pathToMask.replace('mask.png', 'fon.png')
    # sk = int(size[0]/900)
    # imageBack = Image.open(pathToBack).convert('RGBA').resize((size[0]//sk, size[1]//sk))
    # imageMask = imageMask.resize((size[0]//sk, size[1]//sk))
    # xLeft, xRight, yTop, yBott = getSizeAndPos(imageMask)
    # printsize = (xRight-xLeft, yBott-yTop)
    # printPaste = (xLeft, yTop)
    pathToSave = pathToMaskFolder.replace(pathToMaskFolderSilicon, pathToDoneSiliconImageSilicon)
    # pool = multiprocessing.Pool()
    # for imagePrintName in listdir(pathToPrintFolder):
    #     pool.apply_async(FakeCombineImage, args=(imagePrintName, pathToSave, ))
    #     #combineImage(imageMask, imagePrint, imageBack, printsize, printPaste, pathToSave, pathToPrintFolder)
    # # imageMask.close()
    # # imageBack.close()
    # pool.close()
    # pool.join()
    # else:
    for imagePrintName in listdir(pathToPrintFolder):
        if type(topPrint) != str:
            namePrint = imagePrintName.replace('print','(Принт').replace('.png', ')')
            if namePrint in topPrint['Принт'].values.tolist():
                FakeCombineImage(imagePrintName, pathToSave)
        else:
            FakeCombineImage(imagePrintName, pathToSave)


def FakeCombineImage(imagePrintName, pathToSave):
    with open(joinPath(pathToSave,imagePrintName.replace('print','(Принт').replace('.png',').jpg')), 'w') as file:
        # file.write('0')
        file.close()



def copyImage():
    copytree(pathToDoneSiliconImageSilicon, pathToUploadFolderLocal + r'\\Силикон', dirs_exist_ok=True, ignore=ignore_patterns('*.xlsx'))
    copytree(pathToSecondImagesFolderSilicon, pathToSecondImageUploadFolder + r'\\Силикон', dirs_exist_ok=True, ignore=ignore_patterns('*.xlsx'))


def fakecreateAllSiliconImage(pathToSiliconMask, mode, topPrint=''):
    pool = multiprocessing.Pool()
    for model in listdir(pathToSiliconMask):
        pathToModel = joinPath(pathToSiliconMask, model)
        if isdir(pathToModel):
            pool.apply_async(fakeCreateSiliconImage, args=(pathToModel, mode, topPrint,))
    pool.close()
    pool.join()
    # copyImage()


def createAllSiliconImage(pathToSiliconMask, maxCPUUse, addImage, mode, topPrint='',):
    start_time = time.time()
    #i = 0
    pool = multiprocessing.Pool(maxCPUUse)
    for model in listdir(pathToSiliconMask):
        pathToModel = joinPath(pathToSiliconMask, model)
        if isdir(pathToModel):
            # for color in listdir(pathToModel):
                # if 'Thumbs.db' not in color:
                # pathToColor = joinPath(pathToModel,color)
                pool.apply_async(createSiliconImage, args=(pathToModel,1, addImage, mode, topPrint,))
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
    copyImage()
