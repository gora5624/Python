import csv
import os
import time
import requests
import xlrd


def file_exists(file_name):
    '''Функция возвращает True если файл по пути file_name существует и False если не существует'''

    return(os.path.exists(file_name))


def write_csv(data, file_name='new_csv {}.csv'.format(time.strftime('%e.%m.%y')), delimiter=';', mode_write='DictWriter'):
    '''Функция записывает контейнер data в файл формата csv. data - контейнер для записи, file_name - относительный или абсолютный путь к файлу в который нужно записать информацию, delimiter - разделители csv, mode_write - режим записи в файл, может быть DictWriter (по умолчанию) либо NoDict. Если режим DictWriter записть производится по ключам в словаре, ключ - название столбца, его значение это значение ячейки. Режим NoDict записывает без ключей и названий столбцов и порядке слева направо.'''

    file_ex = file_exists(file_name)
    # Открывает файл file_name для добавления информации в него. Если его нет, то создает
    with open(file_name, 'a', encoding='utf-8', newline='') as file:
        if mode_write == 'DictWriter':  # Проверяет режим работы функции
            writer = csv.DictWriter(
                file, fieldnames=data.keys(), delimiter=delimiter)
        elif mode_write == 'NoDict':
            writer = csv.writer(file, delimiter=delimiter)
        else:  # Если режим выбран неправильно, выведет информацию об этом в консоль
            print(
                'Error my_mod/we_csv in function write_csv. mode_write can be only DictWriter or NoDict')
        # Проверяет существует ли файл и какой режим. В зависимости от этого записывает шапку в таблицу
        if not file_ex and mode_write == 'DictWriter':
            writer.writeheader()
        writer.writerow(data)


def read_csv(read_file, delimiter=';', mode_read='DictReader'):
    '''Функция считывает информацию из csv файла по пути read_file. delimiter - разделители csv, mode_read - режим чтения файла. DictReader - чтение словарем. Название столбца это ключ, значение ячейки - значение. NoDict - чтение вложенными списками.'''

    with open(read_file, 'r', encoding='utf-8') as file:
        if mode_read == 'DictReader':
            reader = csv.DictReader(file, delimiter=delimiter)
        elif mode_read == 'NoDict':
            reader = csv.reader(file, delimiter=delimiter)
        else:
            print(
                'Error my_mod/we_csv in function read_csv. mode_read can be only DictWriter or NoDict')
        data_file = []
        for line in reader:
            data_file.append(line)
    return(data_file)


def get_html(url, t=0):
    time.sleep(t)
    r = requests.get(url)
    return r.text


def read_xlsx(file_path, title='Yes'):
    '''Считывает построчно xlsx файл и возращает список словарей - если title = 'Yes', список списков - если title = 'No'
    '''
    rd = xlrd.open_workbook(file_path)
    sheet = rd.sheet_by_index(0)
    if title == 'Yes':
        Name_row = sheet.row_values(0)
        start = 1
    elif title == 'No':
        Name_row = None
        start = 0
    data = []
    for rownum in range(start, sheet.nrows):
        row = sheet.row_values(rownum)
        if title == 'Yes':
            dct = {}
            for i, cel in enumerate(row):
                tmp = {Name_row[i]: cel}
                dct.update(tmp)
            data.append(dct)
        elif title == 'No':
            data.append(row)
    return data


def scan_dir(path):
    '''Возращает список файлов в директории и всех её поддерикториях'''

    list_file = []
    list_tmp = os.listdir(path)
    for tmp in list_tmp:
        if os.path.isfile(os.path.join(path, tmp)):
            list_file.append(os.path.join(path, tmp))
        else:
            list_file.extend(scan_dir(os.path.join(path, tmp)))
    return list_file


def generate_bar_WB():
    url = "https://suppliers-api.wildberries.ru/card/getBarcodes"
    headers = {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjgyYTU2OGZlLTgyNTctNGQ2Yi05ZTg1LTJkYTgxMTgxYWI3MSJ9.ROCdF7eOfTZA-atpsLGTAi15yDzHk2UMes05vwjZwn4',
               'Content-Type': 'application/json',
               'accept': 'application/json'}
    data = "{\"id\":1,\"jsonrpc\":\"2.0\",\"params\":{\"quantity\":1,\"supplierID\":\"3fa85f64-5717-4562-b3fc-2c963f66afa6\"}}"
    while True:
        try:
            r = requests.post(url, data=data, headers=headers)
            data_from_wb = r.json()
            break
        except:
            continue
            data_from_wb = r.json()
    return data_from_wb['result']['barcodes'][0]
