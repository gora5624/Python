from pickletools import optimize
from PIL import Image, ImageFile
from os import listdir
from os.path import join as joinPath, basename
import multiprocessing
ImageFile.LOAD_TRUNCATED_IMAGES = True


class MakePlastins():
    def __init__(self) -> None:
        self.pathToPlastinBackground = r'F:\Маски пластины\bakcgroung.png'    
        self.pathToPlastinRetangleMask = r'F:\Маски пластины\rectangleMask.png'
        self.pathToPlastinCircleMask = r'F:\Маски пластины\circleMask.png'
        self.pathToLogoPrint = r'F:\Принты пластины смешанные\лого'
        self.pathToFullPrint = r'F:\Принты пластины смешанные\полные'
        self.pathToDonePlastins = r'F:\Пластины принты готовые'
        self.leftPointToRect = 256
        self.rightPointToRect = 1384
        self.topPointToRect = 1093
        self.bottPointToRect = 2707
        self.centerCircleX = 2036
        self.centerCircleY = 2140
        self.radiusCircle = 560
    
    
    def makePlastin(self):
        pool = multiprocessing.Pool()
        rectangleMaskImg = Image.open(self.pathToPlastinRetangleMask)
        circleMaskImg = Image.open(self.pathToPlastinCircleMask)
        backgroundImg = Image.open(self.pathToPlastinBackground)
        for logoPrint in listdir(self.pathToLogoPrint):
            #printImg = Image.open(joinPath(self.pathToLogoPrint, logoPrint))
            flag = 'logo'
            pool.apply_async(self.combineImage, args=(joinPath(self.pathToLogoPrint, logoPrint), rectangleMaskImg, circleMaskImg, backgroundImg, flag, ))
        for FullPrint in listdir(self.pathToFullPrint):
            flag = 'full'
            #printImg = Image.open(joinPath(self.pathToLogoPrint, FullPrint))
            pool.apply_async(self.combineImage, args=(joinPath(self.pathToFullPrint, FullPrint), rectangleMaskImg, circleMaskImg, backgroundImg, flag, ))
        pool.close()
        pool.join()


    def combineImage(self, printPath, rectangleMaskImg, circleMaskImg, backgroundImg, flag):
        printImg = Image.open(printPath)
        sizeImg = backgroundImg.size
        mainImg = Image.new('RGB', sizeImg)
        mainImg.paste(backgroundImg, (0,0))
        if flag == 'full':
            printImgRet = printImg.resize(self.returnSizePrintForRect(printImg, flag))
            #mainImg.show()
            mainImgTMP = Image.new('RGBA', sizeImg)
            mainImgTMP.paste(printImgRet, self.returnCoordForPasteRectangleImage(printImgRet))
            mainImg.paste(mainImgTMP, (0, 0), rectangleMaskImg)
            #mainImg.show()
            #mainImg.paste(rectangleMaskImg, (0,0), rectangleMaskImg)
            #mainImg.show()
            printImgCirc = printImg.resize(self.returnSizePrintForCirc(printImg, flag))
            mainImgTMP = Image.new('RGBA', sizeImg)
            mainImgTMP.paste(printImgCirc, self.returnCoordForPasteCircleImage(printImgCirc))
            mainImg.paste(mainImgTMP, (0, 0), circleMaskImg)
            #mainImg.show()
            #mainImg.paste(circleMaskImg, (0,0), circleMaskImg)
            mainImg.save(joinPath(self.pathToDonePlastins, basename(printPath.replace('png','jpg'))), optimize=True)
        else:
            printImgRet = printImg.resize(self.returnSizePrintForRect(printImg, flag))
            #mainImg.show()
            mainImgTMP = Image.new('RGBA', sizeImg)
            mainImgTMP.paste(printImgRet, self.returnCoordForPasteRectangleImage(printImgRet), printImgRet)
            mainImg.paste(mainImgTMP, (0, 0), rectangleMaskImg)
            #mainImg.show()
            #mainImg.paste(rectangleMaskImg, (0,0), rectangleMaskImg)
            #mainImg.show()
            printImgCirc = printImg.resize(self.returnSizePrintForCirc(printImg, flag))
            mainImgTMP = Image.new('RGBA', sizeImg)
            mainImgTMP.paste(printImgCirc, self.returnCoordForPasteCircleImage(printImgCirc), printImgCirc)
            mainImg.paste(mainImgTMP, (0, 0), circleMaskImg)
            #mainImg.show()
            #mainImg.paste(circleMaskImg, (0,0), circleMaskImg)
            mainImg = mainImg.resize((749,1000))
            mainImg.save(joinPath(self.pathToDonePlastins, basename(printPath.replace('png','jpg'))), optimize=True)


    def returnSizePrintForCirc(self, printImgCirc, flag):
        if flag == 'full':
            xSize = self.radiusCircle * 2 * 1.05
            ySize = printImgCirc.size[1] * (xSize / printImgCirc.size[0])
            return (int(xSize), int(ySize))
        else:
            xSize = self.radiusCircle * 2 * 0.9
            ySize = printImgCirc.size[1] * xSize / printImgCirc.size[0]
            if ySize < (self.radiusCircle * 2 * 0.9):
                return (int(xSize), int(ySize))
            else:
                ySize = self.radiusCircle * 2 * 0.9
                xSize = printImgCirc.size[0] * (ySize / printImgCirc.size[1])
                return (int(xSize), int(ySize))


    def returnCoordForPasteCircleImage(self, printImgCirc):
        sizeImg = printImgCirc.size
        pointToPasteX = self.centerCircleX - sizeImg[0]/2
        pointToPasteY = self.centerCircleY - sizeImg[1]/2
        return (int(pointToPasteX),int(pointToPasteY))


    def returnCoordForPasteRectangleImage(self, printImgRet):
        sizeImg = printImgRet.size
        centerRectX = (self.rightPointToRect - self.leftPointToRect)/2 + self.leftPointToRect
        centerRectY = (self.bottPointToRect - self.topPointToRect)/2 + self.topPointToRect
        pointToPasteX = centerRectX - sizeImg[0]/2
        pointToPasteY = centerRectY - sizeImg[1]/2
        return (int(pointToPasteX),int(pointToPasteY))

    def returnSizePrintForRect(self, printImgRet, flag):
        if flag == 'full':
            xSize = (self.rightPointToRect - self.leftPointToRect) * 1.05
            ySize = printImgRet.size[1] * (xSize / printImgRet.size[0])
            return (int(xSize), int(ySize))
        else:
            xSize = (self.rightPointToRect - self.leftPointToRect) * 0.9
            ySize = printImgRet.size[1] * xSize / printImgRet.size[0]
            if ySize < (self.bottPointToRect - self.topPointToRect):
                return (int(xSize), int(ySize))
            else:
                ySize = (self.bottPointToRect - self.topPointToRect) * 0.9
                xSize = printImgRet.size[0] * (ySize / printImgRet.size[1])
                return (int(xSize), int(ySize))


if __name__ == '__main__':
    a = MakePlastins()
    a.makePlastin()