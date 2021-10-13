from PIL import Image, ImageDraw, ImageFont
from os.path import join as joinpath
import copy
from os import listdir
from my_lib import read_xlsx
import multiprocessing

fontDir = r'C:\Users\user\AppData\Local\Microsoft\Windows\Fonts'
fontName = 'CarosSoftBold'
fontPath = joinpath(fontDir, fontName + '.ttf')
pathToDoneBook = r'D:\NanoBook'
pathToFile = r'D:\книги.xlsx'
imageBackPath = r'D:\tmp\my_prod\Python\python\makeWBNanoPic\back'
imageBackList = listdir(imageBackPath)


def openImage(imagePath):
    picBack = Image.open(imagePath).convert("RGB")
    picBackCopy = copy.copy(picBack)
    picBack.close()
    return picBackCopy


def pasteTextOnImage(image, text):
    sizeFont = 100
    text1X = 230
    text1Y = 1445
    text2X = 230
    text2Y = 1545

    font = ImageFont.truetype(fontPath, size=sizeFont)
    drawText = ImageDraw.Draw(image)
    i = -1
    while True:
        textList = text.split(' ')
        textNew = text.split(' ')[0:i]
        sizeText = drawText.textsize(' '.join(textNew),
                                     font=font)
        if sizeText[0] < 1000:
            text1 = ' '.join(textList[0:i])
            text2 = ' '.join(textList[i:])
            break
        else:
            i -= 1
    while True:
        font2 = ImageFont.truetype(fontPath, size=sizeFont)
        sizeText = drawText.textsize(text2,
                                     font=font2)
        if sizeText[0] < 1000:
            font2 = ImageFont.truetype(fontPath, size=sizeFont)
            break
        else:
            sizeFont -= 5
            text2Y += 3

    drawText.text((text1X, text1Y), text=text1, font=font, fill='#FFFFFF')
    drawText.text((text2X, text2Y), text=text2, font=font2, fill='#FFFFFF')
    return image


def savePic(image, barcod):
    joinpath(pathToDoneBook, )
    image.save(joinpath(pathToDoneBook, barcod + '.jpg'))


def makeNanoBookPic(imagePath, line):
    barcod = line['Баркод'] if type(
        line['Баркод']) == str else str(line['Баркод'])[0:-2]
    image = openImage(imagePath)
    imageWithText = pasteTextOnImage(image, line['Название'])
    savePic(imageWithText, barcod)


def main(imageBackList, pathToFile):
    for backImage in imageBackList:
        imagePath = joinpath(imageBackPath, backImage)

        for line in read_xlsx(pathToFile):
            makeNanoBookPic(imagePath, line)


main(imageBackList, pathToFile)
