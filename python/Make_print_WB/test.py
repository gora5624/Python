from PIL import Image
import os
from my_lib import file_exists
import copy

pathToMaskFolder = r'D:\fon.png'
pathToPrintFolder = r'D:\NewPrint'
pathToDonePrints = r'D:\printsPy'


image = Image.open(pathToMaskFolder).convert("RGB")
rgbaCentr = image.getpixel((1748, 1550))
for x in range(1100, 1453):
    b = 'No'
    rgba = image.getpixel((x, 765))
    color2 = rgba[0]+rgba[1]+rgba[2]
    if:
        b = 'Yes'
    print((x, rgba, b))
