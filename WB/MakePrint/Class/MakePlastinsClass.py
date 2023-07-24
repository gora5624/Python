from PIL import Image, ImageFile
from os import listdir
from os.path import join as joinPath, basename
import multiprocessing
ImageFile.LOAD_TRUNCATED_IMAGES = True


class MakePlastins():
    def __init__(self) -> None:
        self.pathToPlastinBackground = r"D:\OpenServer\domains\wordpress\wp-content\uploads\Комплекты бейдж\fonLenta.png"
        # self.pathToPlastinBackground = r"\\192.168.0.33\shared\_Общие документы_\Егор\Архив масок ВБ\Комплекты бейдж\fonSize.png"
        #self.pathToPlastinRetangleMask = r"\\192.168.0.33\shared\_Общие документы_\Егор\Архив масок ВБ\Маски пластины\rectangleMask.png"
        self.pathToPlastinRetangleMask = r"D:\OpenServer\domains\wordpress\wp-content\uploads\Комплекты бейдж\maskLenta.png"
        self.pathToPlastinCircleMask = r"\\192.168.0.33\shared\_Общие документы_\Егор\Архив масок ВБ\Маски пластины\circleMask.png"
        self.pathToLogoPrint = r'F:\Принты пластины смешанные\лого'
        self.pathToFullPrint = r'F:\Принты пластины смешанные\полные'
        self.pathToDonePlastins = r'F:\Пластины принты готовые'
        # self.leftPointToRect = 55
        # self.rightPointToRect = 295
        # self.topPointToRect = 235
        # self.bottPointToRect = 578
        # self.centerCircleX = 436
        # self.centerCircleY = 459
        # self.radiusCircle = 118

        self.leftPointToRect = 212
        self.rightPointToRect = 640
        self.topPointToRect = 222
        self.bottPointToRect = 874
        self.centerCircleX = 436
        self.centerCircleY = 459
        self.radiusCircle = 118    

    def makePlastin(self, i):
        if i == 1:
            pool = multiprocessing.Pool()
            rectangleMaskImg = Image.open(self.pathToPlastinRetangleMask)
            circleMaskImg = Image.open(self.pathToPlastinCircleMask)
            backgroundImg = Image.open(self.pathToPlastinBackground)
            for logoPrint in listdir(self.pathToLogoPrint):
                #printImg = Image.open(joinPath(self.pathToLogoPrint, logoPrint))
                flag = 'logo'
                # if 'print 22.png' in logoPrint:
                if 'Thumbs.db' not in logoPrint:
                    pool.apply_async(self.combineImage, args=(joinPath(self.pathToLogoPrint, logoPrint), rectangleMaskImg, circleMaskImg, backgroundImg, flag, ))
            for FullPrint in listdir(self.pathToFullPrint):
                flag = 'full'
                #printImg = Image.open(joinPath(self.pathToLogoPrint, FullPrint))
                # if 'print 22.png' in FullPrint:
                if 'Thumbs.db' not in FullPrint:
                    pool.apply_async(self.combineImage, args=(joinPath(self.pathToFullPrint, FullPrint), rectangleMaskImg, circleMaskImg, backgroundImg, flag, ))
            pool.close()
            pool.join()
        else:
            pool = multiprocessing.Pool()
            rectangleMaskImg = Image.open(self.pathToPlastinRetangleMask)
            #circleMaskImg = Image.open(self.pathToPlastinCircleMask)
            backgroundImg = Image.open(self.pathToPlastinBackground)
            for logoPrint in listdir(self.pathToLogoPrint):
                #printImg = Image.open(joinPath(self.pathToLogoPrint, logoPrint))
                flag = 'logo'
                if 'Thumbs.db' not in logoPrint:
                    pool.apply_async(self.combineImage2, args=(joinPath(self.pathToLogoPrint, logoPrint), rectangleMaskImg, backgroundImg, flag, ))
            for FullPrint in listdir(self.pathToFullPrint):
                flag = 'full'
                #printImg = Image.open(joinPath(self.pathToLogoPrint, FullPrint))
                if 'Thumbs.db' not in FullPrint:
                    pool.apply_async(self.combineImage2, args=(joinPath(self.pathToFullPrint, FullPrint), rectangleMaskImg, backgroundImg, flag, ))
            pool.close()
            pool.join()


    def combineImage(self, printPath, rectangleMaskImg, circleMaskImg, backgroundImg, flag):
        # if 'print 22.png' in printPath:
            # print('')
        printImg = Image.open(printPath)
        # if 'print 22.png' in printPath:
            # printImg.show()
        sizeImg = backgroundImg.size
        mainImg = Image.new('RGB', sizeImg)
        mainImg.paste(backgroundImg, (0,0))
        if 'print 22.png' in printPath:
            mainImg.show()
        if flag == 'full':
            printImgRet = printImg.resize(sizeTMP:=self.returnSizePrintForRect(printImg, flag))
            # rectangleMaskImg = rectangleMaskImg.resize(sizeTMP)
            # mainImg.show()
            mainImgTMP = Image.new('RGBA', sizeImg)
            mainImgTMP.paste(printImgRet, self.returnCoordForPasteRectangleImage(printImgRet))
            # mainImgTMP.show()
            mainImg.paste(mainImgTMP, (0, 0), rectangleMaskImg)
            # mainImg.show()
            #mainImg.paste(rectangleMaskImg, (0,0), rectangleMaskImg)
            # mainImg.show()
            printImgCirc = printImg.resize(sizeTMP:=self.returnSizePrintForCirc(printImg, flag))
            # circleMaskImg = circleMaskImg.resize(sizeTMP)
            mainImgTMP = Image.new('RGBA', sizeImg)
            mainImgTMP.paste(printImgCirc, self.returnCoordForPasteCircleImage(printImgCirc))
            mainImg.paste(mainImgTMP, (0, 0), circleMaskImg)
            #mainImg.show()
            #mainImg.paste(circleMaskImg, (0,0), circleMaskImg)
            mainImg.save(joinPath(self.pathToDonePlastins, basename(printPath)))
        else:
            printImgRet = printImg.resize(sizeTMP:=self.returnSizePrintForRect(printImg, flag))
            # rectangleMaskImg = rectangleMaskImg.resize(sizeTMP)
            #mainImg.show()
            mainImgTMP = Image.new('RGBA', sizeImg)
            mainImgTMP.paste(printImgRet, self.returnCoordForPasteRectangleImage(printImgRet), printImgRet)
            mainImg.paste(mainImgTMP, (0, 0), rectangleMaskImg)
            #mainImg.show()
            #mainImg.paste(rectangleMaskImg, (0,0), rectangleMaskImg)
            #mainImg.show()
            printImgCirc = printImg.resize(sizeTMP:=self.returnSizePrintForCirc(printImg, flag))
            # circleMaskImg = circleMaskImg.resize(sizeTMP)
            mainImgTMP = Image.new('RGBA', sizeImg)
            mainImgTMP.paste(printImgCirc, self.returnCoordForPasteCircleImage(printImgCirc), printImgCirc)
            mainImg.paste(mainImgTMP, (0, 0), circleMaskImg)
            #mainImg.show()
            #mainImg.paste(circleMaskImg, (0,0), circleMaskImg)
            mainImg.save(joinPath(self.pathToDonePlastins, basename(printPath)))


    def combineImage2(self, printPath, rectangleMaskImg, backgroundImg, flag):
        printImg = Image.open(printPath)
        #printImg.show()
        sizeImg = backgroundImg.size
        mainImg = Image.new('RGB', sizeImg)
        mainImg.paste(backgroundImg, (0,0))
        # mainImg.show()
        if flag == 'full':
            printImgRet = printImg.resize(sizeTMP:=self.returnSizePrintForRect(printImg, flag))
            # rectangleMaskImg = rectangleMaskImg.resize(sizeTMP)
            # mainImg.show()
            mainImgTMP = Image.new('RGBA', sizeImg)
            mainImgTMP.paste(printImgRet, self.returnCoordForPasteRectangleImage(printImgRet))
            # mainImgTMP.show()
            mainImg.paste(mainImgTMP, (0, 0), mainImgTMP)
            mainImg.paste(rectangleMaskImg, (0, 0), rectangleMaskImg)
            # mainImg.show()
            #mainImg.paste(rectangleMaskImg, (0,0), rectangleMaskImg)
            #mainImg.show()
            #printImgCirc = printImg.resize(self.returnSizePrintForCirc(printImg, flag))
            #mainImgTMP = Image.new('RGBA', sizeImg)
            #mainImgTMP.paste(printImgCirc, self.returnCoordForPasteCircleImage(printImgCirc))
            # mainImg.paste(mainImgTMP, (0, 0), circleMaskImg)
            #mainImg.show()
            #mainImg.paste(circleMaskImg, (0,0), circleMaskImg)
            mainImg.save(joinPath(self.pathToDonePlastins, basename(printPath)))
        else:
            printImgRet = printImg.resize(sizeTMP:= self.returnSizePrintForRect(printImg, flag))
            # rectangleMaskImg = rectangleMaskImg.resize(sizeTMP)
            #mainImg.show()
            mainImgTMP = Image.new('RGBA', sizeImg)
            mainImgTMP.paste(printImgRet, self.returnCoordForPasteRectangleImage(printImgRet), printImgRet)
            mainImg.paste(mainImgTMP, (0, 0), mainImgTMP)
            mainImg.paste(rectangleMaskImg, (0, 0), rectangleMaskImg)
            #mainImg.show()
            #mainImg.paste(rectangleMaskImg, (0,0), rectangleMaskImg)
            #mainImg.show()
            #printImgCirc = printImg.resize(self.returnSizePrintForCirc(printImg, flag))
            #mainImgTMP = Image.new('RGBA', sizeImg)
            #mainImgTMP.paste(printImgCirc, self.returnCoordForPasteCircleImage(printImgCirc), printImgCirc)
            # mainImg.paste(mainImgTMP, (0, 0), circleMaskImg)
            #mainImg.show()
            #mainImg.paste(circleMaskImg, (0,0), circleMaskImg)
            mainImg.save(joinPath(self.pathToDonePlastins, basename(printPath)))


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
            xSize = (self.rightPointToRect - self.leftPointToRect) * 0.97
            ySize = printImgRet.size[1] * xSize / printImgRet.size[0]
            if ySize < (self.bottPointToRect - self.topPointToRect):
                return (int(xSize), int(ySize))
            else:
                ySize = (self.bottPointToRect - self.topPointToRect) * 0.97
                xSize = printImgRet.size[0] * (ySize / printImgRet.size[1])
                return (int(xSize), int(ySize))


if __name__ == '__main__':
    a = MakePlastins()
    a.makePlastin(2)