# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__),'modules'))

from flask import Flask, render_template
from turbo_flask import Turbo
import threading
import random
import time
from modules import orders

app = Flask(__name__)
app = Flask(__name__, static_folder=r'static')
turbo = Turbo(app)

@app.route('/')
def index():
    return render_template(r'index.html')

@app.route('/page2.html')
def page2():
    return render_template(r'page2.html')

@app.route('/orders')
def orders_page():
    return orders.get_orders()

@app.context_processor
def inject_load():
    load = [int(random.random() * 100) / 100 for _ in range(3)]
    return {'load1': load[0], 'load5': load[1], 'load15': load[2]}

def update_load():
    with app.app_context():
        while True:
            time.sleep(5)
            turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))

isRunning = False
@app.before_request
def before_request():
    global isRunning
    if not isRunning:
        t = threading.Thread(target=update_load).start()
        print("T start")
        isRunning = True
    else:
        print('alredy start')


if __name__ == '__main__':
    app.run()