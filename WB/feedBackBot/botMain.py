import os, json
import configparser
import time
import telebot
import datetime


from Func import *

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(__file__,'..', 'settings.ini')), "utf8")
botToken = open(os.path.abspath(os.path.join(__file__,'..', 'token')), 'r').read()
bot = telebot.TeleBot(botToken)
# bot.config['api_key'] = botToken

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
        # print('отзыв:', feedback['Text'])
        answer = GenAnswer(os.path.abspath(os.path.join(__file__,'..', 'combination repons.xlsx')), feedback)
        # print('ответ:', answer)
        WriteAnswer(answer, feedback, Token)
        # print('--------------------------------------------------')
        # bot.send_message(-1001550015840, r'Отзыв: {}. ----- Ответ: {}'.format(feedback['Text'],answer))
        log(r'Отзыв: {}. ----- Ответ: {}'.format(feedback['Text'],answer))
        time.sleep(3)
    # print('Итог:', answerLen)
    

def log(mess):
    with open(os.path.join(os.path.dirname(__file__), r'log'), 'a', encoding='utf-8') as logFile:
        logFile.write(mess + ' ' + datetime.datetime.now().strftime('%d.%m.%y, %H:%M:%S') + '\n')
        logFile.close()

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
    global bot
    a = bot.send_message(-1001550015840, 'Начал отвечать')
    try: Start(Token = config["MainSettings"]["tokenAbr"])
    except : bot.send_message(-1001550015840, 'Ошибка при запуске на Манвела')
    try: Start(Token=config["MainSettings"]["tokenKar"])
    except : bot.send_message(-1001550015840, 'Ошибка при запуске на Караханян')
    try: Start(Token=config["MainSettings"]["tokenSam"])
    except : bot.send_message(-1001550015840, 'Ошибка при запуске на Самвел')
    try: Start(Token=config["MainSettings"]["tokenFed"])
    except : bot.send_message(-1001550015840, 'Ошибка при запуске на Федоров')
    bot.send_message(-1001550015840, 'Закончил отвечать без ошибок')

if __name__ == '__main__':
    StartAll()