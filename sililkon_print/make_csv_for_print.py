from my_lib import write_csv, read_csv, file_exists
import os


path = r'D:\tmp\my_prod\Python\sililkon_print'
ListCase = read_csv(path + '\list.csv')
ListPrint = read_csv(path + '\\name_print\print_theme.csv')
count = 0
num = 0
for Case in ListCase:
    for Print in ListPrint:

        PrintNum = Print['NamePrint'][6:9]
        CaseName = Case['Name'] + ' ' + Print['NamePrint'][0:-4]
        DetailPic = '/upload/products_pictures/silicone/' + \
            Case['Name'].replace('/', '').replace('\\',
                                                  '').replace('Чехол для ', '').replace(' силикон черный матовый', '') + '/mate/black/' + Print['NamePrint'][0:-4] + '.jpg'
        Theme = Print['Theme']
        Cod = Case['Cod']
        ServiceCode = '00-00038357'
        data = {"PRINT_NUM": PrintNum,
                "IE_NAME": CaseName,
                "IE_DETAIL_PICTURE": DetailPic,
                "IP_PROP_THEME": Theme,
                "PRODUCT_CODE": Cod,
                "SERVICE_CODE": ServiceCode}

        write_csv(data, os.path.join(path, 'A_Brand_{}.csv'.format(num)))
        count += 1
        if count > 9999:
            count = 0
            num += 1
