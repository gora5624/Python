import pickle
import os
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

def getTokenList():
    try:
        with open(os.path.abspath(os.path.join(__file__, '../..', 'token.pkl')), 'rb') as f:
            logger.info("Token list loaded successfully")
            return pickle.load(f)
    except (OSError, IOError) as e:
        logger.error(f"Error loading token list: {e}")
        return {}
    
def getTeleToken():
    try:
        with open(os.path.abspath(os.path.join(__file__, '../..', 'TeleToken.pkl')), 'rb') as f:
            logger.info("telegram token list loaded successfully")
            tmp = pickle.load(f)
            return (tmp['token'], tmp['chatID'])
    except (OSError, IOError) as e:
        logger.error(f"Error loading telegrem token list: {e}")
        return {}

def saveToken():
    tmp = {
    'Караханян':'',
    'Абраамян':'',   
    'Самвел':'',
    'Иван':''
    }
    pickle.dump(tmp, open(os.path.abspath(os.path.join(__file__, '..', r'token.pkl')), 'wb'))

def saveTeleToken():
    tmp = {
    'token':'5583996306:AAH1WOjS3MgJkNoaxjtewQQ5QWXIxh-fjpw',
    'chatID':-1001550015840   
    }
    pickle.dump(tmp, open(os.path.abspath(os.path.join(__file__, '..', r'TeleToken.pkl')), 'wb'))