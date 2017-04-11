# coding=utf8
# Copyright (c) 2016 CineUse
import sys
import logging

from Qt import QtGui
from Qt import QtCore

import cgtk_qt
from authentication import authentication
from console_ui.strack_log import StrackLogHandler
from login_ui.LoginUI import LoginUI


def main():
    # get user config
    user_settings = QtCore.QSettings("StrackConnection", "StrackDesktop")
    # make logger
    logger = init_logger()
    # auto login
    error_message = auto_login(user_settings, logger)
    if not error_message:
        return
    # show login dialog
    app = QtGui.QApplication.instance()
    cgtk_qt.render_gui(LoginUI, app=app, style="strack_main", singleton=True)


def auto_login(user_settings, logger=logging.getLogger("strack_connection")):
    # get user settings

    # login directly if auto_login is True
    if user_settings.value("auto_login", "false") == "true":
        login_info = user_settings.value("login_info", None)
        return authentication(login_info, logger)
    return "auto login is off."


def init_logger(level="Debug"):
    LEVEL_MAP = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
    }

    logger = logging.getLogger("strack_connection")
    logger.setLevel(LEVEL_MAP.get(level.upper(), "INFO"))
    log_handler = StrackLogHandler()
    logger.addHandler(log_handler)
    return logger


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main()
    app.exec_()
