import os
from my_lib import read_xlsx, write_csv, file_exists

list_stuff = read_xlsx(r'D:\report_2021_5_10.XLSX')
list_barcod = read_xlsx(r'D:\prints\list_barcode_photo.xlsx')
for stuff in list_stuff:
    for barcod in list_barcod:
        if stuff['Баркод'] == str(barcod['barcod'])[0:-2]:
            dest_folder = os.path.join(
                'D:\Done', str(stuff['Артикул WB'])[0:-2], 'photo')
            if not file_exists(os.path.join(
                    'D:\Done', str(stuff['Артикул WB'])[0:-2])):

                os.mkdir(os.path.join(
                    'D:\Done', str(stuff['Артикул WB'])[0:-2]))
            if not file_exists(dest_folder):
                os.mkdir(dest_folder)
            orig_folder = os.path.join(
                'D:\prints', barcod['model'], barcod['name'])
            new_name = os.path.join(
                'D:\Done', str(stuff['Артикул WB'])[0:-2], 'photo', '1.jpg')
            new_folder = os.path.join(dest_folder, barcod['name'])
            os.replace(os.path.join(orig_folder), new_folder)
            os.rename(new_folder, new_name)
            data = {'Артикул WB': str(stuff['Артикул WB'])[0:-2],
                    'Баркод': str(stuff['Баркод'])[0:-2],
                    'Код размера (chrt_id)': str(stuff['Код размера (chrt_id)'])[0:-2]}

            write_csv(data, 'D:\prints\done.csv',)
print(list_stuff)
