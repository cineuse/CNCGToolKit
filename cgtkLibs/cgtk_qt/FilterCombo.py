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
    def __init__(self, parent=None):
        super(FilterCombo, self).__init__(parent)

        self.__item_list = []
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setEditable(True)
        self.completer = QtGui.QCompleter(self)

        # always show all completions
        self.completer.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
        self.pFilterModel = QtGui.QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)

        # set models
        self.model = QtGui.QStandardItemModel()
        super(FilterCombo, self).setModel(self.model)
        self.pFilterModel.setSourceModel(self.model)
        self.completer.setModel(self.pFilterModel)
        self.setModelColumn(0)

        self.completer.setPopup(self.view())
        self.setCompleter(self.completer)

        # connections
        self.lineEdit().textEdited[unicode].connect(self.pFilterModel.setFilterFixedString)
        self.lineEdit().editingFinished.connect(self.edit_done)
        self.completer.activated.connect(self.setTextIfCompleterIsClicked)


    @property
    def item_list(self):
        return self.__item_list

    @item_list.setter
    def item_list(self, value):
        if type(value) not in [list, tuple]:
            value = [value]
        self.__item_list = value
        # setup model
        self.model.clear()
        for i, word in enumerate(self.item_list):
            item = QtGui.QStandardItem(word)
            self.model.setItem(i, 0, item)
        self.setCurrentIndex(0)

    @QtCore.Slot()
    def edit_done(self):
        text = self.lineEdit().text()
        if text not in self.__item_list:
            # select first matched item or first item
            text = self.pFilterModel.data(self.pFilterModel.index(0, 0))
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
        else:
            self.setCurrentIndex(0)
        # delete unmatched text
        self.model.removeRows(len(self.item_list), 9999)

    def set_current_text(self, text):
        if text in self.__item_list:
            index = self.findText(text)
            self.setCurrentIndex(index)

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
    combo = FilterCombo()
    combo.item_list = my_item_list

    combo.show()

    sys.exit(app.exec_())
