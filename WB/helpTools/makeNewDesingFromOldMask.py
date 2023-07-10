from operator import mul
from PIL import Image, ImageFont, ImageDraw
import os
import re
import multiprocessing
import shutil



textSizeBrandX = 880
textSizeBrandY = 150
textSizeModelX = 850
textSizeModelY = 100
fontPath = r'D:\Python\WB\pasteTextToImage\Fonts\CarosSoftBold.ttf'
pathToMaskFolder = r'\\192.168.0.33\shared\_Общие документы_\Егор\Архив масок ВБ\Маски новые'
pathToMaskFolderNew = r'D:\maskNew'
imageBack = Image.open(r"\\192.168.0.33\shared\_Общие документы_\Егор\Архив масок ВБ\MobiNew.png").resize((1200,1600))

def copyImages(pathOld, pathNew):
    for file in os.listdir(pathOld):
        if ('mask' not in file) and ('fon' not in file):
            try:
                if not os.path.exists(os.path.join(pathNew,file)):
                    shutil.copy(os.path.join(pathOld,file), os.path.join(pathNew,file))
            except:
                pass



def makeTextPic(text, mode):
    startSizeText = 300
    delta = 0
    widthText, heightText = 1000, 1000
    tmpImage = Image.new('RGBA',(1200,1600))
    drawText = ImageDraw.Draw(tmpImage)
    customFontBrand = ImageFont.truetype(fontPath, startSizeText)
    left, top, right, bottom = drawText.textbbox((0,0),text=text, font=customFontBrand)
    widthText, heightText = right - left, bottom - top
    if mode=='brand':
        sizeX, sizeY = textSizeBrandX, textSizeBrandY
    else:
        sizeX, sizeY = textSizeModelX, textSizeModelY
    while (widthText > sizeX) or (heightText > sizeY):
        delta+=5
        customFontBrand = ImageFont.truetype(fontPath, startSizeText-delta)
        left, top, right, bottom = drawText.textbbox((0,0),text=text, font=customFontBrand)
        widthText, heightText = right - left, bottom - top
    tmpImage = Image.new('RGBA',(widthText,heightText))
    drawText = ImageDraw.Draw(tmpImage)
    drawText.text((0,-top), text, font=customFontBrand,fill='#2162ff')        
    tmpImage = tmpImage.rotate(90,expand=1)
    return tmpImage       



def main():
    for pathToMask in os.listdir(pathToMaskFolder):
        try:
            mainPath = os.path.join(pathToMaskFolder, pathToMask)
            if not os.path.exists(fullNewPath:=os.path.join(pathToMaskFolderNew,pathToMask)):
                os.makedirs(fullNewPath)
            multiprocessing.Process(target=copyImages, args=(mainPath, mainPath.replace(pathToMaskFolder, pathToMaskFolderNew),)).start()
            imageFon = Image.open(os.path.join(mainPath, 'fon.png')).resize((1200,1600))
            imageMask = Image.open(os.path.join(mainPath, 'mask.png')).resize((1200,1600))
            imageFinal = Image.new('RGBA',(1200,1600))
            imageFinal.paste(imageBack)
            imageFinal.paste(imageMask,(-380,0))
            brandText = re.sub(r' сил.*','',pathToMask).replace('Чехол ','').split(' ')[0]
            brandTextPic = makeTextPic(brandText, 'brand')
            imageFinal.paste(brandTextPic, (833, int((1600/2+48-brandTextPic.size[1]/2))),brandTextPic)
            modelText = ' '.join(re.sub(r' сил.*','',pathToMask).replace('Чехол ','').split(' ')[1:])
            modelTextPic = makeTextPic(modelText, 'model')
            imageFinal.paste(modelTextPic, (1030, int((1600/2+48-modelTextPic.size[1]/2))),modelTextPic)
            # imageFinal.show()

            imageFinal.save(os.path.join(fullNewPath, 'mask.png'))
            imageFinal.paste(imageFon,(-380,0))
            imageFinal.save(os.path.join(fullNewPath, 'fon.png'))
        except FileNotFoundError:
            print(mainPath)
            continue

if __name__ == '__main__':
    main()
