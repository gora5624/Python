from flask import Flask, request, render_template
import os, ctypes
import time
import requests
from threading import Thread
from multiprocessing import Process, Manager, Value, freeze_support

import botMain as Bot

botStarted = False

app = Flask(__name__, template_folder='templates')

@app.route("/ServerMOBI/bot")
def mainurl():
    req = request.args.get('IP')
    if botStarted == False:
        hostname = request.headers.get('Host')
        p = Process(target=Doing, args=(req,hostname,))
        p.start()
        p.join()
        return render_template('/bot/BotSetting.html')
    else:
        return render_template('bot/BotWait.html')

@app.route("/ServerMOBI/AdditionalRoute")
def VarSync():
    req = request.args.get('ChangeBotStartedBool')
    if req == 'True':
        global botStarted
        botStarted = not botStarted

    return 'VarSync end'

def Doing(IP,hostname):
    params = {'ChangeBotStartedBool': True}
    requests.get('http://'+hostname+'/ServerMOBI/AdditionalRoute', params=params)
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
    requests.get('http://' + hostname + '/ServerMOBI/AdditionalRoute', params=params)
    return


