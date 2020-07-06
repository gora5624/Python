#!/usr/bin/python3
# -*- coding: utf-8 -*-

def Main():
    while True:
        try:
            WidthList = int(input('Введите ширину листа в миллиметрах: '))
        except ValueError:
            while True:
                WidthList = input(
                    'Введите ширину листа в миллиметрах, целым числом: ')
                try:
                    WidthList = int(WidthList)
                except ValueError:
                    continue
                if type(WidthList) == int:
                    break
        print('Ширина: {}'.format(WidthList))
        try:
            HeightList = int(input('Введите длинну листа в миллиметрах: '))
        except ValueError:
            while True:
                HeightList = input(
                    'Введите длинну листа в миллиметрах, целым числом: ')
                try:
                    HeightList = int(HeightList)
                except ValueError:
                    continue
                if type(HeightList) == int:
                    break

        print('Размер листа для резки {} на {}. Продолжить, введите "да/нет".'.format(WidthList, HeightList))
        ContFlag = input()
        if ContFlag == "да":
            while True:
                try:
                    WidthFilm = int(
                        input('Введите ширину пленки в миллиметрах: '))
                except ValueError:
                    while True:
                        WidthFilm = input(
                            'Введите ширину пленки в миллиметрах, целым числом: ')
                        try:
                            WidthFilm = int(WidthFilm)
                        except ValueError:
                            continue
                        if type(WidthFilm) == int:
                            break

                print('Ширина: {}'.format(WidthFilm))
                try:
                    HeightFilm = int(
                        input('Введите длинну пленки в миллиметрах: '))
                except ValueError:
                    while True:
                        HeightFilm = input(
                            'Введите длинну пленки в миллиметрах, целым числом: ')
                        try:
                            HeightFilm = int(HeightFilm)
                        except ValueError:
                            continue
                        if type(HeightFilm) == int:
                            break

                print(
                    'Размер пленки {} на {}. Продолжить, введите "да/нет".'.format(WidthFilm, HeightFilm))
                ContFlag_2 = input()
                if ContFlag_2 == 'да':
                    break
                elif ContFlag_2 == 'нет':
                    continue
                else:
                    while True:
                        ContFlag_2 = input('Введите "да" или "нет"')
                        if ContFlag_2 == 'да':
                            break_flag = True
                            break
                        elif ContFlag_2 == 'нет':
                            break_flag = False
                            break
                    if break_flag:
                        break
                    else:
                        continue
            a = WidthList // WidthFilm
            b = WidthList // HeightFilm
            c = HeightList // WidthFilm
            d = HeightList // HeightFilm

            print('Максимальное количество пленок из листа: {}'.format(str(
                a*d) + '. Располагать вдоль.' if a*d > b*c else str(b*c) + '. Располагать поперёк.'))
            restart = input(
                'Запишите результат и введите "продолжить или выйти".')
            if restart == 'продолжить':
                continue
            elif restart == 'выйти':
                break
        elif ContFlag == "нет":
            continue
        else:
            print(
                'Неверный ввод. Нужно вводить "да" или "нет". Попробуйте ещё раз после ввода размеров.')


if __name__ == '__main__':
    Main()
