from enum import Flag
import os
from shutil import copyfile
from my_lib import read_xlsx, write_csv, file_exists
import zipfile


xlsx = r'D:\Список номенклатуры.XLSX'
Count_Arh = 300


def recreate_data(xlsx):
    data = read_xlsx(xlsx)
    data_new = {}
    for line in data:
        barcod = line['Баркод'] if type(
            line['Баркод']) == str else str(line['Баркод'])[0:-2]
        Art = line['Артикул WB'] if type(
            line['Артикул WB']) == str else str(line['Артикул WB'])[0:-2]
        data_new[barcod] = {'Артикул WB': Art}
    return data_new


def main():

    list_stuff = recreate_data(xlsx)
    list_barcod = read_xlsx(
        r'D:\Список номенклатуры.XLSX', title='No')
    for dirorig in os.listdir(r'D:\printsPy'):
        dir = dirorig.replace("_", ' ').lower()
        for print_ in os.listdir(os.path.join(r'D:\printsPy', dirorig)):
            for line in list_barcod:
                strName = line[11].replace('_', ' ').lower()
                if dir in strName:
                    printName = (
                        '('+print_.replace('print', 'принт').replace("_", ' ').lower()[0:-4]+')')
                    if printName in strName:
                        barcod = line[1] if type(
                            line[1]) == str else str(line[1])[0:-2]
                        dest_folder = os.path.join(
                            r'D:\Done', list_stuff[barcod]['Артикул WB'], 'photo')
                        pathToFile = os.path.join(
                            r'D:\printsPy', dirorig, print_)
                        Artn = list_stuff[barcod]['Артикул WB'] if type(
                            list_stuff[barcod]['Артикул WB']) == str else str(list_stuff[barcod]['Артикул WB'])[0: -2]
                        if not file_exists(dest_folder):
                            os.makedirs(dest_folder)
                        copyfile(pathToFile, os.path.join(dest_folder, print_))
                        os.rename(os.path.join(
                            r'D:\Done', Artn, 'photo', print_), os.path.join(
                            dest_folder, '1.jpg'))


main()

i = j = 0
path_arh = r'D:\Done'
for dir_ in os.listdir(path_arh):
    if i == Count_Arh:
        j = j+1
        i = 0
    with zipfile.ZipFile(path_arh + '\Done{}.zip'.format(j), 'a') as myzip:
        myzip.write(os.path.join(path_arh, dir_, 'photo', '1.jpg'),
                    arcname=os.path.join('D:\\', dir_, 'photo', '1.jpg'))
    i += 1
