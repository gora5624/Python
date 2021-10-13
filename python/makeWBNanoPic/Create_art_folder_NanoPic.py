import os
from shutil import copyfile
from my_lib import read_xlsx, file_exists
import zipfile


path_list_stuff = r'C:\Users\Public\Documents\WBGetOrder\TMPDir\Список номенклатуры — копия.XLSX'
Count_Arh = 200


def main(path_list_stuff):
    for line in read_xlsx(path_list_stuff):
        for file in os.listdir(r'D:\NanoBook'):
            if line['Баркод'] == file[0:-4]:
                dest_folder = os.path.join(
                    'D:\Done', str(line['Артикул WB'])[0:-2] if type(line['Артикул WB']) == float else line['Артикул WB'], 'photo')
                if not file_exists(os.path.join(
                        'D:\Done', str(line['Артикул WB'])[0:-2] if type(line['Артикул WB']) == float else line['Артикул WB'])):
                    os.mkdir(os.path.join(
                        'D:\Done', str(line['Артикул WB'])[0:-2] if type(line['Артикул WB']) == float else line['Артикул WB']))
                if not file_exists(dest_folder):
                    os.mkdir(dest_folder)
                orig_folder = os.path.join(
                    r'D:\NanoBook', file)
                new_name = os.path.join(
                    'D:\Done', str(line['Артикул WB'])[0:-2] if type(line['Артикул WB']) == float else line['Артикул WB'], 'photo', '1.jpg')
                new_folder = os.path.join(dest_folder, file)
                copyfile(os.path.join(orig_folder), new_folder)
                os.rename(new_folder, new_name)
                print("Done")


main(path_list_stuff)

i = j = 0
path_arh = r'D:\Done'
for dir_ in os.listdir(path_arh):
    if i == Count_Arh:
        j = j+1
        i = 0
    with zipfile.ZipFile(path_arh + '\Done{}.zip'.format(j), 'a') as myzip:
        myzip.write(os.path.join(path_arh, dir_, 'photo', '1.jpg'),
                    arcname=os.path.join('D:\\', dir_, 'photo', '1.jpg'))
    i = i+1
