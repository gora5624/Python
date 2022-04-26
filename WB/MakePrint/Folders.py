from os.path import abspath, join as joinPath

diskWithPrint = 'F'
pathToPrintAll = r'{}:\Картинки китай\Под натяжку общее\Все'.format(diskWithPrint)
pathToPrintWithOutBack = r'{}:\Картинки китай\Под натяжку общее\Без фона'.format(diskWithPrint)
pathToDonePic = r'{}:\Готовые принты книжки Fashion'.format(diskWithPrint)
pathToEffect = abspath(joinPath(__file__, '..',r'Effect\light.png'))
pathToMasks = abspath(joinPath(__file__, '..',r'BookPic\BookMask'))
pathToBacks = abspath(joinPath(__file__, '..',r'BookPic\BookBack'))
diskWithPrint = 'F'
pathToSiliconMaskFolder = r'{}:\Маски силикон'.format(diskWithPrint)
pathToCategoryList = joinPath(pathToSiliconMaskFolder,'cat.xlsx')
pathToPrintAll = r'{}:\Картинки китай\Принты со светом\Все'.format(diskWithPrint)
pathToPrintWithOutBack = r'{}:\Картинки китай\Принты со светом\Без фона'.format(diskWithPrint)
pathToSecondImagesFolder = r'{}:\Для загрузки\Вторые картинки\Силикон'.format(diskWithPrint)
pathToDoneSiliconImage = r'{}:\Для загрузки\Готовые принты\Силикон'.format(diskWithPrint)
pathToDoneImageWithName = r'{}:\Готовые картинки Fashion по моделям'.format(diskWithPrint)
fontPath = abspath(joinPath(__file__, '..','Fonts','CarosSoftBold.ttf'))
pathToImage = r'{}:\Готовые принты книжки Fashion'.format(diskWithPrint)