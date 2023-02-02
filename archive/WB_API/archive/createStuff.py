from json import encoder
from os.path import join as joinpath
from datetime import datetime, timedelta
import re
import requests
from my_lib import file_exists, read_xlsx
from os import makedirs
import pandas
from my_lib import read_xlsx
import json
import multiprocessing

main_path = r'C:\Users\Public\Documents\WBCreateStuff'
Token_path = joinpath(main_path, r'Token.txt')
pathToCreateList = joinpath(main_path, r'createList.xlsx')
