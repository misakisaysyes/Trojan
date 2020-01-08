#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import os.path
import win32api
import pythoncom
from win32com.shell import shell
from win32com.shell import shellcon

def createDesktopLnk(filename,lnkname):
    shortcut = pythoncom.CoCreateInstance(
        shell.CLSID_ShellLink, None,
        pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
    shortcut.SetPath(filename)
    if os.path.splitext(lnkname)[-1] != '.lnk':
        lnkname += ".lnk"
    # get desktop path
    desktopPath = shell.SHGetPathFromIDList(shell.SHGetSpecialFolderLocation(0,shellcon.CSIDL_DESKTOP))
    lnkname = os.path.join(desktopPath,lnkname)
    shortcut.QueryInterface(pythoncom.IID_IPersistFile).Save(lnkname,0)

if __name__ == '__main__':
    # get current directory
    path = pwd = os.getcwd()
    # create shotcut
    path = path+u'\weixin.exe'
    title = u'微信'
    type = sys.getfilesystemencoding()
    createDesktopLnk(path, title)
    # start this hook program
    win32api.ShellExecute(0, 'open', path, '', '', 1)
    print '创建快捷方式自启动完毕'
