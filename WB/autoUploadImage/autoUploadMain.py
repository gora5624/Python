import os
import telebot
import logging

from multiprocessing import Process, Queue, Manager

from Class.AdClass import scanFolder, uploadXLSX, relocateFile
from Class.tokenOperations import getTokenList
from Class.imageOperations import createImage

from telegramNotifications import send_message
from loggingСonfig import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

class Report:
    def __init__(self, manager):
        self.data = manager.Namespace()
        self.data.started = 0
        self.data.completed = 0
        self.data.errors = manager.list()

    def start(self):
        self.data.started += 1

    def complete(self):
        self.data.completed += 1

    def add_error(self, item, error):
        self.data.errors.append((item, error))

    def generate_report(self):
        report = f"Программа завершена.\nВсего обработано задач: {self.data.started}\nУспешно завершено: {self.data.completed}\nОшибки:\n"
        if not self.data.errors:
            report += "Были обработаны без ошибок.\n"
        else:
            for item, error in self.data.errors:
                report += f"- {item}: {error}\n"
        return report


def main():

    send_message('#ФОТО программа высталения товара запущена.')
    manager = Manager()
    report = Report(manager)
    queueKar = Queue()
    queueAbr = Queue()
    queueSam = Queue()
    queueFed = Queue()

    workerKarProcess = Process(target=workerCommon, args=(queueKar, report))
    workerAbrProcess = Process(target=workerCommon, args=(queueAbr, report))
    workerSamProcess = Process(target=workerCommon, args=(queueSam, report))
    workerFedProcess = Process(target=workerCommon, args=(queueFed, report))

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

    send_message(report.generate_report())
    # send_message('#ФОТО программа завершила работу.')
    
    # pass  

# def workerKar(queue):
#     workerCommon(queue)

# def workerAbr(queue):
#     workerCommon(queue)

# def workerSam(queue):
#     workerCommon(queue)

# def workerFed(queue):
#     workerCommon(queue)     

def workerCommon(queue, report):
    while True:
        item = queue.get()
        if item == 'End':
            logger.info('Worker received end signal.')
            break
        report.start()
        if createImage(item) is None:
            logger.warning(f"Creating image failed for {item['dirName']}")
            send_message(f"Creating image failed for {item['dirName']}")
            report.add_error(item['dirName'], "Creating image failed")
            continue
        try:
            uploadXLSX(item)
            report.complete()
            relocateFile(item['pathToFolder'])
        except Exception as e:
            error_msg = f"Error processing item {item['dirName']}: {e}"
            logger.error(error_msg)
            report.add_error(item['dirName'], str(e))
            send_message(error_msg)



if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        error_msg = f"Unhandled exception: {e}"
        logger.error(error_msg)
        send_message(error_msg)