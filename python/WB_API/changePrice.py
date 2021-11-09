
from os.path import join as joinpath
import requests
from my_lib import read_xlsx


main_path = r'C:\Users\Public\Documents\WBChangePrice'
nameListStuff = r'PriceList.xlsx'
pathToListStuff = joinpath(main_path, nameListStuff)
Token_path = joinpath(main_path, r'Token.txt')


def changePriceMain(priceList):
    with open(Token_path, 'r', encoding='UTF-8') as file:
        Token = file.read()
        file.close()
        changePrice = 'https://suppliers-api.wildberries.ru/public/api/v1/prices'

        while True:
            response = requests.post(changePrice, headers={
                'Authorization': '{}'.format(Token)}, json=priceList)
            if response.status_code == 200:
                print(response.text)
                break
            if 'no free connections available to host' in response.text:
                continue


def changePrice(pathToListStuff):
    priceList = []
    for line in read_xlsx(pathToListStuff):
        json = []
        if len(priceList) < 1000:
            json = {
                "nmId": int(line['Артикул WB']),
                "price": int(line['Цена'])
            }

            priceList.append(json)
        else:
            changePriceMain(priceList)
            priceList = []

    changePriceMain(priceList)


if __name__ == '__main__':
    changePrice(pathToListStuff)
