#!/usr/bin/env python3  

__author__ = 'Amir Debram'
__version__ = '1.0'
__email__ = 'amirdebram@gmail.com'

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import (
    QDialog, 
    QFormLayout,
    QDialogButtonBox, QMessageBox,
    QLabel, QLineEdit
    )

from configparser import ConfigParser
from Libraries.Logging import Log



class ServerDialog(QDialog):
    def __init__(self, parent=None):
        super(ServerDialog, self).__init__(parent)

        self.initUI()

    def initUI(self):
        self.lsHost = QLineEdit()
        self.lsPort = QLineEdit()

        self.Buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.Buttons.accepted.connect(self.prompt)
        self.Buttons.rejected.connect(self.reject)

        self.Layout = QFormLayout()
        self.Layout.addRow(QLabel("Server Host")    , self.lsHost )
        self.Layout.addRow(QLabel("Server Port")    , self.lsPort )
        self.Layout.addRow(self.Buttons)
        self.setLayout(self.Layout)

        self.resize(250, 150)
        self.center()
        self.setWindowTitle('Server Settings')
        
    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def prompt(self):
        reply = QMessageBox.question(None, 'Save Changes', f"Would you like to save your changes?", 
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.modify_config_files()
            Log().write(f"[SERVER CONFIGUARTION] -> Modified")
        else:
            Log().write(f"[SERVER CONFIGUARTION] -> Not Saved")

    def modify_config_files(self):
        config = ConfigParser()
        config.read('./config.ini')
        config.set('SERVER', 'Host', self.lsHost.text())
        config.set('SERVER', 'Port', self.lsPort.text())
        with open('./config.ini', 'w') as configfile:
            config.write(configfile)
        
        QMessageBox.information(None, 'Configuration Saved', 'Server Settings has been saved!', QMessageBox.StandardButton.Ok)
        self.close()

