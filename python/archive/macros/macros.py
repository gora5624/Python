import win32com.client
import keyboard
from pywinauto.keyboard import send_keys
import time


def test():
    time.sleep(5)
    send_keys('для{SPACE}женщин'
              '{ENTER}'
              'для{SPACE}мужчин'
              '{ENTER}')


def mac(key):
    keyboard.add_hotkey("Alt + 1", test)
    keyboard.wait("Alt + 1")


mac('Alt + 1')
