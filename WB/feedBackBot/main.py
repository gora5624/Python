import time
import requests
from threading import Thread
from multiprocessing import Process, Manager, Value, freeze_support

import botMain as Bot

botStarted = False


def Doing(IP,hostname):
    if (IP == 'Abr'):
        Bot.StartAbr()
    if (IP == 'Kar'):
        Bot.StartKar()
    if (IP == 'Sam'):
        Bot.StartSam()
    if (IP == 'Fed'):
        Bot.StartFed()
    if (IP == 'All'):
        Bot.StartAll()
    return

