from PIL import Image, ImageDraw, ImageFont
from os.path import join as joinpath
import multiprocessing
import os
import zipfile

pathToImage = r'D:\image'
fontDir = r'C:\Users\user\AppData\Local\Microsoft\Windows\Fonts'
fontName = 'CarosSoftBold'
fontPath = joinpath(fontDir, fontName + '.ttf')
countInZIP = 200


def addText(image, fullPath):
    sizeFont = 75
    sizeFont2 = 37
    text1X = 655
    text1Y = 798
    text2X = 627
    text2Y = 883
    font = ImageFont.truetype(fontPath, size=sizeFont)
    font2 = ImageFont.truetype(fontPath, size=sizeFont2)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((610, 800, 880, 940), fill='white', radius=43)
    draw.text((text1X, text1Y), text='C21Y', font=font, fill='#FF0000')
    draw.text((text2X, text2Y), text='Не подходит',
              font=font2, fill='#FF0000')
    image.save(fullPath)


def OnenAndSavePic():
    pool = multiprocessing.Pool()
    for dir in os.listdir(pathToImage):
        fullPath = os.path.join(pathToImage, dir, 'photo', '1.jpg')
        try:
            image = Image.open(fullPath)
        except:
            continue
        pool.apply_async(addText, args=(image, fullPath, ))
        # addText(image)
    pool.close()
    pool.join()


def createZIP(pathToImage):
    i = j = 0
    for dir_ in os.listdir(pathToImage):
        if i == countInZIP:
            j = j+1
            i = 0
        with zipfile.ZipFile(pathToImage + '\Done{}.zip'.format(j), 'a') as myzip:
            for file in os.listdir(os.path.join(pathToImage, dir_, 'photo')):
                myzip.write(os.path.join(pathToImage, dir_, 'photo', file),
                            arcname=os.path.join('D:\\', dir_, 'photo', file))
        i = i+1


if __name__ == '__main__':
    OnenAndSavePic()
    createZIP(pathToImage)
