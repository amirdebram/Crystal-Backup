#!/usr/bin/env python3  

__author__ = 'Amir Debram'
__version__ = '1.0'
__email__ = 'amirdebram@gmail.com'

from os import path
import ctypes
from ctypes import wintypes, WinDLL, windll

WinDLL("shell32")
windll.LoadLibrary("shell32")

class _SHFILEOPSTRUCTW(ctypes.Structure):
    _fields_ = [("hwnd", wintypes.HWND),
                ("wFunc", wintypes.UINT),
                ("pFrom", wintypes.LPCWSTR),
                ("pTo", wintypes.LPCWSTR),
                ("fFlags", ctypes.c_uint),
                ("fAnyOperationsAborted", wintypes.BOOL),
                ("hNameMappings", ctypes.c_uint),
                ("lpszProgressTitle", wintypes.LPCWSTR)]

class windowsCopy():
    def __init__(self):
        super(_SHFILEOPSTRUCTW).__init__()

    def copy(src, dst):
        """
        :param str src: Source path to copy from. Must exist!
        :param str dst: Destination path to copy to. Will be created on demand.
        :return: Success of the operation. False means is was aborted!
        :rtype: bool
        """
        if not path.exists(src):
            print('No such source "%s"' % src)
            return False

        src_buffer = ctypes.create_unicode_buffer(src, len(src) + 2)
        dst_buffer = ctypes.create_unicode_buffer(dst, len(dst) + 2)

        fileop = _SHFILEOPSTRUCTW()
        fileop.hwnd = 0
        fileop.wFunc = 2  # FO_COPY
        fileop.pFrom = wintypes.LPCWSTR(ctypes.addressof(src_buffer))
        fileop.pTo = wintypes.LPCWSTR(ctypes.addressof(dst_buffer))
        fileop.fFlags = 512  # FOF_NOCONFIRMMKDIR
        fileop.fAnyOperationsAborted = 0
        fileop.hNameMappings = 0
        fileop.lpszProgressTitle = None

        result = ctypes.windll.shell32.SHFileOperationW(ctypes.byref(fileop))
        return not result