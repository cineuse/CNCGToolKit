# coding=utf8
# Copyright (c) 2017 Strack

import os
import sys
import logging
import logging.handlers

from Qt import QtGui


class StrackLogHandler(logging.Handler):
    def __init__(self, log_format='%(asctime)s - %(name)s - %(filename)s:%(lineno)s - %(message)s', parent=None):
        super(StrackLogHandler, self).__init__()

        self.widget = None
        self.widget = QtGui.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

        formatter = logging.Formatter(log_format)
        self.setFormatter(formatter)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)
