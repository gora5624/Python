from PIL import Image, ImageOps, ImageEnhance
import cv2
import numpy as np

def get_mask_area_color(mask_image, x, y):
    return tuple(mask_image[y, x])

def adjust_color_and_find_area(mask_image, color):
    mask = cv2.inRange(mask_image, np.array(color), np.array(color))
    mask_contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_area = 0
    largest_area_contour = None

    for contour in mask_contours:
        area = cv2.contourArea(contour)
        if area > largest_area:
            largest_area = area
            largest_area_contour = contour

    return largest_area_contour

def get_insertion_info(mask_area_contour):
    rect = cv2.minAreaRect(mask_area_contour)
    ((center_x, center_y), (width, height), angle) = rect

    return (width, height, (center_x, center_y), angle)

def get_color_at_point(image_path, x, y):
    image = Image.open(image_path)
    image = image.resize((6000, 8000))
    pixels = image.load()
    return pixels[x, y]


def create_mask(image_path, mask_color, filename="result.png"):
    image = Image.open(image_path)
    image = image.resize((6000,8000))
    width, height = image.size
    mask = Image.new("1", (width, height))
    pixels = image.load()
    mask_pixels = mask.load()
    
    for x in range(width):
        for y in range(height):
            if pixels[x, y] == mask_color:
                mask_pixels[x, y] = 1
    
    return mask


mask_image_file = r"D:\1_clown.png"
mask_image = cv2.imread(mask_image_file)
mask_image = cv2.resize(mask_image, (6000,8000), interpolation=cv2.INTER_LINEAR)

x, y = 3700, 4200

mask_area_color = get_mask_area_color(mask_image, x, y)

mask_area_contour = adjust_color_and_find_area(mask_image, mask_area_color)

insertion_width, insertion_height, insertion_center, insertion_angle = get_insertion_info(mask_area_contour)

stamp_image_file = r"D:\print 2.png"
input_image_file = r"D:\Модели SkinShell\Чехол Xiaomi 13 Lite силикон с зак.кам. черный противоуд\Карточки\1 — копия.png"

def pasteImage(insertion_center, insertion_height, insertion_width, insertion_angle, stamp_image_file, input_image_file):
    if insertion_height < insertion_width:
        insertion_height, insertion_width = insertion_width, insertion_height
        insertion_angle = - insertion_angle
    else:
        insertion_angle = 90 - insertion_angle
    insertion_width = insertion_width
    printImg = Image.open(stamp_image_file)
    img = Image.open(input_image_file)
    img=img.resize((6000,8000))
    sizeNew = int(insertion_width), int(printImg.size[1]*insertion_width/printImg.size[0])
    imageForSize = Image.new("RGBA",(int(insertion_width),int(insertion_height)))
    # imageForSize.save(r"D:\output3.png", dpi=(300,300))
    # imageForSize = Image.open(r"D:\output3.png")
    # imageForSize.save(r"D:\output4.png")
    printImgRes = printImg.resize(sizeNew)
    # printImgRes.show()
    # printImgRes1 = printImg.resize(sizeNew, resample=Image.ANTIALIAS)
    # printImgRes1.show()
    imageForSize.paste(printImgRes,(int(imageForSize.size[0]/2-printImgRes.size[0]/2),int(imageForSize.size[1]-printImgRes.size[1])),printImgRes)
    # imageForSize.show()
    imageForSize = imageForSize.rotate(insertion_angle, expand=True)
    # printImgRot = printImgRes.rotate(insertion_angle, expand=True)
    # box = printImgRot.getbbox()
    # cropped = printImgRot.crop(box)
    new = Image.new("RGBA",img.size,(0,0,0,0), )
    # new.show()
    new.paste(img,(0,0))
    coordsTopaste = (int(insertion_center[0])-int(imageForSize.size[0]/2) , int(insertion_center[1])-int(imageForSize.size[1]/2))
    new.paste(imageForSize,coordsTopaste, imageForSize)
    color_at_point = get_color_at_point(mask_image_file, x, y)
    maskBg = create_mask(mask_image_file, color_at_point)
    maskBg = maskBg.convert("L")
    maskBg = ImageOps.invert(maskBg)
    # result = Image.new("RGBA", maskBg.size)
    new.paste(img, mask=maskBg)
    new=new.resize((1200,1600))
    new = ImageEnhance.Color(new).enhance(1.30)
    new = ImageEnhance.Contrast(new).enhance(1.05)
    new = ImageEnhance.Brightness(new).enhance(1)
    new.save(r"D:\output.png")
pasteImage(insertion_center, insertion_width, insertion_height, insertion_angle, stamp_image_file, input_image_file)