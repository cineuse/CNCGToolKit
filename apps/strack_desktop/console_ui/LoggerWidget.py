# coding=utf8
# Copyright (c) 2016 CineUse

from Qt import QtWidgets


class LoggerWidget(QtWidgets.QPlainTextEdit):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(LoggerWidget, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, parent=None):
        # only initialize at first time
        if self.__initialized:
            return
        self.__initialized = True

        # do init
        super(LoggerWidget, self).__init__(parent)

        self.setReadOnly(True)


if __name__ == "__main__":
    LoggerWidget()
