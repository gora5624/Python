import os

from multiprocessing import Process, Queue, cpu_count
# from threading import Thread
from Class import scanFolder, createImage,  uploadXLSX, getTokenList, relocateFile


def main():
    queueKar = Queue()
    queueAbr = Queue()
    queueSam = Queue()
    queueFed = Queue()
    workerKarProcess = Process(target=workerKar, args=(queueKar,))
    workerAbrProcess = Process(target=workerSam, args=(queueAbr,))
    workerSamProcess = Process(target=workerAbr, args=(queueSam,))
    workerFedProcess = Process(target=workerFed, args=(queueFed,))
    listProcess = [(workerKarProcess, queueKar), (workerAbrProcess, queueAbr), (workerSamProcess, queueSam), (workerFedProcess, queueFed)]
    listToken = getTokenList()
    listToUploads = scanFolder(listToken)
    for item in listToUploads:
        if item['Seller'] == 'Караханян':
            if not workerKarProcess.is_alive():
                workerKarProcess.start()
            queueKar.put(item)
        if item['Seller'] == 'Абраамян':
            if not workerAbrProcess.is_alive():
                workerKarProcess.start()
            queueAbr.put(item)
        if item['Seller'] == 'Самвел':
            if not workerSamProcess.is_alive():
                workerKarProcess.start()
            queueSam.put(item)
        if item['Seller'] == 'Иван':
            if not workerFedProcess.is_alive():
                workerKarProcess.start()
            queueFed.put(item)
    for p in listProcess:
        if p[0].is_alive():
            p[1].put('End')
    for p in listProcess:
        if  p[0].is_alive():
            p[0].join()
    # pass

def workerKar(queue):
    while True:
        item = queue.get()
        if item == 'End':  # Использование сигнального объекта для определения окончания работы
            break
        createImage(item)
        uploadXLSX(item)
        try:
            relocateFile(item['pathToFolder'])
        except:
            pass

def workerAbr(queue):
    while True:
        item = queue.get()
        if item == 'End':  # Использование сигнального объекта для определения окончания работы
            break
        createImage(item)
        uploadXLSX(item)

def workerSam(queue):
    while True:
        item = queue.get()
        if item == 'End':  # Использование сигнального объекта для определения окончания работы
            break
        createImage(item)
        uploadXLSX(item)

def workerFed(queue):
    while True:
        item = queue.get()
        if item == 'End':  # Использование сигнального объекта для определения окончания работы
            break
        createImage(item)
        uploadXLSX(item)



if __name__ == '__main__':
    main()