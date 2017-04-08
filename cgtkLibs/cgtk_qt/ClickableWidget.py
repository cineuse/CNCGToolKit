# coding=utf8
# Copyright (c) 2017 Strack
import Qt.QtGui as QtGui
import Qt.QtCore as QtCore
from Qt import QtCompat

if "PySide" not in QtCompat.__binding__:
    QtCore.Signal = QtCore.pyqtSignal


class ClickableWidget(QtGui.QWidget):
    leftClicked = QtCore.Signal()
    rightClicked = QtCore.Signal()
    leftDoubleClicked = QtCore.Signal()
    rightDoubleClicked = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(ClickableWidget, self).__init__(*args, **kwargs)
        self.__timer = QtCore.QTimer()
        self.__timer.setInterval(250)
        self.__timer.setSingleShot(True)
        self.__timer.timeout.connect(self.timeout)
        self.__left_click_count = self.__right_click_count = 0

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.__left_click_count += 1
            if not self.__timer.isActive():
                self.__timer.start()
        if event.button() == QtCore.Qt.RightButton:
            self.__right_click_count += 1
            if not self.__timer.isActive():
                self.__timer.start()

    def timeout(self):
        if self.__left_click_count >= self.__right_click_count:
            if self.__left_click_count == 1:
                self.leftClicked.emit()
            else:
                self.leftDoubleClicked.emit()
        else:
            if self.__right_click_count == 1:
                self.rightClicked.emit()
            else:
                self.rightDoubleClicked.emit()
        self.__left_click_count = self.__right_click_count = 0
