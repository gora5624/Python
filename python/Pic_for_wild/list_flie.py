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


path = r'D:\tmp\my_prod\Python\all_pic'
list_pic = scan_dir(path)

with open(r'D:\tmp\my_prod\Python\python\Pic_for_wild\list_pic', 'r') as file:
    list_my_pic = file.readlines()

for tmp in list_my_pic:
    for tmp_2 in list_pic:
        if tmp.strip() + '.jpg' in tmp_2:
            print(tmp.strip())
            os.replace(tmp_2, os.path.join(
                r'D:\tmp\my_prod\Python\python\Pic_for_wild', tmp.strip()+'.jpg'))
