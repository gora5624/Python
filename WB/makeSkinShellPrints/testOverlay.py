from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from PIL import ImageOps

# открываем изображение с оригинальным изображением
img = Image.open(r"D:\1.png")

ImageFilter.EMBOSS.filterargs=((3,3), 1, 150, (-1, 0, 0, 0, 1, 0, 0, 0, 0,))
ImageFilter.CONTOUR.filterargs=((3, 3), 1, 210, (-1, -1, -1, -1, 8, -1, -1, -1, -1))
# print(ImageFilter.CONTOUR.filterargs)
mask = img.filter(ImageFilter.CONTOUR)
# mask.show()
# открываем изображение с тиснением
# mask = Image.open(r"D:\uot.png")

# открываем изображение, которое нужно наложить
print_img = Image.open(r"D:\test.png")

new = Image.new("RGBA", img.size, (255, 255, 255, 0))
new.paste(print_img,(387,183), print_img)
# изменяем размер картинки для соответствия размеру оригинального изображения
print_img = print_img.resize(img.size)

# создаем пустое изображение с альфа-каналом
result = Image.new("RGBA", img.size, (255, 255, 255, 0))

# наложение изображения с помощью метода paste и маски mask.png
result.paste(print_img, mask=mask)
maskNew = Image.new("RGBA", img.size, (255, 255, 255, 0))
maskNew.paste(mask, mask=print_img)
# maskNew.show()
background = Image.new("RGBA", img.size, (255, 255, 255))
tmp = Image.new("RGBA", img.size, (255, 255, 255,0))
tmp.paste(background,mask=print_img)
# tmp.show()
result = Image.blend(print_img, maskNew, 0.2)
# result.show()
result = ImageEnhance.Color(result).enhance(1.30)
result = ImageEnhance.Contrast(result).enhance(1.3)
result = ImageEnhance.Brightness(result).enhance(0.95)
# print_img.show()
maskPaste = Image.open(r"D:\chBmask.png")#.convert("RGB")
# maskPaste.show()
maskPaste = ImageOps.invert(maskPaste)
# maskPaste.show()
tmp2 = Image.new("RGBA", img.size, (255, 255, 255,0))
tmp2.paste(result,mask=maskPaste)
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