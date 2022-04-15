from CardBodyClass import CardCase, Nomenclature
import sys
from os.path import join as joinPath
sys.path.insert(1, joinPath(sys.path[0], '../..'))
from my_mod.my_lib import read_xlsx
import requests
import json
import uuid


main_path = r'C:\Users\Public\Documents\WBUploadImage'
Token_path = joinPath(main_path, r'Token.txt')
Token_path = joinPath(main_path, r'TokenAbr.txt')
mainUrl = 'https://suppliers-api.wildberries.ru/card/batchCreate'
path = r'\\192.168.0.33\shared\_Общие документы_\Егор\WB\создание Чехлы для телефонов от 09.02.22.xlsx'
data = read_xlsx(path)
tmpListNom = {}
tmpListCard = {}
for line in data:
    nomenclature = Nomenclature(line['Артикул цвета'], line['Штрихкод товара'], line['Розничная цена'], photoURLs=['123','321'])
    if line['Артикул поставщика'] in tmpListCard.keys():
        tmpListCard[line['Артикул поставщика']].AddNomenklatures(nomenclature.GetStruct())
    else:
        id = uuid.uuid4
        card = CardCase(id)
        card.SetAddin(line)
        card.SetStruct()
        nomenclature.SetUUID(id)
        card.AddNomenklatures(nomenclature.GetStruct())
        tmpListCard.update({line['Артикул поставщика']:card})

with open(Token_path, 'r', encoding='UTF-8') as file:
        Token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjQ3YjBiYmJkLWQ2NWMtNDNhMi04NDZjLWU1ZDliMDVjZDE4NiJ9.jcFv0PeJTKMzovcugC5i0lmu3vKBYMqoKHi_1jPGqjM'
        file.close()
for item in tmpListCard.values():
    datajson = item.GetStruct()
    with open(r'E:\json2.json', 'w', encoding='utf-8') as file:
        json.dump(datajson, file, sort_keys=True, indent=2,ensure_ascii=False)
    response = requests.post(url=mainUrl, headers={
                'Authorization': '{}'.format(Token)}, json=datajson)
    response