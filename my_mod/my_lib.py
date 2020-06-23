import csv
import os
import time
import requests


def file_exists(file_name):
    '''Функция возвращает True если файл по пути file_name существует и False если не существует'''

    return(os.path.exists(file_name))


def write_csv(data, file_name='new_csv {}.csv'.format(time.strftime('%e.%m.%y, %H.%M.%S')), delimiter=';', mode_write='DictWriter'):
    '''Функция записывает контейнер data в файл формата csv. data - контейнер для записи, file_name - относительный или абсалютный путь к файлу в который нужно записать информацию, delimiter - разделители csv, mode_write - режим записи в файл, может быть DictWriter (по умолчанию) либо NoDict. Если режим DictWriter записть производится по ключам в словаре, ключ - название столбца, его значение это значение ячейки. Режим NoDict записывает без ключей и названий столбцов и порядке слева направо.'''

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


def get_html(url):
    time.sleep(5)
    r = requests.get(url)
    return r.text
