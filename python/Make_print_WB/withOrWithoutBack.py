from PIL import Image
import os


mainDir = r'G:\Картинки китай\Китай 2 png — копия'

for file in os.listdir(mainDir):
    filePath = os.path.join(mainDir, file)
    if os.path.isdir(filePath):
        continue
    image = Image.open(filePath).convert("RGBA")
    size = image.size
    yTop = 10
    count = 0
    for yTop in range(10, size[1]-10):
        xLeft = 5
        for xLeft in range(5, size[0]-5):
            rgba = image.getpixel((xLeft, yTop))
            if rgba[3] != 255:
                count += 1
                if count > 10:
                    try:
                        os.replace(filePath, filePath.replace(
                            r'Китай 2 png — копия', r'Китай 2 png — копия\Без фона'))
                    except:
                        pass
                    break
            xLeft += 1
        break
