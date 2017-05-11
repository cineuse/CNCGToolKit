#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/9/28'
# version     :
# usage       :
# notes       :

# Built-in modules

# Third-party modules
import maya.OpenMayaUI as mui
import maya.cmds as cmds
import Qt.Core as QtCore
from Qt import QtCompat

if "PySide" in QtCompat.__binding__:
    import shiboken as prt
else:
    import sip as prt


# Studio modules

# Local modules


def qt_to_maya(qt_widget):
    layout = cmds.columnLayout(adjustableColumn=True)
    qt_obj = prt.wrapInstance(
        long(mui.MQtUtil.findLayout(layout)), QtCore.QObject)
    qt_obj.children()[0].layout().addWidget(qt_widget)
    cmds.setParent('..')
    return "layout|" + qt_widget.objectName()
