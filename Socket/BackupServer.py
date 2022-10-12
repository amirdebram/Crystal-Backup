#!/usr/bin/env python3  

__author__ = 'Amir Debram'
__version__ = '1.0'
__email__ = 'amirdebram@gmail.com'

from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from os import path, stat, walk, mkdir
from zipfile import ZipFile, ZIP_DEFLATED
from threading import Thread, active_count
from datetime import datetime
from tkinter import messagebox
from Configuration import Config
from Logging import Log

class CrystalBackupServer:
    def __init__(self):
        super(CrystalBackupServer).__init__()

        self.Port_Number = int(Config()['SERVER']['Port'])

        if not self.checkPort(self.Port_Number):
            self.initServer(self.Port_Number)

        if not path.isdir(self.pathstr(Config()['PATH']['Local'])):
            mkdir(self.pathstr(Config()['PATH']['Local']))

    def pathstr(self, path: str) -> str:
        return path.replace('\\\\', '/').replace('\\', '/').strip()

    def initServer(self, port):
        ipaddress = self.get_ipv4()
        socketServer = socket(AF_INET, SOCK_STREAM)
        socketServer.bind((ipaddress, port))
        socketServer.listen()
        Log().write(f"{(ipaddress, port)} [LISTENING] -> Host")
        while True:
            self.connection, host_port = socketServer.accept()
            thread = Thread(target=self.handle_client, args=(host_port,))
            thread.start()
            Log().write(f"[ACTIVE CONNECTIONS] {active_count() - 1}")

    def handle_client(self, host_port):
        Log().write(f"{host_port} [NEW CONNECTION] -> Client")
        connected = True
        encoding = 'utf-8'
        while connected:
            try:
                msg_length = self.connection.recv(64).decode(encoding)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = self.connection.recv(msg_length).decode(encoding)
                    if msg == "DISCONNECT":
                        connected = False
                    print(f"[{host_port}] {msg}")
                    received = str(msg).split(',')
                    if str(msg).split(',')[0] == "INITIATE":
                        Folder_To_Archive = self.pathstr(received[1])
                        self.connection.send("INITIATED".encode("utf-8"))
                        Log().write(f"{host_port} [ZIP INITIATED] -> {Folder_To_Archive}")
                        self.checkFolder(Folder_To_Archive)
                    Log().write(f"{host_port} [ZIP COMPLETED] -> {self.return_value}")
                    self.connection.send(f"COMPLETED, {self.return_value}".encode("utf-8"))
            except:
                connected = False
                Log().write(f"{host_port} [CONNECTOPN FORCE DROP]")
            finally:
                Log().write(f"{host_port} [CONNECTOPN DROPED]")
        self.connection.close()
        
    def current_date(self):
        year = str(datetime.now().year)
        month = datetime.now().strftime('%B')
        day = datetime.now().strftime('%d')
        return " ".join([year, month, day])

    def checkPort(self, port: int) -> bool:
        with socket(AF_INET, SOCK_STREAM) as s:
            if s.connect_ex((self.get_ipv4(), port)) == 0:
                s.close()
                return True
            else:
                s.close()
                return False

    def get_ipv4(self):
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return str(ip)

    def checkFolder(self, Folder_To_Archive):
        File_Name = self.current_date()
        File_Type = ".zip"
        Output_File_Path = path.join(self.pathstr(Config()['PATH']['Local']), f'{File_Name}{File_Type}')
                
        if not path.isfile(Output_File_Path):
            self.zipFolder(Folder_To_Archive, Output_File_Path)
        else:
            i = 1
            while path.isfile(path.join(self.pathstr(Config()['PATH']['Local']), f'{File_Name} ({i}){File_Type}')):
                i += 1
            New_Output_File_Path = path.join(self.pathstr(Config()['PATH']['Local']), f'{File_Name} ({i}){File_Type}')
            self.zipFolder(Folder_To_Archive, New_Output_File_Path)

    def zipFolder(self, Folder_To_Archive, Output_File_Path):
        _files = str()
        with ZipFile(Output_File_Path, 'w') as archive_file:
            for dirpath, dirnames, filenames in walk(Folder_To_Archive):
                for filename in filenames:
                    for x in str(Config()['BACKUP']['Files']).split():
                        if x in filename:
                            file_path = self.pathstr(path.join(dirpath, filename))
                            archive_file_path = path.relpath(file_path, Folder_To_Archive)
                            _name = str(filename)
                            _size = str(round(stat(file_path).st_size / (1024 * 1024), 2))
                            _date_modified = str(datetime.fromtimestamp(path.getmtime(file_path)).strftime('%Y/%m/%d %H:%M'))
                            _files += ' | ' + " - ".join([file_path, _name, _size+'MB', _date_modified])
                            archive_file.write(file_path, archive_file_path, compress_type=ZIP_DEFLATED)
        self.return_value = ' '.join([self.pathstr(Output_File_Path), _files])
        return self.return_value

    def errorPort():
        msg = f"""The Port is currently in use.\nPlease use another."""
        messagebox.showerror("Error - Port", msg)

if __name__ == '__main__':
    CrystalBackupServer()