#!/usr/bin/env python3  

__author__ = 'Amir Debram'
__version__ = '1.0'
__email__ = 'amirdebram@gmail.com'

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import (
    QDialog, QTextBrowser,
    QHBoxLayout, QVBoxLayout,
    QDialogButtonBox,
    QComboBox, QSpinBox
    )

from datetime import date

today = date.today()

d2 = today.strftime("%B %d, %Y")

class LogDialog(QDialog):
    def __init__(self, parent=None):
        super(LogDialog, self).__init__(parent)

        self.initUI()

    def initUI(self):
        
        self._date = QSpinBox()
        self._date.setRange(1, 31)
        self._date.setValue(int(today.strftime("%d")))
        self._date.valueChanged.connect(lambda: self.change())

        self._month = QComboBox()
        self._month.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        self._month.addItems([
            'January', 'February', 'March', 
            'April', 'May', 'June', 
            'July', 'August', 'September', 
            'October', 'November', 'December'])
        self._month.setCurrentIndex(int(today.strftime("%m"))-1)
        self._month.currentIndexChanged.connect(lambda: self.change())

        self._year = QSpinBox()
        self._year.setRange(2022, 2052)
        self._year.setValue(int(today.strftime("%Y")))
        self._year.valueChanged.connect(lambda: self.change())
        
        self.TextBrowser = QTextBrowser()
        try:
            text = open(f"./Logs/{self._year.value()} {self._month.currentText()} {self._date.value():02d}.log").read()
        except FileNotFoundError:
            text = ''
        self.TextBrowser.setPlainText(text)

        self.Buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.Buttons.accepted.connect(self.close)
        
        self.dateLayout = QHBoxLayout()
        self.dateLayout.addWidget(self._date)
        self.dateLayout.addWidget(self._month)
        self.dateLayout.addWidget(self._year)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.dateLayout)
        self.mainLayout.addWidget(self.TextBrowser)
        self.mainLayout.addWidget(self.Buttons)
                
        self.setLayout(self.mainLayout)

        self.resize(600, 600)
        self.center()
        self.setWindowTitle('View Logs')

    def change(self):
        try:
            text = open(f"./Logs/{self._year.value()} {self._month.currentText()} {self._date.value():02d}.log").read()
        except FileNotFoundError:
            text = ''
        self.TextBrowser.setPlainText(text)

    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())