#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/9/21'
# version     :
# usage       :
# notes       :

# Built-in modules

# Third-party modules
import Qt.QtGui as QtGui
import Qt.QtCore as QtCore

# Studio modules

# Local modules


QtCore.QTextCodec.setCodecForLocale(QtCore.QTextCodec.codecForName("utf8"))

def progress_dialog(num, info="In Process..."):
    """

    :param num: range max
    :param info: shown information
    :return: QProgressDialog
    """
    progress_dialog = QtGui.QProgressDialog()
    progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
    progress_dialog.setMinimumDuration(5)
    progress_dialog.setWindowTitle(progress_dialog.tr("In Process..."))
    progress_dialog.setLabelText(progress_dialog.tr(info))
    progress_dialog.setCancelButtonText(progress_dialog.tr("Cancel"))
    progress_dialog.setRange(0, num)
    return progress_dialog


if __name__ == "__main__":
    import sys
    import time
    app = QtGui.QApplication(sys.argv)
    test_pd = progress_dialog(100)
    for i in range(101):
        test_pd.setValue(i)
        time.sleep(0.05)
    app.exec_()
