# coding=utf8
# Copyright (c) 2017 Strack
import os
import sys

import cgtk_qt
from LoggerWidget import LoggerWidget

current_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.dirname(current_dir))
UI = os.path.join(current_dir, "console.ui")
FormClass, BaseClass = cgtk_qt.load_ui_type(UI)


class ConsoleUI(FormClass, BaseClass):
    def __init__(self, parent=None):
        super(ConsoleUI, self).__init__(parent)

        # setup ui
        self.setupUi(self)

        # add widget to dialog
        self.logger_widget = LoggerWidget()
        self.log_layout.addWidget(self.logger_widget)

        # connections
        self.clear_btn.clicked.connect(self.logger_widget.clear)
