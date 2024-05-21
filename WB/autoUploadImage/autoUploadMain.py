import os
import telebot

from multiprocessing import Process, Queue
# from threading import Thread
from Class.Class import scanFolder, createImage,  uploadXLSX, relocateFile
from Class.tokenOperations import getTokenList


def main():
    queueKar = Queue()
    queueAbr = Queue()
    queueSam = Queue()
    queueFed = Queue()

    workerKarProcess = Process(target=workerCommon, args=(queueKar,))
    workerAbrProcess = Process(target=workerCommon, args=(queueAbr,))
    workerSamProcess = Process(target=workerCommon, args=(queueSam,))
    workerFedProcess = Process(target=workerCommon, args=(queueFed,))

    listProcess = [(workerKarProcess, queueKar), (workerAbrProcess, queueAbr), (workerSamProcess, queueSam), (workerFedProcess, queueFed)]
    listToken = getTokenList()
    listToUploads = scanFolder(listToken)

    for item in listToUploads:
        procesQueueMap = {
            'Караханян': (workerKarProcess, queueKar),
            'Абраамян': (workerAbrProcess, queueAbr),
            'Самвел': (workerSamProcess, queueSam),
            'Иван': (workerFedProcess, queueFed)
        }
        
        worker_process, queue = procesQueueMap[item['Seller']]
        
        if not worker_process.is_alive():
            worker_process.start()
        
        queue.put(item)

    for process, queue in listProcess:
        if process.is_alive():
            queue.put('End')

    for process, _ in listProcess:
        if  process.is_alive():
            process.join()
    # pass  

# def workerKar(queue):
#     workerCommon(queue)

# def workerAbr(queue):
#     workerCommon(queue)

# def workerSam(queue):
#     workerCommon(queue)

# def workerFed(queue):
#     workerCommon(queue)     

def workerCommon(queue):
    while True:
        item = queue.get()
        if item == 'End':
            break
        if createImage(item) is None:
            continue
        uploadXLSX(item)
        try:
            relocateFile(item['pathToFolder'])
        except Exception as e:
            print(f"Error relocating file: {e}")



if __name__ == '__main__':
    main()