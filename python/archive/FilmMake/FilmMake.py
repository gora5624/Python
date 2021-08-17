import os
from my_lib import write_csv, read_csv


def RenameFile(DictListFile):
    MainPath = r'D:\Done\NanoPlus'
    for File in DictListFile:
        try:

            OldName = os.path.join(
                MainPath, File['Models'].replace(' ', '-') + '.jpg')
            NewName = os.path.join(
                MainPath, File['ModelsNew'].replace('/', '').replace(' ', '-') + '.jpg')
            os.rename(OldName, NewName)
        except:
            print(File['Models'])


def GetDictListFile(PathFile):
    DictListFile = read_csv(PathFile)
    return DictListFile


def main(PathFile):
    DictListFile = GetDictListFile(PathFile)
    RenameFile(DictListFile)


PathFile = r'D:\tmp\my_prod\Python\Rename.csv'


if __name__ == "__main__":
    main(PathFile)
