import logging
import os

LOGGING_LEVEL = logging.WARNING
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGING_FILE = os.path.abspath(os.path.join(__file__, '..', r'application.log'))

def setup_logging():
    logging.basicConfig(level=LOGGING_LEVEL,
                        format=LOGGING_FORMAT,
                        handlers=[
                            logging.FileHandler(LOGGING_FILE),
                            logging.StreamHandler()
                        ])

setup_logging()