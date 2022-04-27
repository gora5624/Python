from os.path import abspath, join as joinPath

workDisk = 'F'
# пути общие
pathToPrintImageFolderAll = r'{}:\Картинки китай\Под натяжку общее\Все'.format(workDisk)
pathToPrintImageFolderWithOutBack = r'{}:\Картинки китай\Под натяжку общее\Без фона'.format(workDisk)
pathToCategoryList = abspath(joinPath(__file__, '..','cat.xlsx'))
pathToUploadWeb = r'http://80.237.77.44/joomla/images/mobi/Готовые принты'
pathToUploadFolderLocal = r'\\192.168.0.33\web_packages\joomla\images\mobi\Готовые принты'
pathToUploadSecondWeb = r'http://80.237.77.44/joomla/images/mobi/Вторые картинки'
pathToSecondImageUploadFolder = r'\\192.168.0.33\web_packages\joomla\images\mobi\Вторые картинки'
# пути для книжек
pathToBookImageWithOutModel = r'{}:\Готовые принты книжки Fashion'.format(workDisk)
pathToBookEffect = abspath(joinPath(__file__, '..', r'MakeBookImage',r'Effect',r'light.png'))
pathToBookMasks = abspath(joinPath(__file__, '..',r'MakeBookImage',r'BookPic',r'BookMask'))
pathToBookBacks = abspath(joinPath(__file__, '..', r'MakeBookImage',r'BookPic',r'BookBack'))
pathToDoneBookImageWithName = r'{}:\Для загрузки\Готовые принты\Fashion'.format(workDisk)
fontPath = abspath(joinPath(__file__, '..', r'MakeBookImage',r'Fonts',r'CarosSoftBold.ttf'))
pathToSecondImagesBook = r'{}:\Для загрузки\Вторые картинки\Fashoin'.format(workDisk)
# пути для силикона
pathToMaskFolderSilicon = r'{}:\Маски силикон'.format(workDisk)
pathToSecondImagesFolderSilicon = r'{}:\Для загрузки\Вторые картинки\Силикон'.format(workDisk)
pathToDoneSiliconImageSilicon = r'{}:\Для загрузки\Готовые принты\Силикон'.format(workDisk)

