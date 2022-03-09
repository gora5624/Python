from os.path import join as joinPath, abspath, exists
from os import listdir, makedirs
import multiprocessing
from PIL import Image, ImageDraw, ImageFont

disk = 'F'
pathToImage = r'{}:\Готовые принты книжки Fashion'.format(disk)
fontPath = abspath(joinPath(__file__, '..','Fonts','CarosSoftBold.ttf'))
pathToDoneImageWithName = r'{}:\Готовые картинки Fashion по моделям'.format(disk)
XPasteBrand = 50
YPasteBrand = 100
XPasteModel = 50
YPasteModel = 20

def makeImageWithNameModel(colorList, modelBrand, modelModel):
    pool = multiprocessing.Pool()
    for color in colorList:
        pool.apply_async(makeImageColor, args=(color, modelBrand, modelModel,))
    pool.close()
    pool.join()
    # for color in colorList:
    #     makeImageColor(color, modelBrand, modelModel)
    print(modelBrand + ' ' + modelModel + ' готов!')


def makeImageColor(color, modelBrand, modelModel):
    pathToColor = joinPath(pathToImage, color)
    customFontBrand = ImageFont.truetype(fontPath, 80)
    customFontModel = ImageFont.truetype(fontPath, 65)
    for pic in listdir(pathToColor): 
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
        drawText = ImageDraw.Draw(imageDone)
        drawText.text((widthImage-XPasteModel-widthText,heightImage-YPasteModel-heightText), modelModel, font=customFontModel,fill='#000000')
        fullPathToSave = joinPath(pathToDoneImageWithName, modelBrand + ' ' + modelModel, color)
        if not exists(fullPathToSave):
            makedirs(fullPathToSave)
        imageDone.save(joinPath(fullPathToSave, pic[0:-4] + '.jpg'), quality=75)
        #pass