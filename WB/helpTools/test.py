import fitz # PyMuPDF
import io
from PIL import Image
import os
from threading import Thread


dirWithPrint = r'\\192.168.0.111\shared\Отдел производство\макеты для принтера\Макеты для 6090\Оригиналы'
dirToSavePDF = r'E:\PDF'
dirToSavePNG = r'E:\PNG'
def findKoef(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image = image.resize((500, int(image.size[1]*(500/image.size[0]))))
    size = image.size
    koef = [1,1,1,1]
    for w in range(size[0]):
        for h in range(size[1]):
            pix = image.getpixel((w,h))
            if pix != (255,255,255):
                a = w/size[0]
                koef[0] = a if a != 0 else 0
                break
        if koef[0] != 1:
            break
    for h in range(size[1]):
        for w in range(size[0]):
            pix = image.getpixel((w,h))
            if pix != (255,255,255):
                a = h/size[1]
                koef[1] = a if a != 0 else 0
                break
        if koef[1] != 1:
            break
    for w in reversed(range(size[0])):
        for h in range(size[1]):
            pix = image.getpixel((w,h))
            if pix != (255,255,255):
                a = w/size[0]
                koef[2] = a if a != 0 else 0
                break
        if koef[2] != 1:
            break
    for h in reversed(range(size[1])):
        for w in range(size[0]):
            pix = image.getpixel((w,h))
            if pix != (255,255,255):
                a = h/size[1]
                koef[3] = a if a != 0 else 0
                break
        if koef[3] != 1:
            break   

    return tuple(koef)

def makePNG(spot_1, image, file, koef):

    spotImage = Image.open(io.BytesIO(spot_1)).convert('L')
    spotImage = spotImage.resize((500, int(spotImage.size[1]*(500/spotImage.size[0]))))
    # sizeRect = (0,0,spotImage.size[0],spotImage.size[1])
    delta = tuple(int(a*b) for a,b in zip((spotImage.size[0], spotImage.size[1], spotImage.size[0], spotImage.size[1]), koef))
    # cropBorder = tuple(a*b for a,b in zip(sizeRect, koef))
    spotImage = spotImage.crop(delta)
    # spotImage.show()
    spotImage = spotImage.point(lambda x: 0 if x > 200 else 255)
    image = Image.open(io.BytesIO(image)).convert('RGB')
    # image.show()
    image = image.resize((500, int(image.size[1]*(500/image.size[0]))))
    image = image.crop(delta)
    # image.show()
    # spotImage = spotImage.resize(image.size)
    # 
    image.putalpha(spotImage)
    # image.show()
    image = image.resize((500, int(image.size[1]*(500/image.size[0]))))
    image.save(os.path.join(dirToSavePNG, file.replace('pdf', 'png')))

def savePDF(dirToSavePDF, file):
    outFile.save(os.path.join(dirToSavePDF, file))

pool = []
for file in os.listdir(dirWithPrint):
    if file not in os.listdir(dirToSavePDF):
        filePath = os.path.join(dirWithPrint, file)
        # open the file
        if 'pdf' in file:
            pdf_file = fitz.open(filePath)
            outFile = fitz.open()
            for page_index in range(len(pdf_file)):
                page = pdf_file[page_index]
                text = page.get_text('dict')
                dX, dY = page.cropbox[0], page.cropbox[1]
                delta = (dX, dY, dX, dY)
                # deltaMy = (-1, -1, 1, 1)
                image_list = page.get_images()
                for image_index, img in enumerate(image_list, start=1):
                    xref = img[0]
                    base_image = pdf_file.extract_image(xref)
                    
                    if 'Spot_1' in base_image['cs-name']:
                        spot_1 = base_image["image"]
                        koef = findKoef(spot_1)
                        try:
                            bbox = text['blocks'][image_index]['bbox']
                        except IndexError:
                            bbox = page.rect
                        border =  (bbox[0] + bbox[2]*koef[0], bbox[1] + bbox[3]*koef[1], bbox[2]*koef[2], bbox[3]*koef[3])
                        break
                for image_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = pdf_file.extract_image(xref)
                    if base_image:
                        if 'Spot'  in base_image['cs-name']:
                            continue
                        else:
                            pix = fitz.Pixmap(pdf_file, xref)
                            pix0 = fitz.Pixmap(fitz.csRGB, pix)
                            # pix0.save(r'E:\tst1.png')
                            image = pix0.tobytes()
                            # f = open(r'E:\tst.jpeg', 'wb')
                            # f.write(image)
                            # f.close()
                            break
                    else:
                        # image = base_image["image"]
                        pix = fitz.Pixmap(pdf_file, xref)
                        pix0 = fitz.Pixmap(fitz.csRGB, pix)
                        # pix0.save(r'E:\tst1.png')
                        image = pix0.tobytes()
                        # f = open(r'E:\tst.jpeg', 'wb')
                        # f.write(image)
                        # f.close()
                        break
                # cropBoxNew = tuple(a + b for a,b in zip(bbox, border))
                # cropBoxNew = tuple(a+b for a,b in zip(border, delta))
                # cropBoxNew = tuple(a+b for a,b in zip(cropBoxNew, deltaMy))
                # page.set_cropbox(cropBoxNew)
                # page.set_mediabox(cropBoxNew)
                # pdf_file.reload_page(page)
                cropBoxNew2 = fitz.Rect(border)
                pageN = outFile.new_page(-1, width = cropBoxNew2.x1 - cropBoxNew2.x0, height = cropBoxNew2.y0 - cropBoxNew2.y1)
                pageN.show_pdf_page(pageN.rect, pdf_file, 0, clip = cropBoxNew2)
            savePDF(dirToSavePDF, file)
            # thread1 = Thread(target=savePDF, args=(dirToSavePDF, file))
            # thread1.start()
            # thread2 = Thread(target=makePNG, args=(spot_1, image, file,koef,))
            makePNG(spot_1, image, file,koef,)
            # thread2.start()
            # pool.append(thread1)
            # pool.append(thread2)
 

for t in pool:
    t.join()



