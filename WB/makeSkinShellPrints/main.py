from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from PIL import ImageOps
import os
import multiprocessing
import shutil
import numpy as np


caseDir = r'D:\Case'
imageDir = r'D:\Prints'
donePath = r'F:\done'
relations = {'1.png':'.1',
             '2.png':'.2',
             '3.png':'.3',
             '4.png':'.6',
             '5.png':'.4',
             '6.png':'.7',}


def create_mask(case, clownPath):
    image = Image.open(os.path.join(caseDir, case , clownPath))
    #image = image.resize((1500,2000))
    x = 5999
    y = 0
    color = image.getpixel((x, y))
    data = np.array(image)
    mask = np.full(data.shape, color)
    result = (data == mask).all(-1)
    new_image = Image.fromarray(np.uint8(result * 255) , 'L')
    # new_image.show()
    #new_image = ImageOps.invert(new_image)
    return new_image

def overlayImage(backgroundPath, printImgPath, maskPaste):
    img = Image.open(backgroundPath)
    #img = img.resize((1500,2000))

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
    mask = ImageEnhance.Contrast(mask).enhance(2)
    mask = ImageEnhance.Brightness(mask).enhance(1.5)
    print_img = printImgPath
    print_img = print_img.resize(img.size)
    maskNew = Image.new("RGBA", img.size, (255, 255, 255, 0))
    maskNew.paste(mask, mask=print_img)
    background = Image.new("RGBA", img.size, (255, 255, 255))
    tmp = Image.new("RGBA", img.size, (255, 255, 255,0))
    tmp.paste(background,mask=print_img)
    if '4.png' in backgroundPath:
        result = Image.blend(print_img, maskNew, 1)
    else:
        result = Image.blend(print_img, maskNew, 0.1)
        result = ImageEnhance.Color(result).enhance(1.20)
        result = ImageEnhance.Contrast(result).enhance(1.2)
        result = ImageEnhance.Brightness(result).enhance(1.0)
    maskPaste = ImageOps.invert(maskPaste)
    tmp2 = Image.new("RGBA", img.size, (255, 255, 255,0))
    tmp2.paste(result,mask=maskPaste)
    img.paste(tmp2,mask=tmp2)
    return img


def createBackPrint(printImage):
    alpha = printImage.split()[3]
    new_image = Image.new('RGBA', printImage.size, (145,155,147,10))
    #new_image = Image.new('RGBA', printImage.size, (255,255,255,100))
    new_image.putalpha(alpha)
    new_image = new_image.filter(ImageFilter.GaussianBlur(5))
    npImage = np.array(new_image)
    npImage[..., 3]=npImage[..., 3]*0.3
    npImage = np.clip(npImage, 0, 255)
    new_image = Image.fromarray(npImage.astype('uint8'), 'RGBA')
    #new_image.show()
    #new_image.save(r'F:\done\Чехол Honor X5 силикон с зак.кам. черный противоуд. SkinShell\tmp.png')
    return new_image


def main(caseImageNum, printImageNum, case, clownPath):
        #caseImage = Image.open(os.path.join(caseDir, case , caseImageNum)).convert('RGBA')
        mask = create_mask(case, clownPath)
        for image in os.listdir(imageDir):
            finalImagePath = os.path.join(donePath, case, image)
            if not os.path.exists(finalImagePath):
                if printImageNum in image:
                    printImage = Image.open(os.path.join(imageDir, image))
                    if '4' in caseImageNum:
                        printImage = createBackPrint(printImage)
                    #printImage.resize((1500,2000))
                    final = overlayImage(os.path.join(caseDir, case , caseImageNum), printImage, mask)
                    #final.show()
                    #printImageNew = Image.composite(printImage,caseImage, mask)
                    #printImageNew.show()
                    #final = Image.alpha_composite(caseImage,printImage)
                    if not os.path.exists(os.path.join(donePath, case)):
                        os.makedirs(os.path.join(donePath, case))                      
                    # x,y = final.size
                    final = final.resize((1500,2000), Image.LANCZOS)
                    final.save(finalImagePath)
                    # shutil.copy(os.path.join(caseDir, case , '5.png'), os.path.join(donePath, case))

                    #caseImage

def returnClownPath(caseImageNum):
    if '5' in caseImageNum:
        return '4_clown.png'
    elif  '6' in caseImageNum:
        return '7_clown.png'
    elif  '4' in caseImageNum:
        return '6_clown.png'
    else:
        return caseImageNum.replace('.png','_clown.png')

if __name__ == '__main__':
    for case in os.listdir(caseDir):
        # if not os.path.exists(os.path.join(donePath, case)):
            pool = multiprocessing.Pool(6)
            for caseImageNum, printImageNum in relations.items():
                clownPath = returnClownPath(caseImageNum)
                # clownPath = caseImageNum.replace('.png','_clown.png')
                pool.apply_async(main, args=(caseImageNum, printImageNum, case, clownPath,))
                # main(caseImageNum, printImageNum, case)
            pool.close()
            pool.join()
    