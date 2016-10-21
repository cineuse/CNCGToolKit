# coding=utf8

import logging
import os
import sys
import Qt.QtGui as QtGui
import Qt.QtCore as QtCore
import cgtk_qt
import cgtk_py

current_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.dirname(current_dir))

from actions_ui import ActionsUI
from mytasks_ui import MyTasksUI
from publish_ui import PublishUI
from chat_ui import ChatUI


UI = os.path.join(current_dir, "main.ui")
FormClass, BaseClass = cgtk_qt.load_ui_type(UI)


class MainUI(FormClass, BaseClass):

    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)

        # setup ui
        self.setupUi(self)

        # hide title bar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # add a size grip
        size_grip = QtGui.QSizeGrip(self)
        self.sizegrip_layout.addWidget(size_grip, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        # shadow effect
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QtGui.QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setOffset(0, 0)
        self.main_frame.setGraphicsEffect(self.shadow)

        # enable drag and move
        self.title_bar_grp.last_clicked_pos = self.user_info_grp.last_clicked_pos = None
        self.title_bar_grp.main_dialog = self.user_info_grp.main_dialog = self
        cgtk_py.implant_method(self.title_bar_grp, mousePressEvent, "mousePressEvent")
        cgtk_py.implant_method(self.title_bar_grp, mouseMoveEvent, "mouseMoveEvent")
        cgtk_py.implant_method(self.title_bar_grp, mouseReleaseEvent, "mouseReleaseEvent")
        cgtk_py.implant_method(self.user_info_grp, mousePressEvent, "mousePressEvent")
        cgtk_py.implant_method(self.user_info_grp, mouseMoveEvent, "mouseMoveEvent")
        cgtk_py.implant_method(self.user_info_grp, mouseReleaseEvent, "mouseReleaseEvent")

        # make tab button radio
        self.tab_btn_grp = QtGui.QButtonGroup()
        self.tab_btn_grp.addButton(self.action_btn)
        self.tab_btn_grp.addButton(self.task_btn)
        self.tab_btn_grp.addButton(self.publish_btn)
        self.tab_btn_grp.addButton(self.chat_btn)
        self.tab_btn_grp.setExclusive(True)

        # add pages
        # self.action_page = ActionsUI()
        # self.action_layout.addWidget(self.action_page)

        # change tab page
        # self.tab_btn_grp.buttonClicked.connect(self.tab_change)

    def tab_change(self):
        page_dict = {"action_btn": 0,
                     "task_btn": 1,
                     "publish_btn": 2,
                     "chat_btn": 3}
        sender = self.tab_btn_grp.checkedButton()
        page_index = page_dict.get(sender.objectName())
        self.work_stack.setCurrentIndex(page_index)


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
    cgtk_qt.render_gui(MainUI)
