import os
from my_lib import read_csv, file_exists


def main(path):
    ListMask = read_csv(
        'python\\MaskSupportTools\\NameModels.csv')
    for Mask in ListMask:
        FullPath = os.path.join(path.format('done'), Mask['Имя файла']+'.png')
        if file_exists(FullPath) and not (file_exists(os.path.join(path.format('mask'), Mask['Новое имя']+'.png'))):
            os.rename(FullPath, os.path.join(
                path.format('mask'), Mask['Новое имя']+'.png'))


path = r'D:\\tmp\\make_mask\\{}'


if __name__ == "__main__":
    main(path)
