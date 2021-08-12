import os
from shutil import copyfile
from my_lib import read_xlsx, write_csv, file_exists
import zipfile


path_list_stuff = r'D:\Список номенклатуры.XLSX'
Count_Arh = 50


def main(path_list_stuff, model_name):

    list_stuff = read_xlsx(path_list_stuff)
    list_barcod = read_xlsx(
        r'D:\prints\{}.xls'.format(model_name), title='No')
    for stuff in list_stuff:
        for barcod in list_barcod:
            if str(stuff['Баркод'])[0:-2] == str(barcod[0]):
                dest_folder = os.path.join(
                    'D:\Done', str(stuff['Артикул WB'])[0:-2], 'photo')
                if not file_exists(os.path.join(
                        'D:\Done', str(stuff['Артикул WB'])[0:-2])):

                    os.mkdir(os.path.join(
                        'D:\Done', str(stuff['Артикул WB'])[0:-2]))
                if not file_exists(dest_folder):
                    os.mkdir(dest_folder)
                orig_folder = os.path.join(
                    'D:\prints', model_name, barcod[3] + '.jpg')
                orig_folder1 = os.path.join(
                    'D:\mask', model_name.replace('_', ' '), '2.jpg')
                orig_folder2 = os.path.join(
                    'D:\mask', model_name.replace('_', ' '), '3.jpg')
                orig_folder3 = os.path.join(
                    'D:\mask', model_name.replace('_', ' '), '4.jpg')
                new_name = os.path.join(
                    'D:\Done', str(stuff['Артикул WB'])[0:-2], 'photo', '1.jpg')
                new_folder = os.path.join(dest_folder, barcod[3]+'.jpg')
                new_folder = os.path.join(dest_folder, barcod[3]+'.jpg')
                copyfile(os.path.join(orig_folder), new_folder)
                copyfile(os.path.join(orig_folder1),
                         new_name.replace('1.jpg', '2.jpg'))
                copyfile(os.path.join(orig_folder2),
                         new_name.replace('1.jpg', '3.jpg'))
                copyfile(os.path.join(orig_folder3),
                         new_name.replace('1.jpg', '4.jpg'))
                os.rename(new_folder, new_name)
                data = {'Артикул WB': str(stuff['Артикул WB'])[0:-2],
                        'Баркод': str(stuff['Баркод'])[0:-2],
                        'Код размера (chrt_id)': str(stuff['Код размера (chrt_id)'])[0:-2]}

                write_csv(data, 'D:\prints\done.csv',)
    print("Done")


for fold in os.listdir(r'D:\prints'):
    if os.path.isdir(os.path.join('D:\prints', fold)) == True:
        main(path_list_stuff, fold)

i = j = 0
path_arh = r'D:\Done'
for dir_ in os.listdir(path_arh):
    if i == Count_Arh:
        j = j+1
        i = 0
    with zipfile.ZipFile(path_arh + '\Done{}.zip'.format(j), 'a') as myzip:
        myzip.write(os.path.join(path_arh, dir_, 'photo', '1.jpg'),
                    arcname=os.path.join('D:\\', dir_, 'photo', '2.jpg'))
        myzip.write(os.path.join(path_arh, dir_, 'photo', '2.jpg'),
                    arcname=os.path.join('D:\\', dir_, 'photo', '2.jpg'))
        myzip.write(os.path.join(path_arh, dir_, 'photo', '3.jpg'),
                    arcname=os.path.join('D:\\', dir_, 'photo', '3.jpg'))
        myzip.write(os.path.join(path_arh, dir_, 'photo', '4.jpg'),
                    arcname=os.path.join('D:\\', dir_, 'photo', '4.jpg'))
    i = i+1
