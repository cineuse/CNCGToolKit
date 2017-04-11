# coding=utf8
# Copyright (c) 2016 CineUse
import sys
import logging

import cgtk_qt
from Qt import QtGui

from main_ui import MainUI
from strack_tray import StrackTrayIcon
from StrackLogin import StrackLogin

sys.path.insert(0, r"E:\repos\strack_python_api\src")

from strack import Strack


def authentication(login_info, logger=logging.getLogger("strack_connection")):
    # try connecting strack server
    try:
        strack_server = Strack(**login_info)
    except Exception, err:
        logger.error("login failed. Please check login info.")
        logger.error(err)
        # failed notification
        return "login failed. Please check login info."
    else:
        # init login
        StrackLogin(login_info.get("login"), strack_server)
        # start tray and mainUI
        app = QtGui.QApplication.instance()
        app.tray = cgtk_qt.render_gui(StrackTrayIcon, app=app)
        cgtk_qt.render_gui(GUIClass=MainUI, app=app, style="strack_main",
                           color_scheme="default", singleton=True)
