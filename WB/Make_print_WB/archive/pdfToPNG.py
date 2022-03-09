from wand.image import Image
import os

poppler_path = r'C:\Users\user\AppData\Local\Programs\Python\Python38\Lib\site-packages\poppler-0.68.0_x86\poppler-0.68.0\bin'


pathToImagePDF = r'G:\Картинки китай\Китай 3 pdf — копия'
pathToImagePNG = r'G:\Картинки китай\Китай 3 png'
for imagePDF in os.listdir(pathToImagePDF):
    fullPathToPDF = os.path.join(pathToImagePDF, imagePDF)
    with Image(filename=fullPathToPDF, resolution=300) as img:
        img.format = 'png'
        fullPathToPNG = os.path.join(
            pathToImagePNG, imagePDF.replace('.pdf', '.png'))
        img.save(filename=fullPathToPNG)
