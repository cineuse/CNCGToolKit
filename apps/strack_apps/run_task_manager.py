# coding=utf8
# Copyright (c) 2016 CineUse

from Qt import QtGui
import logging
import cgtk_log
import TaskManager

log = cgtk_log.cgtk_log(level=logging.INFO)


def run_task_manager():
    pass


if __name__ == "__main__":
    app = QtGui.QApplication([])
    win = TaskManager.TaskManager()
    win.show()

    app.exec_()
