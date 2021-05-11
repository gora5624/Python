import os

'''возвращает список файлов в папке и подпапках'''


def scan_dir(path):
    list_file = []
    list_tmp = os.listdir(path)
    for tmp in list_tmp:
        if os.path.isfile(os.path.join(path, tmp)):
            list_file.append(os.path.join(path, tmp))
        else:
            list_file.extend(scan_dir(os.path.join(path, tmp)))
    return list_file


path = r'D:\tmp\filmMaket\src\done'
for x in (scan_dir(path)):
    print(x)
