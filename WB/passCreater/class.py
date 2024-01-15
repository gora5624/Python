import requests
import os
import pandas as pd
import time
import datetime
import telebot


class myExc(Exception):
    pass


class PassCreater():
    def __init__(self) -> None:
        self.urlCreatePass = 'https://suppliers-api.wildberries.ru/api/v3/passes'
        self.urlDeletPass = 'https://suppliers-api.wildberries.ru/api/v3/passes/{passId}'
        self.urlGetPass = 'https://suppliers-api.wildberries.ru/api/v3/passes'
        self.pathToPassList = os.path.join(os.path.dirname(__file__), r'Пропуска.xlsx')
        self.headers = {
            'Authorization': open(os.path.join(os.path.dirname(__file__), r'token'), 'r').read()
        }
        self.maxTry = 5
        self.countTry = 0
        self.deletList = []
        self.donePass = []
        self.date = datetime.datetime.strftime(datetime.datetime.now(), '%d.%m.%y')
        self.listErrorsPass = []
        self.finalMessSucs = 'Пропуски от {} созданы успешно'.format(self.date)
        self.finalMessError = 'ОШИБКА ПОРПУСКОВ от {} {} НЕ СОЗДАНЫ'.format(self.date, ','.join(self.listErrorsPass))
        self.botToken = open(os.path.join(os.path.dirname(__file__), 'tokenBot'), 'r', encoding='utf-8').read()
        self.bot = telebot.TeleBot(self.botToken)
        self.bot.config['api_key']=self.botToken # = telebot.TeleBot(self.botToken).config['api_key']=self.botToken

    def createPass(self):
        listPassForCreate = pd.read_excel(self.pathToPassList)
        for row in listPassForCreate.itertuples():
            try:
                self.createOnePass(row)
                self.log('УСПЕШНО createOnePass' + ' создан' + row.Номер)
            except myExc:
                print('Не удалось создать пропуск {}'.format(row.Номер))
                self.listErrorsPass.append(row.Номер)
                continue

        if len(self.donePass) == listPassForCreate.shape[0]:
            self.log('УСПЕШНО createPass' + 'созданы все пропуски')
            print('Успешно созданы все пропуски')


    def createOnePass(self, row):
        self.countTry = 0
        json = {
                "firstName": "Юрий",
                "lastName": "Баканов",
                "carModel": row.Марка,
                "carNumber": row.Номер,
                "officeId": 106
                }
        while self.countTry < self.maxTry:
            r = requests.post(url=self.urlCreatePass, headers=self.headers,json=json,timeout=50)
            if r.status_code == 201:
                print('Создан {}'.format(row.Номер))
                self.donePass.append(row.Номер)
                time.sleep(61*10)
                return 0
            elif r.status_code == 429:
                time.sleep(60*10)
                continue
            else:
                self.countTry+=1
                self.log('НЕ УСПЕШНО createOnePass' + 'создание' + row.Номер)
                time.sleep(5)
                continue
        raise myExc
            

    def deletPass(self):
        try:
            listAlsoCreatedPass = self.getAlsoCreatedPassList()
        except myExc:
            print('Не удалось получить список пропусков, удаление невозможно!')
            raise myExc
        self.countTry = 0
        for line in listAlsoCreatedPass:
            while self.countTry < self.maxTry:
                r = requests.delete(url=self.urlDeletPass.format(passId = line['id']), headers=self.headers,timeout=50)
                if r.status_code == 204:
                    print(line['carNumber'] + ' Успешно удалён!')
                    self.log('УСПЕШНО deletPass' + line['carNumber'] + ' Успешно удалён!')
                    self.deletList.append(line)
                    time.sleep(5)
                    break
                else:
                    time.sleep(5)
                    try:
                        self.log('НЕ УСПЕШНО deletPass {}, {}'.format(r.status_code, r.text) + line['carNumber'] + ' Успешно удалён!')
                    except:
                        self.log('НЕ УСПЕШНО deletPass неизвестен ответ' + line['carNumber'] + ' Успешно удалён!')
                    self.countTry +=1
                    continue
        if len(self.deletList) == len(listAlsoCreatedPass):
            print('Все пропуски успешно удалены')
        else:
            print('НЕ все пропуски были удалены успешно, осталось {}'.format(str(len(listAlsoCreatedPass) - len(self.deletList))))


    def getAlsoCreatedPassList(self):
        while self.countTry < self.maxTry:
            r = requests.get(url=self.urlGetPass, headers=self.headers,timeout=50)
            if r.status_code == 200:
                self.log('УСПЕШНО getAlsoCreatedPassList' + ' список получен')
                return r.json()
            else:
                self.countTry +=1
                time.sleep(5)
                continue
        raise myExc

    def log(self, mess):
        with open(os.path.join(os.path.dirname(__file__), r'log'), 'a', encoding='utf-8') as logFile:
            logFile.write(mess + ' ' + datetime.datetime.now().strftime('%d.%m.%y, %H:%M:%S') + '\n')
            logFile.close()
 
if __name__ == '__main__':
    a = PassCreater()
    try:
        a.deletPass()
    except:
        pass
    try:
        a.createPass()
        a.bot.send_message(-1001550015840, r'ПРОПУСКИ СОЗДАЛИСЬ')
    except:
        a.bot.send_message(-1001550015840, r'ОШИБКА ПРОПУСКОВ')