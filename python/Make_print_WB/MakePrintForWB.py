from PIL import Image
import os
from my_lib import file_exists
import copy

pathToMaskFolder = r'D:\mask'
pathToPrintFolder = r'D:\NewPrint'
pathToDonePrints = r'D:\printsPy'


def getSizeAndPos(pathToMask):
    image = Image.open(pathToMask).convert("RGBA")
    size = image.size
    for xLeft in range(100, size[0]):

        rgba = image.getpixel((xLeft, 1700))
        if rgba[3] != 255:
            break
        xLeft += 1
    for xRight in reversed(range(size[0]-100)):
        rgba = image.getpixel((xRight, 1700))
        if rgba[3] != 255:
            break
        xRight += 1
    for yTop in range(100, size[1]):
        rgba = image.getpixel((1900, yTop))
        if rgba[3] != 255:
            break
        yTop += 1
    for yBott in reversed(range(size[1]-100)):
        rgba = image.getpixel((1900, yBott))
        if rgba[3] != 255:
            break
        yBott += 1

    return (xLeft, xRight, yTop, yBott, size)
    # return (1200, 2200, 400, 2660, size)


def makePrint():
    maskFoldersList = os.listdir(pathToMaskFolder)
    printList = os.listdir(pathToPrintFolder)
    for maskFolder in maskFoldersList:
        pathToMask = os.path.join(pathToMaskFolder, maskFolder, r'mask.png')
        pathToBackground = os.path.join(
            pathToMaskFolder, maskFolder, r'fon.png')
        maskImageOld = Image.open(pathToMask).convert("RGBA")
        BackgroundImageOld = Image.open(pathToBackground)
        xLeft, xRight, yTop, yBott, size = getSizeAndPos(pathToMask)
        printsize = (xRight-xLeft + 10, yBott-yTop+10)
        printPaste = (xLeft-5, yTop-5)
        if not file_exists(os.path.join(pathToDonePrints, maskFolder)):
            os.makedirs(os.path.join(pathToDonePrints, maskFolder))
        for printPath in printList:
            maskImage = copy.copy(maskImageOld)
            BackgroundImage = copy.copy(BackgroundImageOld)
            pathToPrint = os.path.join(pathToPrintFolder, printPath)
            printImage = Image.open(pathToPrint).resize(printsize)
            BackgroundImage.paste(printImage, (printPaste), printImage)
            printImage.close()
            BackgroundImage.paste(maskImage, (0, 0), maskImage)
            printDone = os.path.join(
                pathToDonePrints, maskFolder, printPath.replace('png', 'jpg'))
            BackgroundImage = BackgroundImage.convert('RGB')
            BackgroundImage = BackgroundImage.resize(
                (size[0]//3, size[1]//3))
            BackgroundImage.save(printDone,
                                 quality=70)


makePrint()
