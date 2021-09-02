from os.path import join as joinpath
from datetime import datetime, timedelta
import re
import requests
from my_lib import file_exists, read_xlsx
from os import makedirs
import pandas
from my_lib import read_xlsx


pathToListStuff = r'D:\A22.xlsx'


def getIdWithBarcod(barcod):


def getIdFromListStuff(pathToListStuff):
    dataFromLIstStuff = read_xlsx(pathToListStuff)
    for stuffLine in dataFromLIstStuff:
        barcod = stuffLine['Баркод'] if type(
            stuffLine['Баркод']) == str else str(stuffLine['Баркод'])[0:-2]
        idStuff = getIdWithBarcod(barcod)
