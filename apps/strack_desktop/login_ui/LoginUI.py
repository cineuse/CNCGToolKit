# coding=utf8
# Copyright (c) 2016 CineUse

import os
import sys

import Qt.QtCore as QtCore
import Qt.QtGui as QtGui
import Qt.QtGui as QtWidgets

import cgtk_py
import cgtk_qt

current_dir = os.path.dirname(__file__)

UI = os.path.join(current_dir, "login.ui")
FormClass, BaseClass = cgtk_qt.load_ui_type(UI)


class LoginUI(FormClass, BaseClass):
    def __init__(self, parent=None):
        super(LoginUI, self).__init__(parent)

        # setup ui
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        # hide title bar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # shadow effect
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 0)
        self.main_frame.setGraphicsEffect(shadow)
        # enable drag and move
        self.title_bar_grp.last_clicked_pos = self.user_info_grp.last_clicked_pos = None
        self.title_bar_grp.main_dialog = self.user_info_grp.main_dialog = self
        cgtk_py.implant_method(self.title_bar_grp, mousePressEvent, "mousePressEvent")
        cgtk_py.implant_method(self.title_bar_grp, mouseMoveEvent, "mouseMoveEvent")
        cgtk_py.implant_method(self.title_bar_grp, mouseReleaseEvent, "mouseReleaseEvent")
        cgtk_py.implant_method(self.user_info_grp, mousePressEvent, "mousePressEvent")
        cgtk_py.implant_method(self.user_info_grp, mouseMoveEvent, "mouseMoveEvent")
        cgtk_py.implant_method(self.user_info_grp, mouseReleaseEvent, "mouseReleaseEvent")


def mousePressEvent(obj, event):
    super(obj.__class__, obj).mousePressEvent(event)
    obj.last_clicked_pos = (event.globalPos(), QtCore.QPoint(obj.main_dialog.pos()))


def mouseMoveEvent(obj, event):
    if obj.last_clicked_pos:
        move, begin = obj.last_clicked_pos
        obj.main_dialog.move((event.globalPos() - move) + begin)
    else:
        super(obj.__class__, obj).mouseMoveEvent(event)


def mouseReleaseEvent(obj, event):
    super(obj.__class__, obj).mouseReleaseEvent(event)
    obj.last_clicked_pos = None


if __name__ == "__main__":
    cgtk_qt.render_gui(LoginUI, style="strack_main", singleton=True)
    # app = QtGui.QApplication([])
    # dlg = LoginUI()
    # dlg.show()
    # app.exec_()
