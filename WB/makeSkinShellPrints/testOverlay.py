from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from PIL import ImageOps


backgroundPath = r"F:\Downloads\Render\Case_.1.png"
printImgPath = r"F:\Downloads\Render\Varnish_.1_1.png"
image_path = r"\\192.168.0.33\shared\_Общие документы_\Егор\Модели SkinShell\Рендеры\Чехол Xiaomi 13 Lite силикон с зак.кам. черный противоуд\1_clown.png"



def overlayImage(backgroundPath, printImgPath, maskPaste):
    img = Image.open(backgroundPath)
    img = img.resize((1200,1601))

    ImageFilter.EMBOSS.filterargs=((3, 3), 8, 28, (-1, -1, -1,
                                                    -1, 30, -1,
                                                    -1, -1, -1))
    ImageFilter.CONTOUR.filterargs=((5, 5), 20, 50, (-1, -1, -1, -1, -1,
                                                    -1, -1, -1, -1, -1,
                                                    -1, -1, 47, -1, -1,
                                                    -1, -1, -1, -1, -1,
                                                    -1, -1, -1, -1, -1))
    # print(ImageFilter.CONTOUR.filterargs)
    mask = img.filter(ImageFilter.EMBOSS)

    mask = ImageEnhance.Color(mask).enhance(1)
    mask = ImageEnhance.Contrast(mask).enhance(5)
    mask = ImageEnhance.Brightness(mask).enhance(1.1)
    # открываем изображение, которое нужно наложить
    print_img = Image.open(printImgPath)
    # # изменяем размер картинки для соответствия размеру оригинального изображения
    print_img = print_img.resize(img.size)
    # # создаем пустое изображение с альфа-каналом
    # result = Image.new("RGBA", img.size, (255, 255, 255, 0))
    # # наложение изображения с помощью метода paste и маски mask.png
    # result.paste(print_img, mask=mask)
    # result = print_img
    maskNew = Image.new("RGBA", img.size, (255, 255, 255, 0))
    maskNew.paste(mask, mask=print_img)
    #maskNew.show()
    background = Image.new("RGBA", img.size, (255, 255, 255))
    tmp = Image.new("RGBA", img.size, (255, 255, 255,0))
    tmp.paste(background,mask=print_img)
    # tmp.show()
    result = Image.blend(print_img, maskNew, 0.1)
    # result.show()
    result = ImageEnhance.Color(result).enhance(1.20)
    result = ImageEnhance.Contrast(result).enhance(1.2)
    result = ImageEnhance.Brightness(result).enhance(1.0)
    #maskPaste = Image.open(maskForOverlayPath)#.convert("RGB")
    maskPaste = ImageOps.invert(maskPaste)
    tmp2 = Image.new("RGBA", img.size, (255, 255, 255,0))
    # maskPaste.show()
    tmp2.paste(result,mask=maskPaste)
    # tmp2.show()
    # result.show()
    # tmp2.show()
    # tmp = Image.alpha_composite(tmp,result)
    # tmp.show()
    # result = result.convert("RBG")
    # result.save(r"D:\output.png")
    # наложение получившегося изображения на оригинальное изображение с помощью метода Image.blend и режима наложения "overlay"
    img.paste(tmp2,mask=tmp2)
    img.show()
# # сохраняем результат
# img.save(r"D:\output.png")
def create_mask(image_path):
    image = Image.open(image_path)
    width, height = image.size
    mask = Image.new("1", (width, height))
    pixels = image.load()
    mask_pixels = mask.load()
    for x in range(width):
        for y in range(height):
            if tmp(pixels[x, y]):#(0,0,0)<=pixels[x, y]<(50,50,50):#== mask_color:
                mask_pixels[x, y] = 1
    return mask.convert("L")

def tmp(pix):
    colorMin = (0,0,0)
    colorMax = (70,70,70)
    if colorMin[0]<=pix[0]<colorMax[0]:
        if colorMin[1]<=pix[1]<colorMax[1]:
            if colorMin[2]<=pix[2]<colorMax[2]:
                return True




if __name__ =='__main__':
    maskPaste = create_mask(image_path)
    overlayImage(backgroundPath, printImgPath, maskPaste)