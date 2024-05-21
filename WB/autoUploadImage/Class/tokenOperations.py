import pickle
import os

def getTokenList():
    return pickle.load(open(os.path.abspath(os.path.join(__file__, '../..', r'token.pkl')), 'rb'))

def saveToken():
    tmp = {
    'Караханян':'',
    'Абраамян':'',   
    'Самвел':'',
    'Иван':''
    }
    pickle.dump(tmp, open(os.path.abspath(os.path.join(__file__, '..', r'token.pkl')), 'wb'))