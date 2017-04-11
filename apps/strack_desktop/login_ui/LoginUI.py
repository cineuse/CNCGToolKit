# coding=utf8
# Copyright (c) 2016 CineUse

import logging
import os
import sys

import Qt.QtCore as QtCore
import Qt.QtGui as QtGui
import Qt.QtGui as QtWidgets

current_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.dirname(current_dir))
sys.path.insert(0, r"E:\repos\strack_python_api\src")

import cgtk_py
import cgtk_qt

from authentication import authentication
from console_ui.strack_log import StrackLogHandler

logger = logging.getLogger("strack_connection")

# temp
logger.setLevel(logging.DEBUG)
log_handler = StrackLogHandler()
logger.addHandler(log_handler)
# temp end

current_dir = os.path.dirname(__file__)

UI = os.path.join(current_dir, "login.ui")
FormClass, BaseClass = cgtk_qt.load_ui_type(UI)


class LoginUI(FormClass, BaseClass):
    def __init__(self, parent=None):
        super(LoginUI, self).__init__(parent)

        # setup ui
        self.setupUi(self)
        self.init_ui()

        # connections
        self.login_btn.clicked.connect(self.login)

    def init_ui(self):
        # set size
        self.title_bar_grp.setFixedWidth(450)
        self.body.setFixedHeight(200)
        self.main_layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        # hide default title bar
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

        # add a status bar
        self.status_bar = QtWidgets.QStatusBar()
        self.main_frame_layout.addWidget(self.status_bar)
        self.status_bar.hide()

    def login(self):
        login_info = {
            "base_url": self.url_line.text(),
            "login": self.name_line.text(),
            "api_key": self.key_line.text(),
        }

        logger.debug("login info:\n url %(base_url)s\n name %(login)s\n key %(api_key)s\n" % login_info)

        # do login
        error_message = authentication(login_info, logger)
        self.show_message(error_message, "error")
        if not error_message:
            # auto login setting
            self.set_auto_login(login_info)
            # close login ui
            self.close()

    def set_auto_login(self, login_info):
        # auto login
        user_settings = QtCore.QSettings("StrackConnection", "StrackDesktop")
        if self.autologin_check.isChecked():
            user_settings.setValue("auto_login", True)
            user_settings.setValue("login_info", login_info)
            logger.debug("auto login setup: %s" % login_info)
        else:
            user_settings.setValue("auto_login", False)

    def show_message(self, message, msg_type="info",  duration=3000):
        # set type style
        STYLE_MAP = {
            "info": "QStatusBar{ color: #fff; background-color: #20A0FF;}",
            "warning": "QStatusBar{ color: #fff; background-color: #F7BA2A;}",
            "error": "QStatusBar{ color: #fff; background-color: #FF4949;}",
        }
        self.status_bar.setStyleSheet(STYLE_MAP.get(msg_type, "info"))
        # show message
        self.status_bar.show()
        self.status_bar.showMessage(message, duration)
        # close when time up
        QtCore.QTimer.singleShot(duration, self.status_bar, QtCore.SLOT('hide()'))


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
