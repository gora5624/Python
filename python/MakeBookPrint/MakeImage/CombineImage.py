from os.path import join as joinPath
from os.path import abspath
from os import listdir, makedirs
from os.path import exists, basename
from PIL import Image
from perspective import transformPrint

'''1 - все принты
    другие значения - только без фона'''
mode = 1

diskWithPrint = 'F'
diskForDone = 'F'
pathToPrintAll = r'{}:\Картинки китай\Под натяжку общее\Все'.format(diskForDone)
pathToPrintWithOutBack = r'{}:\Картинки китай\Под натяжку общее\Без фона'.format(diskForDone)
pathToPrint = pathToPrintAll  if mode == 1 else pathToPrintWithOutBack
pathToDonePic = r'{}:\Готовые принты книжки Fashion'.format(diskForDone)
pathToEffect = abspath(joinPath(__file__, '..',r'Effect\light.png'))
pastePrintCoord = (200,547)
width = 1870
widthDone = 900


def chek(pathToChek):
    if not exists(pathToChek):
        makedirs(pathToChek)


def combineImage(pathToImgBack, pathToImgMask):
    pathToSave = joinPath(pathToDonePic, basename(pathToImgBack)[0:-4])
    chek(pathToSave)
    # Открываем фон, маску, эффект текстуры
    imgBack = Image.open(pathToImgBack).convert('RGBA')
    imgMask = Image.open(pathToImgMask).convert('RGBA')
    imgTexture = Image.open(pathToEffect).convert('RGBA')
    # Пробегаемся по списку принтов
    for imagePrint in listdir(pathToPrint):
            # Создаём пустое изображение
        imgMain = Image.new('RGBA', imgBack.size)
        # Открываем принт
        imgPrint = transformPrint(joinPath(pathToPrint,imagePrint))
        # Изменяем размер пропорционально согласно заданному выше
        imgPrint = imgPrint.resize((width, int(imgPrint.size[1]*(width/imgPrint.size[0]))))
        # Вставляем фон на пустое изображение
        imgMain.paste(imgBack,(0,0),imgBack)
        # Вставляем принт на изображение с фоном
        imgMain.paste(imgPrint,pastePrintCoord,imgPrint)
        # Создаём маску по принту для текстуры, чтобы текстура легла только на принт
        # Создаем промежуточную картинку с нашим размером
        imgMaskForTexture = Image.new('L', imgBack.size)
        # Создаём маску для текстуры из промежуточного слоя картинку с альфа-каналом (.split[-1]) в нужном месте
        imgMaskForTexture.paste(imgPrint.split()[-1],pastePrintCoord,imgPrint.split()[-1])
        # Создаём 2ю промежуточную картинку для совмещения
        imgMaskForTexture2 = Image.new('RGBA', imgBack.size)
        # Совмещаем промежуточный слой и маску для текстуры
        imgMaskForTexture2.paste(imgTexture, (0,0), imgMaskForTexture)
        # Совмещаем текстуру и полученное изображение
        imgMain = Image.alpha_composite(imgMain,imgMaskForTexture2)
        # Вставляем поверх всего закрывающую маску чехла
        imgMain = Image.alpha_composite(imgMain,imgMask)
        imgMainDone = imgMain.resize((widthDone, int(imgMain.size[1]*(widthDone/imgMain.size[0]))))
        imgMainDone.save(joinPath(pathToSave, basename(imagePrint)), quality=70)



# pathToImgBack = r'E:\MyProduct\Python\python\MakeBookPrint\BookPic\BookBack\Голубая.jpg'
# pathToImgMask = r'E:\MyProduct\Python\python\MakeBookPrint\BookPic\BookMask\Голубая.png'
# combineImage(pathToImgBack, pathToImgMask)