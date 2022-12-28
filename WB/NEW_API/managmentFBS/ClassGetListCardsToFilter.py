import pandas


class getListCardsToFilter():
    def __init__(self) -> None:
        pass
    # def __init__(self, filter, DB, typeFilter, flterMain) -> None:
        # self.DB = DB
        # self.filter = filter
        # self.typeFilter = typeFilter
        # self.flterMain = flterMain

    
    # def getListCards(self):
    #     if self.flterMain == 'И':
    #         dataForSave = self.DB
    #         for line in self.filter:
    #             dataForSave = dataForSave[dataForSave[line[0]] == line[1]]
    #         return dataForSave
    #     elif self.flterMain =='ИЛИ':
    #         dataForSave = pandas.DataFrame()
    #         for line in self.filter:
    #             dataForSave = pandas.concat([self.DB[self.DB[line[0]] == line[1]],dataForSave])
    #         return dataForSave

    @staticmethod
    def getListCards(filter, DB, flterMain):
        # if flterMain == 'И':
            dataForSave = DB if flterMain == 'И' else pandas.DataFrame()
            for line in filter:
                if line[2] == 'Равно':
                    dataForSave = dataForSave[dataForSave[line[0]].astype('string') == line[1]] if flterMain == 'И' else pandas.concat([DB[DB[line[0]].astype('string') == line[1]],dataForSave])
                elif line[2] == 'Не равно':
                    dataForSave = dataForSave[dataForSave[line[0]].astype('string') != line[1]] if flterMain == 'И' else pandas.concat([DB[DB[line[0]].astype('string') != line[1]],dataForSave])
                elif line[2] == 'Содержит':
                    dataForSave = dataForSave[dataForSave[line[0]].astype('string').str.contains(line[1])] if flterMain == 'И' else pandas.concat([DB[DB[line[0]].astype('string').str.contains(line[1])],dataForSave]) 
                elif line[2] == 'Не содержит':
                    dataForSave = dataForSave[~dataForSave[line[0]].astype('string').str.contains(line[1])] if flterMain == 'И' else pandas.concat([DB[~DB[line[0]].astype('string').str.contains(line[1])],dataForSave]) 
            return dataForSave