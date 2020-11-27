import os


def ListFileInDir(DirPath):
    ListFile = os.listdir(DirPath)
    return ListFile


def FindNone(ListImg, ListFileDir2):

    for File in ListImg:
        FileNewName = File.replace('.jpg', '.pdf')
        if FileNewName not in ListFileDir2:
            print(File)


def main(DirImg, DirPath2):
    ListImg = ListFileInDir(DirImg)
    ListFileDir2 = ListFileInDir(DirPath2)
    FindNone(ListImg, ListFileDir2)


DirImg = r'D:\tab'
DirPath2 = r'D:\Pac\Antispy'


if __name__ == "__main__":
    main(DirImg, DirPath2)
