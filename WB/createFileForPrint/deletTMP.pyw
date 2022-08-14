import os
import time


TMPdir = r'E:\Temp'
timer = 48
while True:
    for file in os.listdir(TMPdir):
        #if "Corel" in file:
        try:
            os.remove(os.path.join(TMPdir, file))
        except:
            pass
time.sleep(60*60*timer)