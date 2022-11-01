from PIL import Image
import os

def combineImage(pathToImg, pathToImgLight):
    # Открываем фон, маску, эффект текстуры
    imgLight = Image.open(pathToImgLight).convert('RGBA')
    # Пробегаемся по списку принтов
    for imagePrint in os.listdir(pathToImg):
        # Открываем принт
        img = Image.open(os.path.join(pathToImg, imagePrint)).convert('RGBA')
        # Создаём пустое изображение
        imgMain = Image.new('RGBA', img.size)
        # Вставляем принт на пустое изображение
        imgMain.paste(img,(0,0),img)
        # Создаём маску по принту для текстуры, чтобы текстура легла только на принт
        # Создаем промежуточную картинку с нашим размером
        imgMaskForTexture = Image.new('L', img.size)
        # Создаём маску для текстуры из промежуточного слоя картинку с альфа-каналом (.split[-1]) в нужном месте
        imgMaskForTexture.paste(img.split()[-1],(0,0),img.split()[-1])
        imgLight = imgLight.resize(imgMaskForTexture.size)
        # Создаём 2ю промежуточную картинку для совмещения
        imgMaskForTexture2 = Image.new('RGBA', img.size)
        # Совмещаем промежуточный слой и маску для текстуры
        imgMaskForTexture2.paste(imgLight, (0,0), imgMaskForTexture)
        # Совмещаем текстуру и полученное изображение
        imgMain = Image.alpha_composite(imgMain,imgMaskForTexture2)
        # Вставляем поверх всего закрывающую маску чехла
        pathToSave = r'F:\Цвета свет'
        imgMain.save(os.path.join(pathToSave, os.path.basename(imagePrint)), quality=70)

        #img = Image.open(os.path.join(pathToImg, imagePrint)).convert('RGBA')

pathToImg = r'F:\Цвета — копия'
pathToImgLight = r'F:\Маски силикон\light3.png'
combineImage(pathToImg, pathToImgLight)