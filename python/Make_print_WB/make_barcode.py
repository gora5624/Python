import os
from my_lib import read_xlsx, write_csv
list_barcode_photo = []
tmp_list = []
tmp_list2 = []
for photo_path_tmp in os.listdir(r'D:\prints'):
    tmp_list2 = []
    photo_path = os.path.join('D:\prints', photo_path_tmp)
    list_photo = os.listdir(photo_path)
    list_barcods = read_xlsx(r'D:\Список штрихкодов.xlsx', title='No')
    for photo in list_photo:
        if photo not in tmp_list2:
            tmp_list2.append(photo)
            for barcod in list_barcods:
                if barcod not in tmp_list:
                    tmp_list.append(barcod)
                    data = {'barcod': barcod,
                            'model': photo_path_tmp,
                            'name': photo}
                    write_csv(data, 'D:\prints\list_barcode_photo.csv')
                    list_barcode_photo.append(data)
                    break
