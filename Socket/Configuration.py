#!/usr/bin/env python3  

__author__ = 'Amir Debram'
__version__ = '1.0'
__email__ = 'amirdebram@gmail.com'

from os import path
from configparser import ConfigParser


class Config(ConfigParser):
    def __init__(self, parent=None):
        super(Config, self).__init__(parent)
    
        self.read(self.createConfig())
    
    def createConfig(self, filename: str = './config.ini') -> str:
        if not path.isfile(filename):
            self.generateConfiguration()
        return filename
        
    def generateConfiguration(self):
        self.add_section('SERVER')
        self['SERVER']['Port'] = '5050'
        self.add_section('PATH')
        self['PATH']['Local'] = '//192.168.1.2/temp/'
        self.add_section('BACKUP')
        self['BACKUP']['Files'] = 'monday tuesday wednesday thursday friday saturday sunday mirror'
        self.add_section('CLIENTS')
        self['CLIENTS']['Max'] = '2'
        self.add_section('LOG')
        self['LOG']['Path'] = path.join('.', 'Logs')
        self['LOG']['Encoding'] = 'utf-8'
        with open('./config.ini', 'w') as configfile:
            self.write(configfile)
