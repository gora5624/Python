from os.path import join as joinPath, abspath, exists
from os import listdir, makedirs
import multiprocessing
from PIL import Image, ImageDraw, ImageFont
import sys
sys.path.append(abspath(joinPath(__file__,'../..')))
from Folders import pathToDoneBookImageWithName, fontPath, pathToBookImageWithOutModel, pathToTopPrint, pathToUploadFolderLocal, pathToBookImageWithOutModelNew
import pandas
from shutil import copytree, ignore_patterns


XPasteBrand = 50
YPasteBrand = 100
XPasteModel = 50
YPasteModel = 20


def copyImage():
    copytree(pathToDoneBookImageWithName, pathToUploadFolderLocal + r'\\Силикон', dirs_exist_ok=True, ignore=ignore_patterns('*.xlsx'))
    # copytree(pathToSecondImagesFolderSilicon, pathToSecondImageUploadFolder + r'\\Силикон', dirs_exist_ok=True, ignore=ignore_patterns('*.xlsx'))

def makeImageBookWithNameModel(colorList, modelBrand, modelModel):
    pool = multiprocessing.Pool()
    for color in colorList:
        pool.apply_async(makeImageColor, args=(color, modelBrand, modelModel,))
    pool.close()
    pool.join()
    # copyImage()
    # for color in colorList:
    #     makeImageColor(color, modelBrand, modelModel)
    print(modelBrand + ' ' + modelModel + ' готов!')


def makeImageBookWithNameModelNew(colorList, modelBrand, modelModel):
    pool = multiprocessing.Pool()
    for color in colorList:
        pool.apply_async(makeImageColorNew2, args=(color, modelBrand, modelModel,))
    pool.close()
    pool.join()
    # copyImage()
    # for color in colorList:
    #     makeImageColor(color, modelBrand, modelModel)
    print(modelBrand + ' ' + modelModel + ' готов!')


def makeImageBookWithNameModelNew2(colorList, modelBrand, modelModel):
    pool = multiprocessing.Pool()
    for color in colorList:
        pool.apply_async(makeImageColorNew3, args=(color, modelBrand, modelModel,))
    pool.close()
    pool.join()
    # copyImage()
    # for color in colorList:
    #     makeImageColor(color, modelBrand, modelModel)
    print(modelBrand + ' ' + modelModel + ' готов!')


def makeImageColor(color, modelBrand, modelModel):
    pathToColor = joinPath(pathToBookImageWithOutModel, color)
    customFontBrand = ImageFont.truetype(fontPath, 80)
    customFontModel = ImageFont.truetype(fontPath, 65)
    topPrint = pandas.DataFrame(pandas.read_excel(pathToTopPrint))[0:200]['Принт'].values.tolist()
    for pic in listdir(pathToColor):
        if pic.replace('.png',')').replace('print','(Принт') in topPrint:
            imagePrint = Image.open(joinPath(pathToColor, pic))
            imagePrint = imagePrint.resize((1200, 1601))
            imageDone = Image.new('RGB', imagePrint.size)
            imageDone.paste(imagePrint)
            # Написать бренд
            drawText = ImageDraw.Draw(imageDone)
            widthImage, heightImage = imageDone.size
            widthText, heightText = drawText.textsize(modelBrand, font=customFontBrand)
            drawText = ImageDraw.Draw(imageDone)
            drawText.text((widthImage-XPasteBrand-widthText,heightImage-YPasteBrand-heightText), modelBrand, font=customFontBrand,fill='#000000')
            # написать Модель
            drawText = ImageDraw.Draw(imageDone)
            widthImage, heightImage = imageDone.size
            widthText, heightText = drawText.textsize(modelModel, font=customFontModel)
            if widthText>800:
                customFontModel = ImageFont.truetype(fontPath, 55)
            drawText = ImageDraw.Draw(imageDone)
            drawText.text((widthImage-XPasteModel-widthText,heightImage-YPasteModel-heightText), modelModel, font=customFontModel,fill='#000000')
            fullPathToSave = joinPath(pathToDoneBookImageWithName, 'Чехол книга ' + modelBrand + ' ' + modelModel +' черный с сил. вставкой Fashion')
            if not exists(fullPathToSave.replace('/','&')):
                makedirs(fullPathToSave.replace('/','&'))
            (x,y) = imageDone.size
            imageDone.save(joinPath(fullPathToSave.replace('/','&'), pic.replace('print ','(Принт ').replace('.png',')') + '.jpg'), quality=75)


def makeImageColorNew(color, modelBrand, modelModel):
    pathToColor = joinPath(pathToBookImageWithOutModelNew, color)
    maxWidth = 650
    maxHeight =110
    # topPrint = pandas.DataFrame(pandas.read_excel(pathToTopPrint))[0:200]['Принт'].values.tolist()
    for pic in listdir(pathToColor):
        if pic == 'Thumbs.db':
            continue
        # if pic.replace('.png',')').replace('print','(Принт') in topPrint:
        imagePrint = Image.open(joinPath(pathToColor, pic))
        imagePrint = imagePrint.resize((1200, 1601))
        imageDone = Image.new('RGB', imagePrint.size)
        imageDone.paste(imagePrint)
        # Написать бренд
        
        drawText = ImageDraw.Draw(imageDone)
        fontSizeDef = 100
        customFont = ImageFont.truetype(fontPath, fontSizeDef)
        while True:
            left, top, right, bottom = drawText.textbbox((0,0),text=modelBrand, font=customFont)
            widthText, heightText = right - left, bottom - top
            if (widthText < maxWidth) and (heightText < maxHeight):
                break
            else:
                fontSizeDef-=5
                customFont = ImageFont.truetype(fontPath, fontSizeDef)
        drawText = ImageDraw.Draw(imageDone)
        drawText.text((368-(int(widthText/2)),1350), modelBrand, font=customFont,fill='#000000')
        # imageDone.show()
        # написать Модель
        fontSizeDef = 100
        customFont = ImageFont.truetype(fontPath, fontSizeDef)
        drawText = ImageDraw.Draw(imageDone)
        while True:
            left, top, right, bottom = drawText.textbbox((0,0),text=modelModel, font=customFont)
            widthText, heightText = right - left, bottom - top
            if (widthText < maxWidth) and (heightText < maxHeight):
                break
            else:
                fontSizeDef-=5
                customFont = ImageFont.truetype(fontPath, fontSizeDef)
        drawText = ImageDraw.Draw(imageDone)
        drawText.text((368-(int(widthText/2)),1470), modelModel, font=customFont,fill='#000000')
        # imageDone.show()
        fullPathToSave = joinPath(pathToDoneBookImageWithName, 'Чехол книга ' + modelBrand + ' ' + modelModel +' черный с сил. вставкой Fashion')
        if not exists(fullPathToSave.replace('/','&')):
            makedirs(fullPathToSave.replace('/','&'))
        imageDone.save(joinPath(fullPathToSave.replace('/','&'), pic.replace('print ','(Принт ').replace('.png',')') + '.jpg'), quality=100)

def makeImageColorNew2(color, modelBrand, modelModel):
    pathToBookImageWithOutModelNew2 = r'F:\книжки новые2'
    pathToColor = joinPath(pathToBookImageWithOutModelNew2, color)
    maxWidth = 650
    maxHeight =110
    # topPrint = pandas.DataFrame(pandas.read_excel(pathToTopPrint))[0:200]['Принт'].values.tolist()
    for pic in listdir(pathToColor):
        if pic == 'Thumbs.db':
            continue
        # if pic.replace('.png',')').replace('print','(Принт') in topPrint:
        imagePrint = Image.open(joinPath(pathToColor, pic))
        imagePrint = imagePrint.resize((1200, 1601))
        imageDone = Image.new('RGB', imagePrint.size)
        imageDone.paste(imagePrint)
        # Написать бренд
        
        drawText = ImageDraw.Draw(imageDone)
        fontSizeDef = 100
        customFont = ImageFont.truetype(fontPath, fontSizeDef)
        while True:
            left, top, right, bottom = drawText.textbbox((0,0),text=modelBrand, font=customFont)
            widthText, heightText = right - left, bottom - top
            if (widthText < maxWidth) and (heightText < maxHeight):
                break
            else:
                fontSizeDef-=5
                customFont = ImageFont.truetype(fontPath, fontSizeDef)
        drawText = ImageDraw.Draw(imageDone)
        drawText.text((840-(int(widthText/2)),1350), modelBrand, font=customFont,fill='#000000')
        # imageDone.show()
        # написать Модель
        fontSizeDef = 100
        customFont = ImageFont.truetype(fontPath, fontSizeDef)
        drawText = ImageDraw.Draw(imageDone)
        while True:
            left, top, right, bottom = drawText.textbbox((0,0),text=modelModel, font=customFont)
            widthText, heightText = right - left, bottom - top
            if (widthText < maxWidth) and (heightText < maxHeight):
                break
            else:
                fontSizeDef-=5
                customFont = ImageFont.truetype(fontPath, fontSizeDef)
        drawText = ImageDraw.Draw(imageDone)
        drawText.text((840-(int(widthText/2)),1470), modelModel, font=customFont,fill='#000000')
        # imageDone.show()
        fullPathToSave = joinPath(pathToDoneBookImageWithName, 'Чехол книга ' + modelBrand + ' ' + modelModel +' черный с сил. вставкой Fashion')
        if not exists(fullPathToSave.replace('/','&')):
            makedirs(fullPathToSave.replace('/','&'))
        imageDone.save(joinPath(fullPathToSave.replace('/','&'), pic.replace('print ','(Принт ').replace('.png',')') + '.jpg'), quality=80)


def makeImageColorNew3(color, modelBrand, modelModel):
    pathToBookImageWithOutModelNew2 = r'F:\книжки новые3 — копия'
    pathToColor = joinPath(pathToBookImageWithOutModelNew2, color)
    maxWidth = 650
    maxHeight =110
    # topPrint = pandas.DataFrame(pandas.read_excel(pathToTopPrint))[0:200]['Принт'].values.tolist()
    for pic in listdir(pathToColor):
        if pic == 'Thumbs.db':
            continue
        # if pic.replace('.png',')').replace('print','(Принт') in topPrint:
        imagePrint = Image.open(joinPath(pathToColor, pic))
        imagePrint = imagePrint.resize((1200, 1601))
        imageDone = Image.new('RGB', imagePrint.size)
        imageDone.paste(imagePrint)
        # Написать бренд
        
        drawText = ImageDraw.Draw(imageDone)
        fontSizeDef = 100
        customFont = ImageFont.truetype(fontPath, fontSizeDef)
        while True:
            left, top, right, bottom = drawText.textbbox((0,0),text=modelBrand, font=customFont)
            widthText, heightText = right - left, bottom - top
            if (widthText < maxWidth) and (heightText < maxHeight):
                break
            else:
                fontSizeDef-=5
                customFont = ImageFont.truetype(fontPath, fontSizeDef)
        drawText = ImageDraw.Draw(imageDone)
        drawText.text((840-(int(widthText/2)),1350), modelBrand, font=customFont,fill='#000000')
        # imageDone.show()
        # написать Модель
        fontSizeDef = 100
        customFont = ImageFont.truetype(fontPath, fontSizeDef)
        drawText = ImageDraw.Draw(imageDone)
        while True:
            left, top, right, bottom = drawText.textbbox((0,0),text=modelModel, font=customFont)
            widthText, heightText = right - left, bottom - top
            if (widthText < maxWidth) and (heightText < maxHeight):
                break
            else:
                fontSizeDef-=5
                customFont = ImageFont.truetype(fontPath, fontSizeDef)
        drawText = ImageDraw.Draw(imageDone)
        drawText.text((840-(int(widthText/2)),1470), modelModel, font=customFont,fill='#000000')
        # imageDone.show()
        fullPathToSave = joinPath(pathToDoneBookImageWithName, 'Чехол книга ' + modelBrand + ' ' + modelModel +' черный с сил. вставкой Fashion')
        if not exists(fullPathToSave.replace('/','&')):
            makedirs(fullPathToSave.replace('/','&'))
        imageDone.save(joinPath(fullPathToSave.replace('/','&'), pic.replace('print ','(Принт ').replace('.png',')') + '.jpg'), quality=80)