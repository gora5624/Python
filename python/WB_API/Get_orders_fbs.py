import requests
import datetime
import json
import pandas
from my_lib import file_exists

path_to_file = 'D:\end_data.txt'
Url = 'https://suppliers-api.wildberries.ru/api/v2/orders?date_start={}T{}&take=1000&skip=0'


def read_data(path_to_file):
    if not file_exists:
        with open(path_to_file, 'w') as file_data:
            file_data.close()

    with open(path_to_file, 'r') as file_data:
        end_data_file = file_data.read()
        file_data.close()
    if end_data_file == '':
        end_data_file = "2021-08-01T00:00:00+03:00"
    end_data = end_data_file.split('T')[0]
    end_time = end_data_file.split('T')[1].replace(
        ':', '%3A').replace('+', '%2B').replace('.', '%2E')
    return end_data, end_time, end_data_file


def write_data(path_to_file, end_data_file):
    with open(path_to_file, 'w') as file_data:
        file_data.write(end_data_file)
        file_data.close()


def get_orders(Url, end_data, end_time, all_data):
    response = requests.get(Url.format(end_data, end_time), headers={
                            'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjgyYTU2OGZlLTgyNTctNGQ2Yi05ZTg1LTJkYTgxMTgxYWI3MSJ9.ROCdF7eOfTZA-atpsLGTAi15yDzHk2UMes05vwjZwn4'})

    data = response.json()['orders']

    for line in data:
        line.update(wbStickerEncoded=line['sticker']['wbStickerEncoded'])
        line.update(wbStickerSvgBase64=line['sticker']['wbStickerSvgBase64'])

    with open(r'D:\order.json', 'w') as file:
        json.dump(data, file)
        file.close()
    tmp = pandas.read_json(r'D:\order.json')
    all_data = all_data.append(tmp)
    return data, all_data


all_data = pandas.DataFrame()
try:
    tmp = pandas.read_excel(r'D:\Data_order.xlsx')
    all_data = all_data.append(tmp)
    end_data, end_time, end_data_file = read_data(path_to_file)
except:
    print("Предыдущие заказы не обнаружены, делаю с начала.")
    end_data_file = "2021-08-01T00:00:00+03:00"
    end_data = end_data_file.split('T')[0]
    end_time = end_data_file.split('T')[1].replace(
        ':', '%3A').replace('+', '%2B').replace('.', '%2E')

data, all_data = get_orders(Url, end_data, end_time, all_data)
while len(data) > 1:
    data, all_data = get_orders(Url, end_data, end_time, all_data)
    end_data = data[-1]['dateCreated'].split('T')[0]
    end_time = data[-1]['dateCreated'].split('T')[1].replace(
        ':', '%3A').replace('+', '%2B').replace('.', '%2E')

all_data.to_excel(r'D:\Data_order.xlsx', index=False)
all_data.to_excel(
    r'\\192.168.0.33\shared\_Общие документы_\Заказы вайлд\Архив\Data_order.xlsx', index=False)
write_data(path_to_file, end_data_file)
