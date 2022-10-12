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
        self.add_section('CUSTOMER')
        self['CUSTOMER']['Name'] = '<Company Name>'
        self['CUSTOMER']['Branch'] = '<Company Branch>'
        self.add_section('SERVER')
        self['SERVER']['Host'] = '192.168.1.2'
        self['SERVER']['Port'] = '5050'
        self.add_section('PATH')
        self['PATH']['Remote'] = '//192.168.1.2/D3Backups/'
        self['PATH']['Local'] = 'C:/'
        self.add_section('MAIL')
        self['MAIL']['Address'] = '<Email Address>'
        self['MAIL']['Password'] = '<Email Password>'
        self['MAIL']['SMTP_Server'] = '<Outgoing SMTP Server>'
        self['MAIL']['SMTP_Port'] = '<Outgoing SMTP Port>'
        self['MAIL']['To'] = '<email@domain.com> <email@domain.com>' # Add multiple by seperating with space
        self.add_section('LOG')
        self['LOG']['Path'] = path.join('.', 'Logs')
        self['LOG']['Encoding'] = 'utf-8'
        with open('./config.ini', 'w') as configfile:
            self.write(configfile)
