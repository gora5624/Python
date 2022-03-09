import os
import sys

from xlrd import count_records
from my_lib import read_xlsx

mainPath = r'C:\Users\Public\Documents\PrintHelp'
file_order_pass = os.path.join(mainPath, 'ФБС Печать 07.07.21.xlsx')
confin_path = os.path.join(mainPath, 'config_printing.ini')
file_with_models_path = os.path.join(
    r'\\192.168.0.33\shared\_Общие документы_\Женя\выставить', 'список печати.xlsx')

size_pr = ['XL', 'L', 'M', 'MS', 'S', 'XS']


def mainPathExist(mainPath):
    '''Проверяем есть ли служебная папка для программы и, если нет, - создаём.'''
    if os.path.exists(mainPath):
        return
    else:
        os.mkdir(mainPath)


def chek(mainPath):
    '''Первоначальные настройки и проверки чтобы было меньше проблем и более ясная картина при работе.'''
    mainPathExist(mainPath)  # Главная директория где происходит весь движ


def get_data_from_order(file_order_pass):
    '''Парсим эксель под печать. Ожидаем эксель без заголовков, порядок столбцов:
    [0]-название номенклатуры в 1С
    [2]-код номенклатуры в 1С
    [3]-ШК номенклатуры в 1С
    [4]-количество в печать
    [1]-код чехла, на котором печатаем
    Попутно удаляем пустые строки и сливаем посторяющиеся строки
    '''
    # прочиали файл
    data_for_printing = read_xlsx(file_order_pass, title='No')
    # составляем списки всех значений по "столбцам" для последующей проверки на уникальность
    unic_test_list = {'Name': [],
                      'Cod_1C': [],
                      'Barcode': [],
                      'Count': [],
                      'Cod_1C_main': []}
    # зоводим новый список, куда будем складывать интерисующие нас значения, без всего лишнего
    data_for_printing_new = []
    for data in data_for_printing:
        # Преобразуем floatы в str и убираем лишние 0 на конце
        for n, j in enumerate(data):
            if type(j) == float:
                data[n] = str(j).replace('.0', '')
        # Если строка НЕ пустая, добавляем значения в наш новый список и в список на проверк ууникальности
        if ''.join(data):
            # составляем списки на проверку уникальности
            unic_test_list['Name'].append(data[0])
            unic_test_list['Cod_1C'].append(data[1])
            unic_test_list['Barcode'].append(data[2])
            unic_test_list['Count'].append(data[3])
            unic_test_list['Cod_1C_main'].append(data[4])
    # проверяем список на уникальность и при необходимости складываем значения в одно
    stop_list = []
    for data in unic_test_list['Barcode']:
        n = unic_test_list['Barcode'].index(data)
        if unic_test_list['Barcode'].count(data) == 1:
            data_for_printing_new.append([unic_test_list['Name'][n],
                                          unic_test_list['Cod_1C'][n],
                                          unic_test_list['Barcode'][n],
                                          unic_test_list['Count'][n],
                                          unic_test_list['Cod_1C_main'][n]])
        elif unic_test_list['Barcode'].count(data) > 1 and unic_test_list['Barcode'][n] not in stop_list:
            count = unic_test_list['Barcode'].count(data)
            st = 0
            count_new = 0
            for num in range(count):
                st = unic_test_list['Barcode'].index(data, st)
                count_new = count_new + int(unic_test_list['Count'][st])
            data_for_printing_new.append([unic_test_list['Name'][n],
                                          unic_test_list['Cod_1C'][n],
                                          unic_test_list['Barcode'][n],
                                          count_new,
                                          unic_test_list['Cod_1C_main'][n]])
            stop_list.append(unic_test_list['Barcode'][n])
            num = num+1
    unic_test_list
    return data_for_printing_new


def get_data_about_models(file_with_models_path):

    data_about_model = read_xlsx(file_with_models_path)
    return data_about_model


def create_config_file(confin_path, file_with_models_path):
    '''создаём текстовый файл ini с описанием какие модели мы режем, откуда берём под них макеты,
    какого размера должен быть под них стол и сколько их умещается в столе. Одна строка - одна модель. Разделитель внутри строки 'dlmt_str', разделитель строк 'end_str'
    '''
    # Парсим эксель с описанием где и какие макеты под какую модель лежат. Ожидаем эксель с заголовками столбцов:
    # [0]-Название модели в 1С
    # [1]-Типоразмер
    # [2]-Печать отдельно
    try:
        data_about_models = read_xlsx(file_with_models_path)
        dlmt_str = ';'  # Разделитель между свойствами
        end_str = '\n'  # Разделитель между сроками

        with open(confin_path, 'w') as config_file:  # Создаём файл по пути confin_path
            for data in data_about_models:
                list_tmp = [data['Название модели в 1С'],
                            data['Типоразмер'].lower(),
                            data['Печать отдельно'].lower()]
                # Записываем в него всю информацию
                config_file.writelines(dlmt_str.join(list_tmp)+end_str)
            config_file.close()
            return 0
    except:
        return 1


def create_printing_file(file_order_pass, size_pr):
    data_from_printing = read_xlsx(file_order_pass, 'No')
    data_for_printing = []
    data_about_models = read_xlsx(file_with_models_path)
    for i in data_from_printing:
        data_for_printing.append(i[0].replace('\xa0', ' '))
    for size in size_pr:
        for prints in data_for_printing:
            prints


def main(file_order_pass, confin_path, file_with_models_path, mainPath):

    chek(mainPath)
    # распарсили эксель с заказом, получили список списков
    data_for_printing = get_data_from_order(file_order_pass)

    # создаём файл конфига с описанием какие макеты под какие модели и на каких столах печатать для Corel

   # if create_config_file(confin_path, file_with_models_path) != 0:
    # input(
    # 'Не удалось создать файл конфигурации резки. Нажмите Enter для выхода.')

    create_printing_file(file_order_pass)

    return 0


a = (file_order_pass, confin_path, file_with_models_path, mainPath)

main(*a)
