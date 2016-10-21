# coding=utf8
# Copyright (c) 2016 CineUse

import sys
import Qt.QtGui as QtGui
import Qt.QtCore as QtCore
from Qt import QtCompat
import logging
import cgtk_log

log = cgtk_log.cgtk_log(level=logging.INFO)

if "PySide" not in QtCompat.__binding__:
    QtCore.Slot = QtCore.pyqtSlot


class FilterLineEdit(QtGui.QLineEdit):
    def __init__(self, parent=None):
        super(FilterLineEdit, self).__init__(parent)


if __name__ == "__main__":
    FilterLineEdit()
