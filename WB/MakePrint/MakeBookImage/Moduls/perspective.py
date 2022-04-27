from PIL import Image
from Moduls.findCoef import find_coeffs



def transformPrint(pathToPrint):
    img = Image.open(pathToPrint)
    width, height = img.size

    XEtalon = 1437
    YEtalon = 3071
    Xscale = width/XEtalon
    Yscale = height/YEtalon

    coeffs = find_coeffs(
            [(0, 0), (width, 0), (width, height), (0, height)],
            [(int(-473*Xscale),int(-125*Yscale)), (width, 0), (width+int(357*Xscale), height), (0, height+int(132*Yscale))])

    img = img.transform((width, height), Image.PERSPECTIVE, coeffs,
            Image.BICUBIC)
    return img

# pathToImage = r'E:\print 233.png'
# img = transformPrint(pathToImage)
# img.show()
# img.save(pathToImage[0:-4] + '_2.png')