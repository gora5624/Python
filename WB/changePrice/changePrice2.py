import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor
import time

# Определение структуры priceDict
priority_priceDict = {
    'NewPoket': (981, 49),
    'под карту': (981, 49),
    'усил.угл. проз.': (981, 49),
    ' проз.': (510, 41),
    ' мат.': (510, 41),
    'AirTag': (510, 41),
    'Пластина магнитного держателя': (510, 41),
    'черный противоуд. SkinShell': (981, 49),
    'Картхолдер': (981, 49),
    'Fashion': (999, 43)
}

# Список файлов и токенов для каждого продавца
data_files_tokens = [
    (r"F:\data_Караханян.txt", 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njg4MiwiaWQiOiI4YjEzZWUzOC03MGIxLTQ3ZjgtYTdlNC03OTIzY2Q2ZmQ3ZTciLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjEwMTA2MiwicyI6MTAsInNpZCI6IjNhOTNkZGMxLWFhNTctNWMyYi05YzVjLWRkZDIyMTg4OTQ0MCIsInVpZCI6NDUzMjI5MjB9.DXm6RuooUieyrnNdXr3FfPPdwK5uV4aiTF5SZIryJUhbQW4uScXQLEb-n8p0iM3RT6Js6aVKijiyOkawE6r76g'),
    (r"F:\data_Манвел.txt", 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njk1MSwiaWQiOiIyMzUyZGFmYS05NTdhLTQ0MzAtYWFhMi1lZGM5NDZkZDY0ODEiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjUyNzczNiwicyI6MTAsInNpZCI6ImFhNDdlNDg5LTU5ZTAtNDIzMi1hMWJmLTBlMTIzOWYwNDJmMSIsInVpZCI6NDUzMjI5MjB9.j9s_VtDpTEWceEd1vUTWf6uofUuSY30q0UrR-H047qZE40sb8atwtAviABB7eoeLQdu3T69UosBdn_Bvj2-2ZQ'),
    (r"F:\data_Самвел.txt", 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5Njk3MiwiaWQiOiJjZWE4ZTNmYy1iYzg5LTRjYjktYmNmNy0xN2ZiNmNjNzk1MTQiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjgxOTI0NiwicyI6MTAsInNpZCI6IjBhYjhiMTA1LTA1MWYtNGVkNi04NzBiLTM5OWU3NWUxMDI4NiIsInVpZCI6NDUzMjI5MjB9.bOmPtl_ZXx-1C25-5CbftPJVQuuHzwG5iH9QUx0x8CdZCjI9ZnbFgMU1ijL-lfgn_N1JxPvojV2dBrKTpDnolw'),
    (r"F:\data_Федоров.txt", 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzA5NzAwNywiaWQiOiI1ZWRjMWY0Ni04OWVhLTQxMzktYjVjYi1hNDM5OGUwMzUxNTMiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjExNzEwNDQsInMiOjEwLCJzaWQiOiJkOWU0OGUxZi05ZjgxLTQ1MmMtODRiYy05ZGYxZWRiMzNmNDkiLCJ1aWQiOjQ1MzIyOTIwfQ.y2sbT8zqvoM-iSxKJcsdiEphMoLRfNq8pBsIQnmGQIbc1btCIoe7Qkz65Ur91fVEqyDbQZ-Ry_1tTkgof5hKDw')
]

# URL для отправки данных
urlPushPrice = 'https://discounts-prices-api.wb.ru/api/v2/upload/task'

# Функция для обработки отдельного файла
def process_file(file_name, token, shk_df, priceDict):
    # Чтение файла data_
    data_df = pd.read_csv(file_name)
    data_df['skus'] = data_df['skus'].apply(eval)
    data_df = data_df.explode('skus')  # Разворачиваем список skus в отдельные строки
    data_df['skus'] = data_df['skus'].astype(str).str.strip()
    shk_df['Штрихкод'] = shk_df['Штрихкод'].astype(str).str.strip()
    # Объединение данных по SKU
    merged_df = pd.merge(data_df[['nmID', 'skus']], shk_df, left_on='skus', right_on='Штрихкод')
    
    # Создание списка dataForUpload
    dataForUpload = []
    for _, row in merged_df.iterrows():
        nmId = row['nmID']
        nomenclature = row['Номенклатура']
        # Проверка ключей по приоритету
        for key in priority_priceDict:
            if key in nomenclature:
                p, d = priority_priceDict[key]
                dataForUpload.append({
                    "nmId": nmId,
                    "price": p,
                    "discount": d
                })
                break  # После нахождения первого соответствующего ключа выходим из цикла
    
    pushPrice(dataForUpload, token)

# Функция для отправки данных на сервер
def pushPrice(dataForUpload, token):
    headers = {'Authorization': token}
    jsonPrice = [{"nmId": line['nmId'], "price": line['price'], "discount": line['discount']} for line in dataForUpload]
    countTry = 0

    for i in range(0, len(jsonPrice), 1000):
        while countTry < 5:
            r = requests.post(url=urlPushPrice, json={'data': jsonPrice[i:i+1000]}, headers=headers)
            if r.status_code == 200:
                print('Цены установлены успешно')
                time.sleep(0.7)
                break
            elif 'No goods for process' in r.text:
                time.sleep(0.7)
                # print('Цены уже установлены')
                break
            else:
                countTry += 1
                time.sleep(5)
                print('Ошибка установки цен')
                continue

if __name__ == "__main__":
    shk_df = pd.read_csv(r"\\192.168.0.33\shared\_Общие документы_\Егор\ШК\ШК.txt", delimiter='\t')

    # Создание пула потоков для одновременной обработки файлов
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_file, file_name, token, shk_df, priority_priceDict) for file_name, token in data_files_tokens]

    # Ожидание завершения всех потоков
    for future in futures:
        future.result()