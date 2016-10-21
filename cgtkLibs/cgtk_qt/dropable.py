# coding=utf8
# Copyright (c) 2016 CineUse

import Qt.QtGui as QtGui
import Qt.QtCore as QtCore
from Qt import QtCompat
import logging
import cgtk_log

log = cgtk_log.cgtk_log(level=logging.INFO)


if "PySide" not in QtCompat.__binding__:
    QtCore.Signal = QtCore.pyqtSignal


def dropable(widget):
    class Filter(QtCore.QObject):
        drop_in = QtCore.Signal(list)

        def eventFilter(self, obj, event):

            if obj == widget:
                if event.type() in [QtCore.QEvent.DragEnter, QtCore.QEvent.DragMove]:
                    if event.mimeData().hasUrls():
                        event.acceptProposedAction()
                        return True
                    else:
                        event.ignore()
                        return False
                if event.type() == QtCore.QEvent.Drop:
                    in_paths = []
                    for url in event.mimeData().urls():
                        path = url.toLocalFile()
                        in_paths.append(path)
                    self.drop_in.emit(in_paths)
                    return True
            return False

    if hasattr(widget, "setAcceptDrops"):
        widget.setAcceptDrops(True)
    obj = Filter(widget)
    widget.installEventFilter(obj)
    return obj.drop_in


if __name__ == "__main__":
    import sys
    from setup_ui import setup_ui

    class TestWidget(QtGui.QDialog):
        """Load .ui file example, using setattr/getattr approach"""
        def __init__(self, parent=None):
            QtGui.QDialog.__init__(self, parent)
            self.base_instance = setup_ui("E:/CodeTest/new_shelf_btn.ui", self)
            dropped = dropable(self.code_edit)
            dropped.connect(self.on_drop)

        def on_drop(self, files):
            print files

    app = QtGui.QApplication(sys.argv)
    wgt = TestWidget()

    wgt.show()
    app.exec_()
