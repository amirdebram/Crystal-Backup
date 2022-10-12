#!/usr/bin/env python3  

__author__ = 'Amir Debram'
__version__ = '1.0'
__email__ = 'amirdebram@gmail.com'

from PyQt6.QtWidgets import QMainWindow, QApplication, \
    QMenu, QPushButton, QMessageBox, QHBoxLayout, QVBoxLayout, QLabel, QWidget
from PyQt6.QtGui import QIcon, QAction, QGuiApplication, QFont
from PyQt6.QtCore import Qt, QSize

from socket import socket, gethostname, AF_INET, SOCK_STREAM, SOCK_DGRAM
# from multiprocessing import Process
from threading import Thread
# from shutil import copyfile

from Modules.Backup import BackupDialog
from Modules.Email import EmailDialog
from Modules.Server import ServerDialog
from Modules.Log import LogDialog

from Libraries.Configuration import Config
from Libraries.Logging import Log
from Libraries.Copy import windowsCopy

class CrystalBackup(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        fileMenu = self.menuBar().addMenu('&File')
        editMenu = self.menuBar().addMenu('&Edit')
        viewMenu = self.menuBar().addMenu('&View')
        helpMenu = self.menuBar().addMenu('&Help')

        # File Menu
        fileExit = QAction(QIcon('Exit.png'), '&Exit', self)
        fileExit.setShortcut('Ctrl+Q')
        fileExit.setStatusTip('Exit application')
        fileExit.triggered.connect(QApplication.instance().quit)
        fileMenu.addAction(fileExit)

        # Edit Menu
        editSettings = QMenu('Settings', self)
        serverSetting = QAction(QIcon('Log.png'), '&Listening Server', self)
        serverSetting.setStatusTip('Lets you configure the files you want to have copied')
        serverSetting.triggered.connect(lambda: self.serversetting())
        emailSetting = QAction(QIcon('Log.png'), '&Email', self)
        emailSetting.setStatusTip('Lets you configure the emails settings')
        emailSetting.triggered.connect(lambda: self.emailsetting())
        editSettings.addAction(serverSetting)
        editSettings.addAction(emailSetting)
        editMenu.addMenu(editSettings)
 
        editBackup = QMenu('Backup', self)
        backupFiles = QAction(QIcon('Log.png'), '&Locations', self)
        backupFiles.setStatusTip('Lets you configure the files you want to have copied')
        backupFiles.triggered.connect(lambda: self.backupsetting())
        editBackup.addAction(backupFiles)
        editMenu.addMenu(editBackup)

        # View Menu
        filetransferLog = QAction(QIcon('Log.png'), '&Logs', self)
        filetransferLog.setStatusTip('Open\'s log file')
        filetransferLog.triggered.connect(lambda: self.logsetting())
        viewMenu.addAction(filetransferLog)

        # Help Menu
        helpAbout = QAction(QIcon('About.png'), '&About', self)
        helpAbout.setStatusTip('About Application')
        helpAbout.triggered.connect(lambda: self.about())
        helpMenu.addAction(helpAbout)

        self.backupLabel = QLabel("Status : \nClick to start Backup")
        self.backupLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.backupLabel.setFont(QFont("Times", 20))

        self.backupButton = QPushButton()
        self.backupButton.setIcon(QIcon("./res/Icons/crystal.png"))
        self.backupButton.setIconSize(QSize(100, 100))
        # self.backupButton.setStyleSheet("border-radius : 50; border : 2px solid black")
        self.backupButton.clicked.connect(self.initBackup)
        
        self.lableHLayout = QHBoxLayout()
        self.lableHLayout.addWidget(self.backupLabel)

        self.buttonHLayout = QHBoxLayout()
        self.buttonHLayout.addWidget(self.backupButton)   

        self.buttonLayout = QVBoxLayout()
        self.buttonLayout.addLayout(self.lableHLayout)
        self.buttonLayout.addLayout(self.buttonHLayout)

        self.layoutWidget = QWidget()
        self.layoutWidget.setLayout(self.buttonLayout)
        self.setCentralWidget(self.layoutWidget)
        
        self.statusBar()
        self.resize(500, 300)
        self.center()
        self.setWindowTitle('Crystal Backup')

    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def backupsetting(self):
        window = BackupDialog(self)
        Log().write(f"[BACKUP CONFIGUARTION] -> Clicked")
        # window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        try:
            window.remoteLineEdit.setText(Config()['PATH']['Remote'])
            window.localLineEdit.setText(Config()['PATH']['Local'])
        except KeyError:
            Config().generateConfiguration()
        window.show()

    def emailsetting(self):
        window = EmailDialog(self)
        Log().write(f"[EMAIL CONFIGUARTION] -> Clicked")
        # window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        try:
            window.emailAddress.setText(Config()['MAIL']['Address'])
            window.emailPassword.setText(Config()['MAIL']['Password'])
            window.emailServer.setText(Config()['MAIL']['SMTP_Server'])
            window.emailPort.setText(Config()['MAIL']['SMTP_Port'])
        except KeyError:
            Config().generateConfiguration()
        window.show()

    def serversetting(self):
        window = ServerDialog(self)
        Log().write(f"[SERVER CONFIGUARTION] -> Clicked")
        # window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        try:
            window.lsHost.setText(Config()['SERVER']['Host'])
            window.lsPort.setText(Config()['SERVER']['Port'])
        except KeyError:
            Config().generateConfiguration()
        window.show()

    def logsetting(self):
        window = LogDialog(self)
        window.show()

    def pathstr(self, path: str) -> str:
        return path.replace('\\\\', '//').replace('\\', '/').strip()

    def initBackup(self):
        Thread(target=self.start).start()

    def start(self):
        self.backupLabel.setText("Status : \nCompressing the backups\nPlease Wait..")
        self.backupButton.setEnabled(False)
        self.send(f"INITIATE, {Config()['PATH']['remote']}")
        Log().write(f"[ZIP] -> Completed")
        Log().write(f"[FILECOPY] -> Started")
        self.backupLabel.setText("Status : \nCopying the backups to destination\nPlease Wait..")
        windowsCopy.copy(self.remote_Location, self.destination)
        # copyfile(self.remote_Location, self.destination)
        Log().write(f"[FILECOPY] -> Finished")
        self.send("DISCONNECT")
        self.backupLabel.setText("Status : \nEmailing Backup Info\nPlease Wait..")
        for receiver_email in Config()['MAIL']['To'].split(' '):
            EmailDialog().send(receiver_email, self.message)
        self.backupLabel.setText("Status : \nClick to start Backup")
        self.backupButton.setEnabled(True)

    def send(self, msg: str):
        try:
            self.client = socket(AF_INET, SOCK_STREAM)
            self.client.connect((Config()['SERVER']['Host'], int(Config()['SERVER']['Port'])))
        except ConnectionRefusedError:
            QMessageBox.information(None, 'Connection Error', 'Backup Server is offline.', QMessageBox.StandardButton.Ok)
        encoding = 'utf-8'
        message = msg.encode(encoding)
        msg_length = len(message)
        send_length = str(msg_length).encode(encoding)
        send_length += b' ' * (64 - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        connected = True
        while connected:
            data = self.client.recv(2048).decode(encoding)
            if data == 'INITIATED':
                Log().write(f"[SERVER ZIP INITIATED] -> {Config()['PATH']['remote']}")
            else:
                response = data.split(',')
                if response[0] == 'COMPLETED':
                    connected = False
                    datasplit = response[1].strip().split(' | ')
                    self.remote_Location = datasplit[0].strip()
                    self.destination = Config()['PATH']['local'] + self.remote_Location.split('/')[-1]
                    datafiles = \
                        """\n""".join([x for x in datasplit])
                    self.message = \
                        f"""
                        {Config()['CUSTOMER']['Name']}
                        {Config()['CUSTOMER']['Branch']}
                        Device Name : {gethostname()}
                        Backup Device Location : {self.destination}
                        Backup Files:
                        {datafiles}
                        """

    def get_ipv4(self):
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return str(ip)

    def about(self):
        msg = f"""Crystal Backup.\n\
            \n>>> Connects to a deployed socket server that zips specific files and folders\
            which is then copied to a destination of your choosing.\n\
            \nVersion : {__version__}\
            \nCreated By : {__author__}\n\
            \nFor more information please contact:\
            \n{__author__} : {__email__}"""
        QMessageBox.information(None, 'About', msg, QMessageBox.StandardButton.Ok)

if __name__ == '__main__':
    from sys import argv, exit

    app = QApplication(argv)
    
    backupApp = CrystalBackup()
    backupApp.show()

    exit(app.exec())