from os.path import abspath, join as joinPath

diskWithPrint = 'F'
diskForDone = 'F'
pathToPrintAll = r'{}:\Картинки китай\Под натяжку общее\Все'.format(diskForDone)
pathToPrintWithOutBack = r'{}:\Картинки китай\Под натяжку общее\Без фона'.format(diskForDone)
pathToDonePic = r'{}:\Готовые принты книжки Fashion'.format(diskForDone)
pathToEffect = abspath(joinPath(__file__, '..',r'Effect\light.png'))
pathToMasks = abspath(joinPath(__file__, '..',r'BookPic\BookMask'))
pathToBacks = abspath(joinPath(__file__, '..',r'BookPic\BookBack'))