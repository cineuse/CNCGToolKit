# coding=utf8
# Copyright (c) 2016 CineUse

import Qt.QtGui as QtGui
import Qt.QtCore as QtCore
import logging
import cgtk_log

log = cgtk_log.cgtk_log(level=logging.INFO)


class Node(object):
    def __init__(self, name, parent=None):
        self._name = name
        self._children = list()
        self._parent = parent
        if parent:
            parent.addChild(self)

    def addChild(self, child):
        self._children.append(child)

    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def child(self, row):
        return self._children[row]

    def children(self):
        return self._children

    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent:
            return self._parent._children.index(self)

    def isValid(self):
        return False

    def clear(self):
        self._children = list()

    def find(self, name):
        for i in self._children:
            if i.name() == name:
                return i


class ParentNode(Node):
    def __init__(self, strack_node, parent=None):
        self.st_task_node = strack_node
        name = self.st_task_node.get("name")
        super(ParentNode, self).__init__(name, parent)

    @property
    def node_type(self):
        return "parent"


class EntityNode(Node):
    def __init__(self, strack_node, parent=None):
        self.st_task_node = strack_node
        name = self.st_task_node.get("name")
        super(EntityNode, self).__init__(name, parent)

    @property
    def node_type(self):
        return "entity"


class TaskNode(Node):
    def __init__(self, strack_node, parent=None):
        self.st_task_node = strack_node
        name = self.st_task_node.get("name")
        super(TaskNode, self).__init__(name, parent)
        # todo: get info via a strack node
        self.people = "XX"
        self.status = self.st_task_node.get("status")
        self.date = "2016-10-14"
        self.description = "great work!"

    @property
    def long_name(self):
        """ this attribute is created for filter"""
        entity = self.parent()
        parent = entity.parent()
        parent_name = parent.name()
        entity_name = entity.name()
        task_name = self.name()
        return "%s_%s_%s" % (parent_name, entity_name, task_name)

    @property
    def node_type(self):
        return "task"


class TaskTreeModel(QtCore.QAbstractItemModel):
    def __init__(self, root_node=None, parent=None):
        super(TaskTreeModel, self).__init__(parent)
        self.__root_node = root_node

    def clear(self):
        self.__root_node.clear()
        self.reset()

    @property
    def root_node(self):
        return self.__root_node

    @root_node.setter
    def root_node(self, value):
        if isinstance(value, Node):
            self.__root_node = value
            self.reset()

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self.root_node

    def rowCount(self, parent):
        parent_node = self.getNode(parent)
        return parent_node.childCount()

    def columnCount(self, parent):
        return 2

    def data(self, index, role):
        if not index.isValid():
            return
        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                return node.name()
            if index.column() == 1 and node.node_type == "task":
                return node.status
            if index.column() == 2 and node.node_type == "task":
                # this hided column is for filtering
                return node.long_name

    def headerData(self, section, orientation, role):
        header_list = ["name", "status"]
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return header_list[section]

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def parent(self, index):
        node = self.getNode(index)
        parent_node = node.parent()
        if parent_node == self.root_node:
            return QtCore.QModelIndex()
        return self.createIndex(parent_node.row(), 0, parent_node)

    def index(self, row, column, parent):
        parent_node = self.getNode(parent)
        child_item = parent_node.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QtCore.QModelIndex()


class TaskFilterProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self):
        super(TaskFilterProxyModel, self).__init__()
        self.setDynamicSortFilter(True)
        self.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.unfinished_only = False

    def filterAcceptsRow(self, row_num, source_parent):
        ''' Overriding the parent function '''
        # Check if the current row matches
        if self.filter_accepts_row_itself(row_num, source_parent):
            return True

        # Traverse up all the way to root and check if any of them match
        if self.filter_accepts_any_parent(source_parent):
            return True

        # Finally, check if any of the children match
        return self.has_accepted_children(row_num, source_parent)

    def filter_accepts_row_itself(self, row_num, parent):
        status_index = self.sourceModel().index(row_num, 1, parent)
        filter_result = super(TaskFilterProxyModel, self).filterAcceptsRow(row_num, parent)
        if self.unfinished_only:
            unfinished = self.sourceModel().data(status_index, QtCore.Qt.DisplayRole) != "approved"
            return filter_result and unfinished
        else:
            return filter_result

    def filter_accepts_any_parent(self, parent):
        ''' Traverse to the root node and check if any of the
            ancestors match the filter
        '''
        while parent.isValid():
            if self.filter_accepts_row_itself(parent.row(), parent.parent()):
                return True
            parent = parent.parent()
        return False

    def has_accepted_children(self, row_num, parent):
        ''' Starting from the current node as root, traverse all
            the descendants and test if any of the children match
        '''
        model = self.sourceModel()
        source_index = model.index(row_num, 0, parent)
        children_count = model.rowCount(source_index)
        for i in xrange(children_count):
            if self.filterAcceptsRow(i, source_index):
                return True
        return False


if __name__ == "__main__":
    TaskTreeModel()
