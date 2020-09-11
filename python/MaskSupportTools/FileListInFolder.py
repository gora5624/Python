import os
from my_lib import write_csv


def main():
    path = os.path.abspath(input('Введите путь к папке: '))
    if path == '':
        path = os.curdir
    FileName = input('Введите путь и название файла с результатами: ')
    if FileName == '':
        FileName = 'ListFile.csv'
    data = []
    data = (os.listdir(path))
    for line in data:
        Data = {'Имя файла': line}
        write_csv(Data, FileName)


if __name__ == "__main__":
    main()
