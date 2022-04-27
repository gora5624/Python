from Moduls.CombineImage import combineImage
from os.path import abspath
from os.path import join as joinPath
from os import listdir
import sys
sys.path.append(abspath(joinPath(__file__,'../..')))
from Folders import pathToBookMasks, pathToBookBacks
import multiprocessing


def makeBookPrint():
    pool = multiprocessing.Pool()
    for mask in listdir(pathToBookMasks):
        pathToMask = joinPath(pathToBookMasks, mask)
        pathToBack = joinPath(pathToBookBacks, mask.replace('.png', '.jpg'))
        pool.apply_async(combineImage, args=(pathToBack, pathToMask, ))
    pool.close()
    pool.join()


if __name__ == '__main__':
    makeBookPrint()