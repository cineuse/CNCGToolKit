# coding=utf8
# Copyright (c) 2016 CineUse

import sys
import Qt.QtGui as QtGui
import Qt.QtCore as QtCore
from Qt import QtCompat
import logging
import cgtk_log

log = cgtk_log.cgtk_log(level=logging.INFO)

if "PySide" not in QtCompat.__binding__:
    QtCore.Slot = QtCore.pyqtSlot


class FilterCombo(QtGui.QComboBox):
    def __init__(self, item_list, parent=None):
        super(FilterCombo, self).__init__(parent)

        self.item_list = item_list

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setEditable(True)
        self.completer = QtGui.QCompleter(self)

        # always show all completions
        self.completer.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
        self.pFilterModel = QtGui.QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)

        # set models
        self.source_model = QtGui.QStandardItemModel()
        for i, word in enumerate(self.item_list):
            item = QtGui.QStandardItem(word)
            self.source_model.setItem(i, 0, item)
        super(FilterCombo, self).setModel(self.source_model)
        self.pFilterModel.setSourceModel(self.source_model)
        self.completer.setModel(self.pFilterModel)
        self.setModelColumn(0)

        self.completer.setPopup(self.view())
        self.setCompleter(self.completer)

        # connections
        self.lineEdit().textEdited[unicode].connect(self.pFilterModel.setFilterFixedString)
        self.lineEdit().editingFinished.connect(self.edit_done)
        self.completer.activated.connect(self.setTextIfCompleterIsClicked)

        # select text
        self.lineEdit().selectAll()

    @QtCore.Slot()
    def edit_done(self):
        # select first matched item or first item
        matched_index = self.pFilterModel.mapToSource(self.pFilterModel.index(0, 0))
        if matched_index.row() >= len(self.item_list):
            self.setCurrentIndex(0)
        else:
            self.setCurrentIndex(matched_index.row())
        # delete unmatched text
        self.source_model.removeRows(len(self.item_list), 1)
        # select all text
        self.lineEdit().selectAll()

    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(FilterCombo, self).setModelColumn(column)

    def view(self):
        return self.completer.popup()

    def index(self):
        return self.currentIndex()

    def setTextIfCompleterIsClicked(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    my_item_list = ['hello', 'world', 'hi', 'babe', 'baby']
    combo = FilterCombo(my_item_list)

    combo.show()

    sys.exit(app.exec_())
