from datetime import datetime
import os
from datetime import datetime

class LogMaker():
    def __init__(self) -> None:
        pass

    @staticmethod
    def metodStart(methodName='',methodArgs={}):
        with open(os.path.join(r'E:\MyProduct\Python\WB\MakePrint', 'log.txt'), 'a') as logFile:
            logFile.write('{}\t Method {} start with args:\n'.format(datetime.now(), methodName))
            if methodArgs != {}:
                for key,value in methodArgs.items():
                    logFile.write('{}\t arg Name = {}, value = {} \n'.format(datetime.now(),key, value))
            else:
                logFile.write('{}\t arg None \n'.format(datetime.now()))
    
    @staticmethod
    def metodEnd(methodName='',result=''):
        with open(os.path.join(r'E:\MyProduct\Python\WB\MakePrint', 'log.txt'), 'a') as logFile:
            logFile.write('{}\t Method {} end with result:\n'.format(datetime.now(), methodName))
            if result != '':
                logFile.write('{}\t result = {}\n'.format(datetime.now(),result))
            else:
                logFile.write('{}\t result None \n'.format(datetime.now()))

    @staticmethod
    def logAction(methodName='',action=''):
        pass
        # with open(os.path.join(r'E:\MyProduct\Python\WB\MakePrint', 'log.txt'), 'a') as logFile:
        #     logFile.write('{}\t Method {} in do some:\n'.format(datetime.now(), methodName))
        #     if action != '':
        #         logFile.write('{}\t action = {}\n'.format(datetime.now(),action))
    




