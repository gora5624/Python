import os
from my_lib import read_xlsx, generate_bar_WB
import xlwt
list_barcode_photo = []
tmp_list = []
tmp_list2 = []


def make_bar(photo_path_tmp):
    list_nom = read_xlsx(r'D:\список номенклатуры 1C.XLSX', title='No')
    for nom in list_nom:
        if photo_path_tmp.replace(
                '_', ' ') == nom[1]:
            kod_1C = nom[3]
            break
        else:
            kod_1C = None
    tmp_list2 = []
    write_data = []
    photo_path = os.path.join('D:\prints', photo_path_tmp)
    list_photo = os.listdir(photo_path)

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Лист 1')
    for photo in list_photo:
        if photo not in tmp_list2:
            tmp_list2.append(photo)
            barcod = generate_bar_WB()
            data = [barcod,
                    photo_path_tmp.replace(
                        '_', ' ') + ' ' + photo.replace('.jpg', ''),
                    kod_1C,
                    photo.replace('.jpg', '')]
            write_data.append(data)

    for row_index, row in enumerate(write_data):
        for col_index, el in enumerate(row):
            ws.write(row_index, col_index, el)
    wb.save(r'D:\prints\{}.xls'.format(photo_path_tmp))


# make_bar(r'Чехол_для_Samsung_Galaxy_M32_силикон_прозрачный')


for photo_path_tmp in os.listdir(r'D:\prints'):
    make_bar(photo_path_tmp)
