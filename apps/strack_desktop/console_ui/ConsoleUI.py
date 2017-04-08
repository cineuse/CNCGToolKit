# coding=utf8
# Copyright (c) 2017 Strack
import sys
import os
import logging

from Qt import QtGui

import cgtk_qt
from strack_log import StrackLogHandler

current_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.dirname(current_dir))
UI = os.path.join(current_dir, "console.ui")
FormClass, BaseClass = cgtk_qt.load_ui_type(UI)


class ConsoleUI(FormClass, BaseClass):
    def __init__(self, parent=None):
        super(ConsoleUI, self).__init__(parent)

        # setup ui
        self.setupUi(self)

        # make logger
        self.log_handler = StrackLogHandler()
        self.strack_log = logging.getLogger("strack").addHandler(self.log_handler)

        # add widget to dialog
        self.log_layout.addWidget(self.log_handler.widget)

        # connections

