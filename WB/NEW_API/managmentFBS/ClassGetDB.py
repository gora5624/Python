import pandas
import re
import os
import time
import multiprocessing


class getDB():
    def __init__(self) -> None:
        self.pathToDb = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\db'
        self.lableDBFile = r'DB_card \D+.txt'
        self.replaceToDBFileName = ['DB_card ', '.txt']
        self.dbFull = pandas.DataFrame()
    
    def test(self):
        for i in os.listdir(self.pathToDb):
            if re.fullmatch(self.lableDBFile, i):
                print('test')


    def isMatchToDB(self, fileName):
        return True if re.fullmatch(self.lableDBFile, fileName) else False

    @staticmethod
    def saveDB(dbFull, pathToDb):
        dbFull.to_csv(os.path.join(pathToDb, 'DB_full.txt'), sep='\t', index=False)


    def createDB(self):
        for file in os.listdir(self.pathToDb):
            if self.isMatchToDB(file):
                nameIP = file
                for i in self.replaceToDBFileName:
                    nameIP = nameIP.replace(i,'')
                tmpDF = pandas.read_table(os.path.join(self.pathToDb, file), sep='\t')
                tmpDF.insert(0, 'ИП', nameIP)
                self.dbFull = pandas.concat([self.dbFull, tmpDF])
        # p1 = multiprocessing.Process(target=self.saveDB, args=(self.dbFull, self.pathToDb,), daemon=False)
        # p1.start()
        # self.dbFull.to_csv(os.path.join(self.pathToDb, 'DB_full.txt'), sep='\t', index=False)


    def getDB(self):
        if self.dbFull.size == 0:
            self.createDB()
            return self.dbFull
        else:
            return self.dbFull


if __name__ == '__main__':
    test = getDB()
    test.createDB()
    time.sleep(60)