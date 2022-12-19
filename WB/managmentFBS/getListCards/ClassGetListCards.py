import pandas


class getListCards():
    def __init__(self, filter, DB, typeFilter, flterMain) -> None:
        self.DB = DB
        self.filter = filter
        self.typeFilter = typeFilter
        self.flterMain = flterMain

    
    def getListCards(self):
        if self.flterMain == 'И':
            dataForSave = self.DB
            for line in self.filter:
                dataForSave = dataForSave[dataForSave[line[0]] == line[1]]
            return dataForSave
        elif self.flterMain =='ИЛИ':
            dataForSave = pandas.DataFrame()
            for line in self.filter:
                dataForSave = pandas.concat([self.DB[self.DB[line[0]] == line[1]],dataForSave])
            return dataForSave
            dataForSave = DB