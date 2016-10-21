# coding=utf8
# Copyright (c) 2016 CineUse

import os
import logging
import Qt.QtGui as QtGui
import Qt.QtCore as QtCore
import cgtk_log
import cgtk_qt
from .. import standalone_env

log = cgtk_log.cgtk_log(level=logging.INFO)

UI = os.path.join(os.environ.get("CGTKUIPATH"), "task_manager.ui")


class TaskManager(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(TaskManager, self).__init__(parent)
        cgtk_qt.setup_ui(UI, self)

        self.project_combo.item_list = ["bigBunny", "god", "hello"]
        self.entity_type_combo.item_list = ["Asset", "Shot"]
        self.parent_combo.item_list = ["001", "002", "003"]
        self.entity_combo.item_list = ["001", "002", "003", "004"]
        self.task_combo.item_list = ["layout", "anim", "light"]


if __name__ == "__main__":
    app = QtGui.QApplication([])
    win = TaskManager()
    win.show()
    # print win.project_combo.__class__

    import Qt
    ui = Qt.load_ui(UI)
    print ui.task_filter_edit
    print Qt.__file__

    app.exec_()
