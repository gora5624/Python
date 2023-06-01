import fitz # PyMuPDF
import io
from PIL import Image
import os
import multiprocessing
import re


dirWithPrint = r'\\192.168.0.111\shared\Отдел производство\макеты для принтера\Макеты для 6090\Оригиналы'
dirToSavePDF = r'D:\PDF'
dirToSavePNG = r'D:\PNG'
def findKoef(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    # image.show()
    image = image.resize((500, int(image.size[1]*(500/image.size[0]))))
    # image.save(os.path.join(r'E:\PDF','test.png'))
    # a = image.getpixel((499,0))
    size = image.size
    koef = ['','','','']
    for w in range(size[0]):
        for h in range(size[1]):
            pix = image.getpixel((w,h))
            if pix != (255,255,255):
                if w==0:
                    a = w/size[0]
                    koef[0] = a if a != 0 else 0
                    break
                else:
                    a = (w+1)/size[0]
                    koef[0] = a if a != 0 else 0
                    break
        if koef[0] != '':
            break
    for h in range(size[1]):
        for w in range(size[0]):
            pix = image.getpixel((w,h))
            if pix != (255,255,255):
                if h==0:
                    a = h/size[1]
                    koef[1] = a if a != 0 else 0
                    break
                else:
                    a = (h+1)/size[1]
                    koef[1] = a if a != 0 else 0
                    break
        if koef[1] != '':
            break
    for w in reversed(range(size[0])):
        for h in range(size[1]):
            pix = image.getpixel((w,h))
            if pix != (255,255,255):
                if w==0:
                    a = w/size[0]
                    koef[2] = a if a != 0 else 0
                    break
                else:
                    a = (w+1)/size[0]
                    koef[2] = a if a != 0 else 0
                    break
        if koef[2] != '':
            break
    for h in reversed(range(size[1])):
        for w in range(size[0]):
            pix = image.getpixel((w,h))
            if pix != (255,255,255):
                if h==0:
                    a = h/size[1]
                    koef[3] = a if a != 0 else 0
                    break       
                else:
                    a = (h+1)/size[1]
                    koef[3] = a if a != 0 else 0
                    break
        if koef[3] != '':
            break   

    return tuple(koef)

def makePNG(spot_1, image, file, koef):
    spotImage = Image.open(io.BytesIO(spot_1)).convert('L')
    image = Image.open(io.BytesIO(image)).convert('RGB')
    # spotImage.show()
    spotImage = spotImage.resize((500, int(spotImage.size[1]*(500/spotImage.size[0]))))
    image = image.resize((spotImage.size[0], spotImage.size[1]))
    delta = tuple(int(a*b) for a,b in zip((spotImage.size[0], spotImage.size[1], spotImage.size[0], spotImage.size[1]), koef))
    spotImage = spotImage.crop(delta)
    image = image.crop(delta)
    spotImage = spotImage.point(lambda x: 0 if x > 200 else 255)
    # image.show()
    image.putalpha(spotImage)
    image.save(os.path.join(dirToSavePNG, file.replace('pdf', 'png')))


def main(file, filePath):       
    pdf_file = fitz.open(filePath)
    outFile = fitz.open()
    for page_index in range(len(pdf_file)):
        page = pdf_file[page_index]
        text = page.get_text('dict')
        dX, dY = page.mediabox.x0, page.mediabox.y0
        w,h = page.mediabox_size.x+dX, page.mediabox_size.y+dY
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
                if border[0] != 0 and border[1] !=0:
                    w,h = border[2]-border[0], border[3]-border[1]
                    border = (border[0]-(w*0.02), border[1]-(h*0.01), border[2]+(w*0.02),border[3]+(h*0.01))
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
        # pageN.insert_image(pageN.rect, stream=spot_1)
        # pageN.insert_image(pageN.rect, stream=image)
    outFile.save(os.path.join(dirToSavePDF, file))
    f = open(os.path.join(dirToSavePDF,'cords.txt'), 'a')
    f.write(file + ','+','.join([str(cropBoxNew2.x0+dX), str(cropBoxNew2.x1+dX), str(cropBoxNew2.y0+dY),str(cropBoxNew2.y1+dY), str(w),str(h)])+'\n')
    f.close()
    # thread1 = Thread(target=savePDF, args=(dirToSavePDF, file))
    # thread1.start()
    # thread2 = Thread(target=makePNG, args=(spot_1, image, file,koef,))
    makePNG(spot_1, image, file,koef,)

    # first_page.mediabox.setLowerLeft() = pageN.rect
    # thread2.start()
    # pool.append(thread1)
    # pool.append(thread2)


if __name__ == '__main__':
    pool = multiprocessing.Pool(6)
    for file in os.listdir(dirWithPrint):
        if file not in os.listdir(dirToSavePDF):
            filePath = os.path.join(dirWithPrint, file)
            # if re.match(r'print 22.pdf', file):
            if re.match(r'print \d*.pdf', file):
                pool.apply_async(main, args=(file,filePath,))
    pool.close()
    pool.join()




