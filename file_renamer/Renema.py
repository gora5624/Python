import os
import json

''' Скрипт заменяет русские буквы латинскими согласно таблице транслитерации LatChar.txt
в названиях каталогов и файлов начиная с "dir_in" '''

dir_in = r'D:\Фото без логотипа публичная'  # Задаём точку входа

# Меняем директорию с репозитория на директорию скрипта
os.chdir(r'file_renamer')


def main(dir_in):
    '''Рекурсивно сканирует каталоги начиная с dir_in и переименовывает их путём замены
    русских символов литинскими, по словарю char_list, который хранится одельным файлом.'''
    list_dir = os.listdir(dir_in)
    with open('char_list', 'r', encoding='utf-8') as file:
        char_dict = json.loads(str(file.read()))
        file.close()
    for dir_ in list_dir:
        if os.path.isdir(os.path.join(dir_in, dir_)):
            dir_rename = ''
            for char in dir_:
                try:
                    char_new = char_dict[char]
                    dir_rename += char_new
                except:
                    dir_rename += char
            os.rename(os.path.join(dir_in, dir_),
                      os.path.join(dir_in, dir_rename))
            main(os.path.join(dir_in, dir_rename))


main(dir_in)
