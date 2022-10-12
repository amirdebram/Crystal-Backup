#!/usr/bin/env python3  

__author__ = 'Amir Debram'
__version__ = '1.0'
__email__ = 'amirdebram@gmail.com'

from os import path, mkdir
from datetime import datetime
from Configuration import Config
import logging


class Log:
    def __init__(self):
        
        if not path.isdir(Config()['LOG']['Path']):
            mkdir(Config()['LOG']['Path'])
        
        if not path.isfile(path.join(Config()['LOG']['Path'], self.current_date() + ".log")):
            with open(path.join(Config()['LOG']['Path'], self.current_date() + ".log"), 'w') as logfile:
                logfile

    def current_date(self):
        year = str(datetime.now().year)
        month = datetime.now().strftime('%B')
        day = datetime.now().strftime('%d')
        return " ".join([year, month, day])

    def write(self, data):        
        logging.basicConfig(
            filename = path.join(Config()['LOG']['Path'], self.current_date() + ".log"), 
            format = '%(asctime)s %(message)s', 
            encoding = Config()['LOG']['Encoding'], 
            level = logging.DEBUG)
        logging.info(data)