# coding=utf8

import os
import Qt.QtGui as QtGui
import cgtk_qt

current_dir = os.path.dirname(__file__)
UI = os.path.join(current_dir, "chat.ui")
FormClass, BaseClass = cgtk_qt.load_ui_type(UI)


class ChatUI(FormClass, BaseClass):
    def __init__(self, parent=None):
        super(ChatUI, self).__init__(parent)
        # setup ui
        self.setupUi(self)

if __name__ == "__main__":
    cgtk_qt.render_gui(ChatUI)
