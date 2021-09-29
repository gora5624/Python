import requests
from os.path import join as joinpath

main_path = r'C:\Users\Public\Documents\WBGetOrder'
Token_path = joinpath(main_path, r'Token.txt')
status = 0


def getToken():
    """Получаем токен для авторизации"""
    with open(Token_path, 'r', encoding='UTF-8') as file:
        Token = file.read()
        file.close()
    return Token


def changeStatus(orderId, Token):
    """Изменяет статус заказа на заданный, в данном случае "1" - на сборке"""
    Url = 'https://suppliers-api.wildberries.ru/api/v2/orders'
    datajson = [{"orderId": orderId,
                 "status": status}]
    while True:
        try:
            response = requests.put(Url, headers={
                'Authorization': '{}'.format(Token)}, json=datajson)
            print(response.text)
            if response.status_code != 200:
                continue
            elif response.status_code == 200:
                break
        except:
            continue
    print(response)


Token = getToken()
changeStatus('89253869', Token)
