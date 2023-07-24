import os, json
import configparser
import sys

from Func import *

config = configparser.ConfigParser()
config.read(r'E:\MyProduct\Python\WB\ServerMOBI\settings.ini', "utf8")


def Start(Token):
    stop_list = json.loads(config.get("MainSettings", "stop_list"))

    requests = RequestFeedback(Token)

    WriteFeedbacks(requests, stop_list)

    answerLen = WriteFeedbacks(requests, stop_list)[0]
    stop_listLen = WriteFeedbacks(requests, stop_list)[1]
    otherLen = WriteFeedbacks(requests, stop_list)[2]

    ############
    for i in range(answerLen):
        feedback = LoadFeedback('answer', i)[0]
        
        print('отзыв:', feedback['Text'])
        answer = GenAnswer(r'E:\MyProduct\Python\WB\ServerMOBI\combination repons.xlsx', feedback)
        print('ответ:', answer)
        WriteAnswer(answer, feedback, Token)
        print('--------------------------------------------------')
    print('Итог:', answerLen)

def StartAbr():
    try: Start(Token = config["MainSettings"]["tokenAbr"])
    except: pass
def StartKar():
    try: Start(Token = config["MainSettings"]["tokenKar"])
    except: pass
def StartSam():
    try: Start(Token = config["MainSettings"]["tokenSam"])
    except: pass
def StartFed():
    try: Start(Token = config["MainSettings"]["tokenFed"])
    except: pass
def StartAll():
    try: Start(Token = config["MainSettings"]["tokenAbr"])
    except : pass

    try: Start(Token=config["MainSettings"]["tokenKar"])
    except : pass

    try: Start(Token=config["MainSettings"]["tokenSam"])
    except : pass

    try: Start(Token=config["MainSettings"]["tokenFed"])
    except : pass

