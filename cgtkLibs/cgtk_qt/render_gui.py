# coding=utf8

import logging
import sys
import os
import Qt.QtGui as QtGui
import Qt.QtCore as QtCore
from load_style import load_style
from StrackColorScheme import StrackColorScheme

QSS_DIR = os.path.join(os.path.dirname(__file__), "styles")


def render_gui(GUIClass, app=None, style="default", singleton=True):
    # init event loop
    if not app:
        use_default_app = True
        app = QtGui.QApplication(sys.argv)
    else:
        use_default_app = False
    # init gui object
    gui_obj = GUIClass()
    # set stylesheet
    qss_name = r"%s/%s.qss" % (QSS_DIR, style)
    if not os.path.isfile(qss_name):
        qss_name = r"%s/%s.qss" % (QSS_DIR, "default")
    stylesheet = load_style(qss_name)
    if isinstance(gui_obj, QtGui.QWidget):
        gui_obj.setStyleSheet(stylesheet)
    # singleton
    if singleton:
        for widget in app.allWidgets():
            if gui_obj.objectName() == widget.objectName():
                widget.close()
    # set Color Scheme
    StrackColorScheme(baseColor=QtGui.QColor(50, 50, 50), highlightColor=QtGui.QColor(247, 147, 30), spread=2.5)
    # run gui
    gui_obj.show()
    # don't close after window closed
    QtGui.QApplication.setQuitOnLastWindowClosed(False)
    # run event loop
    if use_default_app:
        app.exec_()
    return gui_obj


if __name__ == "__main__":
    pass
