# coding=utf8
# Copyright (c) 2017 Strack

import logging
import logging.handlers

from LoggerWidget import LoggerWidget


class StrackLogHandler(logging.Handler):
    def __init__(self, log_format='%(asctime)s - %(name)s - %(filename)s:%(lineno)s - %(message)s', parent=None):
        super(StrackLogHandler, self).__init__()

        formatter = logging.Formatter(log_format)
        self.setFormatter(formatter)

    def emit(self, record):
        style_dict = {
            "DEBUG": "<font color=#00FFFF>%s</font>",
            "INFO": "<font color=#00FF00>%s</font>",
            "WARNING": "<font color=#F0E68C>%s</font>",
            "ERROR": "<font color=#FF0000>%s</font>",
        }
        msg = self.format(record)
        widget = LoggerWidget()
        widget.appendHtml(style_dict.get(record.levelname, "DEBUG") % msg)
