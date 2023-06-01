from os.path import join as joinPath, abspath, exists
from os import listdir, makedirs
import multiprocessing
from PIL import Image, ImageDraw, ImageFont
import sys
sys.path.append(abspath(joinPath(__file__,'../..')))
from Folders import pathToDoneBookImageWithName, fontPath, pathToBookImageWithOutModel, pathToTopPrint, pathToUploadFolderLocal
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
    copyImage()
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
            imageDone.save(joinPath(fullPathToSave.replace('/','&'), pic.replace('print ','(Принт ').replace('.png',')') + '.jpg'), quality=75)