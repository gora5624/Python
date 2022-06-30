class FilterNomenclatures():
    def __init__(self, brandFilter, modelFilter, colorFilter, cameraFilter, categoryFilter, dataBase) -> None:
        self.brandFilter = brandFilter
        self.modelFilter = modelFilter
        self.colorFilter = colorFilter
        self.cameraFilter = cameraFilter
        self.categoryFilter = categoryFilter
        self.dataBase = dataBase
        self.barcodList = ''
        self.nmIdList = ''


    def getBarcodsList(self):
        if self.brandFilter != 'Все':
            self.dataBase = self.dataBase[self.dataBase.brand == self.brandFilter]
        if self.modelFilter != 'Все':
            self.dataBase = self.dataBase[self.dataBase.model == self.modelFilter]
        if self.colorFilter != 'Все':
            self.dataBase = self.dataBase[self.dataBase.color == self.colorFilter]
        if self.cameraFilter != 'Все':
            self.dataBase = self.dataBase[self.dataBase.cameraType == self.cameraFilter]
        if self.categoryFilter != 'Все':
            self.dataBase = self.dataBase[self.dataBase.category == self.categoryFilter]
        self.barcodList = self.dataBase.barcod.unique().tolist()
        self.barcodList

    def getnmIdList(self):
        if self.brandFilter != 'Все':
            self.dataBase = self.dataBase[self.dataBase.brand == self.brandFilter]
        if self.modelFilter != 'Все':
            self.dataBase = self.dataBase[self.dataBase.model == self.modelFilter]
        if self.colorFilter != 'Все':
            self.dataBase = self.dataBase[self.dataBase.color == self.colorFilter]
        if self.cameraFilter != 'Все':
            self.dataBase = self.dataBase[self.dataBase.cameraType == self.cameraFilter]
        if self.categoryFilter != 'Все':
            self.dataBase = self.dataBase[self.dataBase.category == self.categoryFilter]
        self.nmIdList = self.dataBase.nmId.unique().tolist()
        self.nmIdList