from PIL import ImageOps, ImageDraw, ImageEnhance, Image, ImageFilter, ImageFont
import os
# import multiprocessing
from multiprocessing import Process, Queue, cpu_count
from threading import Thread
import re
import numpy as np
from shutil import copytree
import cv2
import numpy as np
from copy import deepcopy
# import time
# import asyncio
# import aiofiles


deltaForMask = 0.015 # на сколько уменьшаем отновсительно чехла рахмер принта
pathToNewPocket = r'D:\case' # пусть к фоткам чехлов и клоунам
pathToPrintImage = r'F:\Принты_05032024_выбрано' # Путь откуда брать фотки для натяжки
pathToSaveDone = r'D:\done' # Куда класть готовое
clownName = r'1_clown.png' # нахвание файла клоуна
flag = False
SIZE = (1800,2400)

def main(pathToNewPocket, dirName):

    pathToImageDir = os.path.join(pathToNewPocket, dirName)

    backImage = Image.open(os.path.join(pathToImageDir, '1.png')).resize(SIZE)
    coordToMaskCard = findCoordsToMaskCard(backImage)
    mask = createMaskForShadows(backImage, coordToMaskCard)
    maskImage, top_left, bottom_right = createMask(pathToImageDir)

    if maskImage == 0:
        print(pathToImageDir + ' файл с маски не обнаружен')
        return
    
    lenListPrint = len(os.listdir(pathToPrintImage))
    countProcess = max(1, min(int(cpu_count() - 2), lenListPrint))

    queue = Queue()
    listForProcess = []
    listProcess = []

    saveProcess = Thread(target=imageSaver, args=(queue,dirName))
    saveProcess.start()

    for i in range(0,lenListPrint,int(lenListPrint/countProcess)):
        listForProcess.append(os.listdir(pathToPrintImage)[i:i+int(lenListPrint/countProcess)])

    for listImagePath in listForProcess:
        p = Process(target=createPrintImage, args=(listImagePath, mask, maskImage, backImage, top_left, bottom_right, queue))
        listProcess.append(p)
        p.start()

    for p in listProcess:
        p.join()

    queue.put(None)
    print('done')
    saveProcess.join()
    

def imageSaver(queue, dirName):
    """Функция сохраняющего процесса."""
    if not os.path.exists(tmp:=os.path.join(pathToSaveDone, dirName)):
        os.mkdir(tmp)
    while True:
        item = queue.get()
        if item is None:  # Использование сигнального объекта для определения окончания работы
            break
        image, filename = item
        image_path = os.path.join(pathToSaveDone,dirName, filename.replace('png','jpg'))
        # image_path = os.path.join(pathToSaveDone,dirName, filename)

        # print(filename)
        # image.show()
        image.save(image_path, quality=80)
        # image.save(image_path)

def findCoordsToMaskCard(backImage):
    # Открываем изображение
    target_color = backImage.getpixel((530,1000))
    deltaX = 360
    deltaY = 870
    image = backImage.crop((deltaX,deltaY,900,1000))
    tolerance = 5
    # image.show()
    # Преобразуем изображение в массив NumPy
    img_array = np.array(image)
    # image = Image.open(backImage)
    # image
    
    # Разделяем целевой цвет на компоненты
    target_r, target_g, target_b = target_color
    
    # Вычисляем абсолютную разницу между целевым цветом и цветами пикселей
    color_diff = np.abs(img_array - [target_r, target_g, target_b])
    
    # Находим маску, где цвет пикселя близок к целевому цвету с учетом допуска
    mask = np.all(color_diff <= tolerance, axis=-1)
    
    # Находим координаты пикселей, удовлетворяющих условию
    coords = np.argwhere(mask)
    
    if len(coords) > 0:
        # Находим минимальные значения x и y
        min_y, min_x = np.min(coords, axis=0)
        
        # print(f"Приблизительный цвет {target_color} найден на координатах (x, y): ({min_x+deltaX}, {min_y+deltaY})")
        return min_x+deltaX, min_y+deltaY
    else:
        # print(f"Приблизительный цвет {target_color} не найден на изображении.")
        return None, None

def maskCard(coordToMaskCard, mask):
        draw = ImageDraw.Draw(mask)
        # Рассчитываем координаты нижнего правого угла
        x = coordToMaskCard[0]-15
        y = coordToMaskCard[1]-10
        color = mask.getpixel((x-2, y))
        bottom_right_x = x + 500
        bottom_right_y = y + 1100
        if flag:
            draw.rectangle([x, y, bottom_right_x, bottom_right_y], outline=color, fill=color)
        # mask.show()
        return mask


def createMaskForShadows(backImage, coordToMaskCard):
    img = ImageOps.invert(backImage)
    img = maskCard(coordToMaskCard, img)
    ImageFilter.EMBOSS.filterargs=((3, 3), 8, 28, (-1, -1, -1,
                                                        -1, 30, -1,
                                                        -1, -1, -1))
    ImageFilter.CONTOUR.filterargs=((5, 5), 20, 50, (-1, -1, -1, -1, -1,
                                                            -1, -1, -1, -1, -1,
                                                            -1, -1, 47, -1, -1,
                                                            -1, -1, -1, -1, -1,
                                                            -1, -1, -1, -1, -1))
    mask = img.filter(ImageFilter.EMBOSS)
    mask = ImageEnhance.Color(mask).enhance(3)
    mask = ImageEnhance.Contrast(mask).enhance(10)
    mask = ImageEnhance.Brightness(mask).enhance(1.5)
    # mask.show()
    return mask


def createPrintImage(listImagePath, mask, maskImage,backImage, top_left, bottom_right, queue):
    maskImage = ImageOps.invert(maskImage)
    coordsToPaste = top_left
    # img = deepcopy(backImage)
    # img = backImage
    #mask = #createMaskForShadows(backImage, coordToMaskCard)
    for printImageName in listImagePath:
        maskNew = Image.new("RGBA", backImage.size, (255, 255, 255, 0))
        img = Image.new("RGBA", backImage.size, (255, 255, 255, 0))
        img.paste(backImage)
        if '.png' in printImageName:
            printImage = Image.open(os.path.join(pathToPrintImage,printImageName))
            # printImage = Image.open(printImagePath)
            if printImage.mode != 'RGBA':
                printImage = printImage.convert('RGBA')
            printImage = transformPrintImage(printImage, top_left, bottom_right)
            printDisplacement = Image.new("RGBA", mask.size, (255, 255, 255, 0))
            printDisplacement.paste(printImage, coordsToPaste, printImage)
            maskNew.paste(mask, mask=printDisplacement)
            # maskNew.show()
            result = Image.blend(printDisplacement, maskNew, 0.1)
            result = ImageEnhance.Color(result).enhance(1.1)
            result = ImageEnhance.Contrast(result).enhance(1.00)
            result = ImageEnhance.Brightness(result).enhance(1.3)
            # maskImage = ImageOps.invert(maskImage)
            tmp2 = Image.new("RGBA", img.size, (255, 255, 255, 0))
            tmp2.paste(result,mask=maskImage)
            img.paste(tmp2,mask=tmp2)
            # img.show()
            # img.save(os.path.join(r'F:\Принты_05032024_выбрано\tmp', printImagePath))
            img = img.resize((900,1200))
            queue.put((img.convert('RGB'), printImageName))
            # queue.put((img, printImageName))
            # print(printImageName)
            # img.show()
    return 0
    

def transformPrintImage(printImage, top_left, bottom_right):
    # printImage = Image.open(os.path.join(pathToPrintImage,printImagePath))
    frameForPrint = (bottom_right[0]-top_left[0], bottom_right[1]-top_left[1])
    (wPrint, hPrint) = printImage.size
    printImage = printImage.resize((int(wPrint*(frameForPrint[1]/hPrint)), int(hPrint*(frameForPrint[1]/hPrint))))
    (wPrint, hPrint) = printImage.size
    if wPrint<frameForPrint[0]:
        printImage = printImage.resize((int(wPrint*(frameForPrint[0]/wPrint)), int(hPrint*(frameForPrint[0]/wPrint))))
    return printImage



def createMask(pathToImageDir):
    if not os.path.exists(pathToMaskFile:=os.path.join(pathToImageDir, clownName)):
        # print(pathToImageDir + ' файл с маски не обнаружен')
        return 0, 0, 0
    # image.show()
    image, top_left, bottom_right = transformMask(pathToMaskFile)
    x = int((bottom_right[0]-top_left[0])/2+top_left[0])
    y = int((bottom_right[1]-top_left[1])/2+top_left[1])
    color = image.getpixel((x, y))
    data = np.array(image)
    mask = np.full(data.shape, color)
    result = (data == mask).all(-1)
    new_image = Image.fromarray(np.uint8(result * 255) , 'L')
    new_image = ImageOps.invert(new_image)
    # new_image.show()
    return new_image, top_left, bottom_right


def transformMask(pathToMaskFile):
    top_left, bottom_right, radius, image = find_largest_bounding_box(pathToMaskFile)
    rect_color = (255, 255, 255)  # цвет прямоугольника (белый)
    thickness = -1  # заливка
    rect_mask = np.zeros_like(image)
    cv2.rectangle(rect_mask, (top_left[0]+radius, top_left[1]), (bottom_right[0]-radius, bottom_right[1]), rect_color, thickness)
    cv2.rectangle(rect_mask, (top_left[0], top_left[1]+radius), (bottom_right[0], bottom_right[1]-radius), rect_color, thickness)
    cv2.circle(rect_mask, (top_left[0]+radius, top_left[1]+radius), radius, rect_color, thickness)
    cv2.circle(rect_mask, (bottom_right[0]-radius, top_left[1]+radius), radius, rect_color, thickness)
    cv2.circle(rect_mask, (top_left[0]+radius, bottom_right[1]-radius), radius, rect_color, thickness)
    cv2.circle(rect_mask, (bottom_right[0]-radius, bottom_right[1]-radius), radius, rect_color, thickness)
    image = np.where(rect_mask == rect_color, image, (0,0,0)).astype(np.uint8) # Принудительное приведение типа
    rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_img)
    # pil_image.show()
    return pil_image, top_left, bottom_right


def find_largest_bounding_box(image_path):
    file = open(image_path, 'rb')
    chunk = file.read()
    chunk_arr = np.frombuffer(chunk, dtype=np.uint8)
    image = cv2.imdecode(chunk_arr, cv2.IMREAD_COLOR)
    dim = (SIZE)
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    # cv2.imshow('image',image)
    # cv2.waitKey(0)
    if image is None:
        print(f"Failed to load image: {image_path}")
        return
    image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('image',gray)
    # cv2.waitKey(0)
    _, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x_min, y_min = np.inf, np.inf
    x_max, y_max = 0, 0
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if (240 < w < 260):# and (465 < h < 480):
            print(1)
        x_min, y_min = min(x_min, x), min(y_min, y)
        x_max, y_max = max(x_max, x+w), max(y_max, y+h)
    
    radius = None
    j = 2
    while radius is None:
        for i in range(y_min+j, y_max):
            color = tuple(image[i, x_min+j])
            if color != (0, 0, 0):
                radius = i-y
                break
        j+=1
    if radius >150:
        radius = None
        j = 2
        while radius is None:
            for i in range(y_min+j, y_max):
                color = tuple(image[i, x_min+j+7])
                if color != (0, 0, 0):
                    radius = i-y
                    break
            j+=1

    # if radius is None:
    #     for i in range(y_min+3, h):
    #         color = tuple(image[i, x_min+3])
    #         if color != (0, 0, 0):
    #             radius = i-y
    #             break
    # print(f"Coordinates of the largest bounding box: ({x_min}, {y_min}), ({x_max}, {y_max})")
    return (int(x_min+SIZE[0]*deltaForMask), int(y_min+SIZE[0]*deltaForMask)), (int(x_max-SIZE[0]*deltaForMask), int(y_max-SIZE[0]*deltaForMask)), radius, image

if __name__ == '__main__':
    for dirName in os.listdir(pathToNewPocket):
        main(pathToNewPocket, dirName)