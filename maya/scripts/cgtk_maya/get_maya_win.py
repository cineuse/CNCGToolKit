#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/7/23'
# version     :
# usage       :
# notes       :

# Built-in modules

# Third-party modules
import maya.OpenMayaUI as mui

# Studio modules

# Local modules


def get_maya_win(module="mayaUI"):
    """
    get a QMainWindow Object of maya main window
    :param module (optional): string "PySide"(default) or "PyQt4"
    :return main_window: QWidget or QMainWindow object
    """
    prt = mui.MQtUtil.mainWindow()
    if module == "Qt":
        from Qt import QtCompat
        if "PyQt" in QtCompat.__binding__:
            import sip
            import PyQt4.QtCore as QtCore
            main_window = sip.wrapinstance(long(prt), QtCore.QObject)
        else:
            import shiboken
            import PySide.QtGui as QtGui
            main_window = shiboken.wrapInstance(long(prt), QtGui.QWidget)
    elif module == "PyQt4":
        import sip
        import PyQt4.QtCore as QtCore
        main_window = sip.wrapinstance(long(prt), QtCore.QObject)
    elif module == "PySide":
        import shiboken
        import PySide.QtGui as QtGui
        main_window = shiboken.wrapInstance(long(prt), QtGui.QWidget)
    elif module == "mayaUI":
        main_window = "MayaWindow"
    else:
        raise ValueError('param "module" must be "mayaUI" "PyQt4" or "PySide"')
    return main_window
