from CombineImage import combineImage
from os.path import abspath
from os.path import join as joinPath
from os import listdir
import requests
import multiprocessing

pathToMasks = abspath(joinPath(__file__, '..',r'BookPic\BookMask'))
pathToBacks = abspath(joinPath(__file__, '..',r'BookPic\BookBack'))


def makeBookPrint():
    pool = multiprocessing.Pool()
    for mask in listdir(pathToMasks):
        pathToMask = joinPath(pathToMasks, mask)
        pathToBack = joinPath(pathToBacks, mask.replace('.png', '.jpg'))
        pool.apply_async(combineImage, args=(pathToBack, pathToMask, ))
    pool.close()
    pool.join()


 



if __name__ == '__main__':
    makeBookPrint()