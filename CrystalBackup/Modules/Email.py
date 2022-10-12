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
from Libraries.Configuration import Config
from Libraries.Logging import Log

import smtplib, ssl


class EmailDialog(QDialog):
    def __init__(self, parent=None):
        super(EmailDialog, self).__init__(parent)

        self.initUI()

    def initUI(self):
        self.emailAddress = QLineEdit()
        self.emailPassword = QLineEdit()
        self.emailServer = QLineEdit()
        self.emailPort = QLineEdit()

        self.Buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.Buttons.accepted.connect(self.prompt)
        self.Buttons.rejected.connect(self.reject)

        self.Layout = QFormLayout()
        self.Layout.addRow(QLabel("Email Address")  , self.emailAddress  )
        self.Layout.addRow(QLabel("Email Password") , self.emailPassword )
        self.Layout.addRow(QLabel("SMTP Server")    , self.emailServer   )
        self.Layout.addRow(QLabel("SMTP Port")      , self.emailPort     )
        self.Layout.addRow(self.Buttons)
        self.setLayout(self.Layout)

        self.resize(300, 200)
        self.center()
        self.setWindowTitle('Email Settings')
        
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
            Log().write(f"[EMAIL CONFIGUARTION] -> Modified")
        else:
            Log().write(f"[EMAIL CONFIGUARTION] -> Not Saved")
            
    def modify_config_files(self):
        config = ConfigParser()
        config.read('./config.ini')
        config.set('MAIL', 'Address', self.emailAddress.text())
        config.set('MAIL', 'Password', self.emailPassword.text())
        config.set('MAIL', 'SMTP_Server', self.emailServer.text())
        config.set('MAIL', 'SMTP_Port', self.emailPort.text())
        with open('./config.ini', 'w') as configfile:
            config.write(configfile)
        
        QMessageBox.information(None, 'Configuration Saved', 'Email Settings has been saved!', QMessageBox.StandardButton.Ok)
        # self.initLogging(f"{host_port} [NEW CONNECTION] -> Client")
        self.close()

    def send(self, receiver_email: str = 'kiran@@crystallogic.co.za', message: str = "Backup Completed"):
        port = Config()['MAIL']['smtp_port']
        smtp_server = Config()['MAIL']['smtp_server']
        sender_email = Config()['MAIL']['address']
        password = Config()['MAIL']['password']
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        Log().write(f"[EMAIL SENT] -> {receiver_email}")