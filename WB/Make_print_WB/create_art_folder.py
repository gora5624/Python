import os
from shutil import copyfile
import sys
sys.path.insert(1, os.path.abspath(os.path.join(__file__,'../../..','my_mod')))
from my_lib import read_xlsx, file_exists
import zipfile
import multiprocessing
from PIL import Image

workDisk = 'E'
#path_list_stuff = r'C:\Users\Public\Documents\WBChangeStuff\barcodes and art.xlsx'
path_list_stuff = r'\\192.168.0.33\shared\Отдел производство\Wildberries\Список номенклатуры — копия.XLSX'
pathToPrint = r'{}:\ForPrints\printsPy'.format(workDisk)
pathToDone = r'{}:\ForPrints\Done'.format(workDisk)
pathToMask = r'{}:\ForPrints\mask'.format(workDisk)
Count_Arh = 200


def main(path_list_stuff, model_name):
    list_stuff = read_xlsx(path_list_stuff)
    list_barcod = read_xlsx(
        os.path.join(pathToPrint,'{}.xlsx'. format(model_name)), title='No') if file_exists(
         os.path.join(pathToPrint,'{}.xlsx'. format(model_name))) else read_xlsx( os.path.join(pathToPrint,'{}.xlsx'. format(model_name)), title='No')
    if 'прозрачный' not in model_name:
        try:
            image = Image.open(os.path.join(
                pathToMask, model_name, '2' + '.jpg')).convert('RGB')
            size = image.size
            size_new = (900, int(float(size[1])*(900.0/float(size[0]))))
            image = image.resize(size_new)
            image.save(os.path.join(
                pathToMask, model_name, '2_res' + '.jpg'),
                quality=70)
        except:
            pass
    for stuff in list_stuff:
        for barcod in list_barcod:
            if (str(stuff['Баркод'])[0:-2] if type(stuff['Баркод']) == float else stuff['Баркод']) == (str(barcod[0])[0:-2] if type(barcod[0]) == float else str(barcod[0])):
                dest_folder = os.path.join(
                    pathToDone, str(stuff['Артикул WB'])[0:-2], 'photo')
                if not file_exists(os.path.join(
                        pathToDone, str(stuff['Артикул WB'])[0:-2])):
                    os.mkdir(os.path.join(
                        pathToDone, str(stuff['Артикул WB'])[0:-2]))
                if not file_exists(dest_folder):
                    os.mkdir(dest_folder)
                mask_folder = os.path.join(
                    pathToMask, model_name, '2' + '.jpg')
                mask_folder_res = os.path.join(
                    pathToMask, model_name, '2_res' + '.jpg')
                orig_folder = os.path.join(
                    pathToPrint, model_name, barcod[3] + '.jpg').replace('))', ')')
                new_name = os.path.join(
                    pathToDone, str(stuff['Артикул WB'])[0:-2], 'photo', '1.jpg')
                new_folder = os.path.join(
                    dest_folder, barcod[3]+'.jpg').replace('))', ')')
                new_name_2 = os.path.join(dest_folder, '2_res'+'.jpg')
                copyfile(os.path.join(orig_folder), new_folder)
                if 'прозрачный' not in model_name:
                    try:
                        copyfile(os.path.join(mask_folder_res), new_name_2)
                    except:
                        pass
                try:
                    os.rename(new_folder, new_name)
                except FileExistsError:
                    continue
                print(model_name)


if __name__ == '__main__':
    pool = multiprocessing.Pool()
    for fold in os.listdir(pathToPrint):
        if os.path.isdir(os.path.join(pathToPrint, fold)) == True:
            pool.apply_async(main, args=(path_list_stuff, fold,))
    pool.close()
    pool.join()

    i = j = 0
    path_arh = pathToDone
    for dir_ in os.listdir(path_arh):
        if i == Count_Arh:
            j = j+1
            i = 0
        with zipfile.ZipFile(path_arh + '\Done{}.zip'.format(j), 'a') as myzip:
            myzip.write(os.path.join(path_arh, dir_, 'photo', '1.jpg'),
                        arcname=os.path.join('{}:\\'.format(workDisk), dir_, 'photo', '1.jpg'))
            try:
                myzip.write(os.path.join(path_arh, dir_, 'photo', '2_res.jpg'),
                            arcname=os.path.join('{}:\\'.format(workDisk), dir_, 'photo', '2.jpg'))
            except:
                pass
        i = i+1
