#!/usr/bin/env python3  

__author__ = 'Amir Debram'
__version__ = '1.0'
__email__ = 'amirdebram@gmail.com'

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import (
    QDialog, QFileDialog,
    QHBoxLayout, QVBoxLayout,
    QMessageBox, QDialogButtonBox,
    QLabel, QLineEdit, QPushButton
    )

from configparser import ConfigParser
from Libraries.Configuration import Config
from Libraries.Logging import Log

class BackupDialog(QDialog):
    def __init__(self, parent=None):
        super(BackupDialog, self).__init__(parent)

        self.initUI()

    def initUI(self):
        
        self.remoteLabel = QLabel("Folder to Backup: ")
        self.remoteLineEdit = QLineEdit()
        self.remoteButtonBrowse = QPushButton("Browse")
        self.remoteButtonBrowse.clicked.connect(self.browseRemote)

        self.localLabel = QLabel("Destination Path: ")
        self.localLineEdit = QLineEdit()
        self.localButtonBrowse = QPushButton("Browse")
        self.localButtonBrowse.clicked.connect(self.browseLocal)
        
        self.Buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.Buttons.accepted.connect(self.prompt)
        self.Buttons.rejected.connect(self.reject)   
        
        self.remoteLayout = QHBoxLayout()
        self.remoteLayout.addWidget(self.remoteLabel)
        self.remoteLayout.addWidget(self.remoteLineEdit)
        self.remoteLayout.addWidget(self.remoteButtonBrowse)
        
        self.localLayout = QHBoxLayout()
        self.localLayout.addWidget(self.localLabel)
        self.localLayout.addWidget(self.localLineEdit)
        self.localLayout.addWidget(self.localButtonBrowse)
        
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.Buttons)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.remoteLayout)
        self.mainLayout.addLayout(self.localLayout)
        self.mainLayout.addLayout(self.buttonLayout)
        
        self.setLayout(self.mainLayout)

        self.resize(600, 200)
        self.center()
        self.setWindowTitle('Backup Settings')
        
    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def browseRemote(self):
        path = Config()['PATH']['Remote']
        directory = QFileDialog.getExistingDirectory(self, "Choose Folder", directory=path)
        if directory:
            self.remoteLineEdit.setText(directory.replace('\\', '/'))

    def browseLocal(self):
        path = Config()['PATH']['Local']
        directory = QFileDialog.getExistingDirectory(self, "Choose Folder", directory=path)
        if directory:
            self.localLineEdit.setText(directory.replace('\\', '/'))
    
    def prompt(self):
        reply = QMessageBox.question(None, 'Save Changes', f"Would you like to save your changes?", 
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.modify_config_files()
            Log().write(f"[BACKUP CONFIGUARTION] -> Modified")
        else:
            Log().write(f"[BACKUP CONFIGUARTION] -> Not Saved")
            
    def modify_config_files(self):
        config = ConfigParser()
        config.read('./config.ini')
        config.set('PATH', 'Remote', self.remoteLineEdit.text())
        config.set('PATH', 'Local', self.localLineEdit.text())
        with open('./config.ini', 'w') as configfile:
            config.write(configfile)
        
        QMessageBox.information(None, 'Configuration Saved', 'Backup Settings has been saved!', QMessageBox.StandardButton.Ok)
        # self.initLogging(f"{host_port} [NEW CONNECTION] -> Client")
        self.close()

