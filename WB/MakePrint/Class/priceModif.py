import requests


class priceMod:
    def __init__(self, nmIdList, token, price, discount):
        self.urlPushPrice = 'https://suppliers-api.wildberries.ru/public/api/v1/prices'
        self.urlPushDiscount = 'https://suppliers-api.wildberries.ru/public/api/v1/updateDiscounts'
        self.nmIdList = nmIdList
        self.headers = {'Authorization': token}
        self.discount = discount
        self.price = price


    def pushPrice(self):
        jsonPrice = []
        for nmId in self.nmIdList:
            json = {
                        "nmId": nmId,
                        "price": self.price
                    }
            jsonPrice.append(json)
        r = requests.post(url=self.urlPushPrice, json=jsonPrice, headers=self.headers)
        if r.status_code == 200:
            print('Цены установлены успешно')
        elif ':No goods for process' in r.text:
            print('Цены уже установлены')
        else:
            print('Ошибка установки цен')


    def pushDiscounts(self):
        jsonDiscounts = []
        for nmId in self.nmIdList:
            json = {
                        "nm": nmId,
                        "discount": self.discount
                    }
            jsonDiscounts.append(json)
        r = requests.post(url=self.urlPushDiscount, json=jsonDiscounts, headers=self.headers)
        if r.status_code == 200:
            print('Скидки установлены успешно')
        elif 'No goods for process' in r.text:
            print('Скидки уже установлены')
        else:
            print('Ошибка установки скидок')