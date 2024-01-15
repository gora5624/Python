from os.path import join as joinPath, abspath, exists, basename, splitext
from os import listdir, makedirs
import multiprocessing
from PIL import Image, ImageDraw, ImageFont
import pandas
import re



# http://95.78.233.163:8001/wp-content/uploads/пленки/Планшеты/Глянцевая/Done/1/***.jpg;http://95.78.233.163:8001/wp-content/uploads/пленки/Планшеты/Глянцевая/4.jpg

def makeImageBookWithNameModel(colorList, modelBrand, modelModel):
    pool = multiprocessing.Pool()
    for color in colorList:
        pool.apply_async(makeImageColor, args=(color, modelBrand, modelModel,))
    pool.close()
    pool.join()
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
            imageDone.save(joinPath(fullPathToSave.replace('/','&'), pic[0:-4] + '.jpg'), quality=75)

pathToExcelWithName = r"F:\Downloads\11 партия_Макет_Медиафайлы.xlsx"
pathToImagesToPaste = ''
# pathToImagesToPasteFolder = r'\\rab\uploads\пленки\Планшеты\Матовая'
# pathToImagesToPasteFolder = r'\\rab\uploads\пленки\Планшеты\Глянцевая'
# pathToImagesToPasteFolder = r'\\rab\uploads\пленки\Смартфоны\Матовая'
pathToImagesToPasteFolder = r'\\rab\uploads\пленки\Смартфоны\Глянцевая'
listValidImageName = ["1",'2','3']
listValidFileTypes = ['.jpg']
fontPath = r'D:\Python\WB\makeNanoFilm\Fonts\CarosSoftBold.ttf'
columnName = 'Модель'


textSizeBrand = 250
textSizeModel = 500
deltaTextSize = 5

# XPasteBrand = 2662
# YPasteBrand = 996
# XPasteModel = 2662
# YPasteModel = 1153

# Планшеты
XPasteBrand = 1812
YPasteBrand = 3277
XPasteModel = XPasteBrand
YPasteModel = 3505

# Смартфоны
# XPasteBrand = 1662
# YPasteBrand = 3345
# XPasteModel = XPasteBrand
# YPasteModel = 3591

def startPasteText(pathToFile=''):
    listModels = pandas.read_excel(pathToExcelWithName)
    listModelsDict = listModels.to_dict('records')
    # listModelsDict = [{'Модель':'Tecno Camon 20/20 Pro 4G'}]
    for line in listModelsDict:
        deltaTextSize = 5
        customFontBrand = ImageFont.truetype(fontPath, textSizeBrand)
        customFontModel = ImageFont.truetype(fontPath, textSizeModel)
        brand = line[columnName].split(' ')[0]
        model = ' '.join(line[columnName].split(' ')[1:])
        image = Image.open(pathToFile)
        imageDone = Image.new('RGB', image.size)
        imageDone.paste(image)
        drawText = ImageDraw.Draw(imageDone)
        widthText, heightText = drawText.textsize(brand, font=customFontBrand)
        while widthText>1494:
                textSizeBrandNew = textSizeBrand - deltaTextSize
                customFontBrand = ImageFont.truetype(fontPath, textSizeBrandNew)
                widthText, heightText = drawText.textsize(brand, font=customFontBrand)
                deltaTextSize += 5
        while heightText>250:
                textSizeBrandNew = textSizeBrand - deltaTextSize
                customFontBrand = ImageFont.truetype(fontPath, textSizeBrandNew)
                widthText, heightText = drawText.textsize(brand, font=customFontBrand)
                deltaTextSize += 5
        drawText.text((XPasteBrand-widthText,YPasteBrand-heightText), brand, font=customFontBrand,fill='#FFFFFF')
        drawText = ImageDraw.Draw(imageDone)
        widthText, heightText = drawText.textsize(model, font=customFontModel)
        while widthText>1494:
                textSizeModelNew = textSizeModel - deltaTextSize
                customFontModel = ImageFont.truetype(fontPath, textSizeModelNew)
                widthText, heightText = drawText.textsize(model, font=customFontModel)
                deltaTextSize += 5
        while heightText>200:
                textSizeModelNew = textSizeModel - deltaTextSize
                customFontModel = ImageFont.truetype(fontPath, textSizeModelNew)
                widthText, heightText = drawText.textsize(model, font=customFontModel)
                deltaTextSize += 5
        drawText.text((XPasteBrand-widthText,YPasteModel-heightText), model, font=customFontModel,fill='#FFFFFF')        
        if not exists(fullPathToSave:=joinPath(pathToImagesToPasteFolder, 'Done', splitext(basename(pathToFile))[0])):
            makedirs(fullPathToSave)
        imageDone = imageDone.resize((900,int(imageDone.size[1]*(900/imageDone.size[0]))))
        imageDone.save(joinPath(fullPathToSave, re.sub(r'[^\w_.)()-]', '_', line[columnName]) + '.jpg'), quality=75)
        print(str(line[columnName]) + ';' + joinPath(fullPathToSave, re.sub(r'[^\w_.)()-]', '_', line[columnName]) + '.jpg').replace(r'\\rab', r'http://95.78.233.163:8001/wp-content').replace('\\','/'))


def main():
    pool = multiprocessing.Pool()
    for file in listdir(pathToImagesToPasteFolder):
        for fileTypes in listValidFileTypes:
            #if fileTypes in file:
                if file.replace(fileTypes, '') in listValidImageName:
                    pool.apply_async(startPasteText, args=(joinPath(pathToImagesToPasteFolder, file), ))
    pool.close()
    pool.join()

    

if __name__ == '__main__':
    main()