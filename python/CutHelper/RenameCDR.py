import os
import sys
from my_lib import read_xlsx, file_exists

if __name__ == "__main__":
    if len(sys.argv) > 1:

        order_path = sys.argv[1]
        cdrPath = r'\\192.168.0.33\shared\Отдел производство\Wildberries\Макеты'
        cdrList = os.listdir(cdrPath)
        order = read_xlsx(order_path, 'No')
        ordetTXTpath = r'C:\Users\Public\Documents\CutHelp\order.txt'

        if file_exists(ordetTXTpath):
            os.remove(ordetTXTpath)
        with open(ordetTXTpath, 'a', encoding='ANSI') as file:
            for row in order:
                for cdr in cdrList:
                    if row[1] in cdr:
                        file.writelines('\\\\192.168.0.33\shared\Отдел производство\Wildberries\Макеты\\' + cdr +
                                        ';' + str(row[3]) +
                                        ';' + str(row[1]) + '\n')
            file.close()
    else:
        print("Error")
        input("Всё пошло не по плану!")
