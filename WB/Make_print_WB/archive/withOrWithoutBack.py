from PIL import Image
import os


mainDir = r'G:\Картинки китай\Китай 1 png'
doneDir = r'G:\Картинки китай\без фона'

for file in os.listdir(mainDir):
    filePath = os.path.join(mainDir, file)
    if os.path.isdir(filePath):
        continue
    image = Image.open(filePath).convert("RGBA")
    size = image.size
    yTop = 10
    count = 0
    yStart = 10 if size[1] < 700 else 100
    xStart = 10 if size[0] < 500 else 100
    for yTop in range(yStart, size[1]-10):
        xLeft = 5
        for xLeft in range(xStart, size[0]-5):
            rgba = image.getpixel((xLeft, yTop))
            if rgba[3] != 255:
                count += 1
                if count > 10:
                    try:
                        os.replace(filePath, os.path.join(doneDir, file))
                    except:
                        pass
                    break
            xLeft += 1
        break
