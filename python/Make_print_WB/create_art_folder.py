import os
from shutil import copyfile
from my_lib import read_xlsx, file_exists
import zipfile


path_list_stuff = r'D:\Список номенклатуры — копия.XLSX'
Count_Arh = 200


def main(path_list_stuff, model_name):

    list_stuff = read_xlsx(path_list_stuff)
    list_barcod = read_xlsx(
        r'D:\printsPy\{}.xlsx'.format(model_name), title='No')
    for stuff in list_stuff:
        for barcod in list_barcod:
            if stuff['Баркод'] == str(barcod[0]):
                dest_folder = os.path.join(
                    'D:\Done', str(stuff['Артикул WB'])[0:-2], 'photo')
                if not file_exists(os.path.join(
                        'D:\Done', str(stuff['Артикул WB'])[0:-2])):

                    os.mkdir(os.path.join(
                        'D:\Done', str(stuff['Артикул WB'])[0:-2]))
                if not file_exists(dest_folder):
                    os.mkdir(dest_folder)
                orig_folder = os.path.join(
                    'D:\printsPy', model_name, barcod[3] + '.jpg')
                new_name = os.path.join(
                    'D:\Done', str(stuff['Артикул WB'])[0:-2], 'photo', '1.jpg')
                new_folder = os.path.join(dest_folder, barcod[3]+'.jpg')
                copyfile(os.path.join(orig_folder), new_folder)
                os.rename(new_folder, new_name)
                print("Done")


for fold in os.listdir(r'D:\printsPy'):
    if os.path.isdir(os.path.join('D:\printsPy', fold)) == True:
        main(path_list_stuff, fold)

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
