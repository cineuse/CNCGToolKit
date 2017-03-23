# coding=utf8
# Copyright (c) 2016 CineUse

import os
import logging
import Qt.QtGui as QtGui
import Qt.QtCore as QtCore
import itertools

import cgtk_log
import cgtk_qt
from TaskTreeModel import TaskTreeModel, TaskFilterProxyModel, TaskNode, EntityNode, ParentNode, Node

import sys

sys.path.append(r"D:\aaron\repos\strack_python_api\src\strack_api")
import strack
import strack_server_temp

log = cgtk_log.cgtk_log(level=logging.INFO)

# ------temp-------- #
# fixme: delete temp code
os.environ.setdefault("CGTKUIPATH", r"E:\repos\CNCGToolKit\uis")
# ------temp end ------ #
UI = os.path.join(os.environ.get("CGTKUIPATH"), "task_manager.ui")
FormClass, BaseClass = cgtk_qt.load_ui_type(UI)
strack_server = strack_server_temp.get_strack_server()


class TaskManager(FormClass, BaseClass):
    def __init__(self, parent=None):
        super(TaskManager, self).__init__(parent)
        self.setupUi(self)

        self.__combo_dict = {
            "project_combo": self.project_combo,
            "area_combo": self.area_combo,
            "parent_combo": self.parent_combo,
            "entity_combo": self.entity_combo,
            "task_combo": self.task_combo
        }
        self.current_page = 1

        self.task_appender = TaskAppender(self)

        # init combo data
        # fixme: get data via functions
        self.project_combo.item_list = self.all_projects()
        self.area_combo.item_list = ["Asset", "Shot"]  # always be this, hard coded

        # set tasks model
        self.task_model = TaskTreeModel(Node("task_root"), self)
        self.proxy_model = TaskFilterProxyModel()
        self.proxy_model.setSourceModel(self.task_model)
        self.task_tree.setModel(self.proxy_model)

        # update combos
        self.area_combo.currentIndexChanged.connect(self.on_combo_index_changed)
        self.parent_combo.currentIndexChanged.connect(self.on_combo_index_changed)
        self.entity_combo.currentIndexChanged.connect(self.on_combo_index_changed)

        # update versions
        self.task_combo.currentIndexChanged.connect(self.update_versions)

        # project and area combo effect task tree
        self.project_combo.currentIndexChanged.connect(self.update_task_tree)
        self.area_combo.currentIndexChanged.connect(self.update_task_tree)

        # append new items when scroll bar changed
        self.task_tree.verticalScrollBar().valueChanged.connect(self.on_taskview_scroll)
        self.task_appender.finished.connect(self.task_model.reset)
        self.task_appender.finished.connect(self.task_tree.expandAll)

        # update combos when task selected
        self.task_tree.clicked.connect(self.on_task_selected)

        # filter
        self.task_filter_edit.textChanged.connect(self.on_task_filter)
        self.my_task_check.clicked.connect(self.on_task_filter)
        self.unfinished_check.clicked.connect(self.on_task_filter)

        # set default data
        self.update_task_tree()

    def all_projects(self):
        project_nodes = strack_server.project.select()
        return [i.get("p_name") for i in project_nodes]

    @property
    def project(self):
        project_name = self.project_combo.currentText().lower()
        project_id = strack_server.project.find("p_name=%s" % project_name).get("id")
        return {
            "id": project_id,
            "name": project_name
        }

    @property
    def area(self):
        area_map = {
            "pre-production": 30,
            "asset": 40,
            "shot": 70
        }
        area_name = self.area_combo.currentText().lower()
        return {
            "id": area_map.get(area_name),
            "name": area_name
        }

    def set_combo(self, key, value):
        if key in self.__combo_dict:
            combo = self.__combo_dict[key]
            index = combo.findText(value)
            if index > -1:
                combo.setCurrentIndex(index)

    def on_task_selected(self, index):
        parent_name = entity_name = task_name = None
        # get selected task info
        src_index = self.proxy_model.mapToSource(index)
        selected_node = self.task_model.getNode(src_index)
        if selected_node.node_type == "parent":
            parent_name = selected_node.name()
        if selected_node.node_type == "entity":
            parent_node = selected_node.parent()
            parent_name = parent_node.name()
            entity_name = selected_node.name()
        if selected_node.node_type == "task":
            entity_node = selected_node.parent()
            parent_node = entity_node.parent()
            parent_name = parent_node.name()
            entity_name = entity_node.name()
            task_name = selected_node.name()
            # todo: set combos
            # self.set_combo("parent_combo", parent_name)
            # self.set_combo("entity_combo", entity_name)
            # self.set_combo("task_combo", task_name)

    def on_task_filter(self, name=None):
        if self.sender != self.task_filter_edit:
            name = self.task_filter_edit.text() or r"."  # filter edit changed the reg will be name, else it should be "."
        if self.my_task_check.isChecked():
            self.proxy_model.my_tasks_only = True
        else:
            self.proxy_model.my_tasks_only = False
        if self.unfinished_check.isChecked():
            self.proxy_model.unfinished_only = True
        else:
            self.proxy_model.unfinished_only = False
        self.proxy_model.setFilterKeyColumn(3)
        self.proxy_model.setFilterRegExp(name)
        self.task_tree.expandAll()

    def on_combo_index_changed(self):
        combo = self.sender()
        self.update_combo_model(combo)

    def on_taskview_scroll(self, value):
        scroll_bar = self.task_tree.verticalScrollBar()
        threshold = scroll_bar.maximum()*0.85
        if value > threshold:
            # make nodes
            # self.append_items()
            self.task_appender.start()

    def update_combo_model(self, combo):
        project = self.project_combo.currentText()
        area = self.area_combo.currentText()
        parent = self.parent_combo.currentText()
        entity = self.entity_combo.currentText()
        if combo.objectName() == "area_combo":
            self.parent_combo.item_list = self.__get_parent_items(project, area)
        elif combo.objectName() == "parent_combo":
            self.entity_combo.item_list = self.__get_entity_items(project, area, parent)
        elif combo.objectName() == "entity_combo":
            self.task_combo.item_list = self.__get_task_items(project, area, parent, entity)

    def update_task_tree(self):

        # clear all models
        self.task_model.clear()
        self.current_page = 1
        self.parent_combo.item_list = []
        self.entity_combo.item_list = []
        self.task_combo.item_list = []
        # parent key map
        # select items of project and area
        items = self.__next_page_items()
        # items = strack_server.item.select("p_id=%s and type=%s" % (project_id, area_id))
        length = strack_server.item.summary("item_id",
                                            "p_id=%s and type=%s" % (self.project.get("id"), self.area.get("id")),
                                            "count")
        self.__make_nodes(items)

    def __make_nodes(self, items):
        if self.area.get("name") == "asset":
            parent_key = "category"
        else:
            parent_key = "sequenceid"
        for item in items:
            tasks = strack_server.task.select("item_id=%s" % item.get("id"))
            first_task = next(tasks, None)
            if not first_task:
                continue
            tasks = itertools.chain([first_task], tasks)

            parent = item.get(parent_key) or "None"
            parent_node = self.task_model.root_node.find(parent)
            item_node = parent_node.find(item.get("item_name")) if parent_node else None
            if not parent_node:
                parent_node = ParentNode(parent, self.task_model.root_node)
                # self.parent_combo.item_list.append(parent_node.name())
            if not item_node:
                item_node = EntityNode(item, parent_node)
                # self.entity_combo.item_list.append(item_node.name())

            for task in tasks:
                task_node = TaskNode(task, item_node)
                # self.task_combo.item_list.append(task_node.name())

        self.task_model.reset()
        self.task_tree.expandAll()

    def append_items(self):
        new_items = self.__next_page_items()
        self.__make_nodes(new_items)

    def __next_page_items(self):
        items = strack_server.item.select("p_id=%s and type=%s" % (self.project.get("id"), self.area.get("id")),
                                          page=[{"pagenum": self.current_page, "pagesize": 20}])
        self.current_page += 1
        return items

    def update_versions(self):
        # todo: get versions in version path or via api
        pass


class TaskAppender(QtCore.QThread):
    def __init__(self, task_manager):
        super(TaskAppender, self).__init__()

        self.obj = task_manager

    def run(self):
        # print ">>>", self.obj.current_page
        # print "-->", self.obj.task_model.rowCount(self.obj.task_model.root_node)
        new_items = self.__next_page_items()
        self.__make_nodes(new_items)

    def __make_nodes(self, items):
        if self.obj.area.get("name") == "asset":
            parent_key = "category"
        else:
            parent_key = "sequenceid"
        for item in items:
            if not item:
                return False
            tasks = strack_server.task.select("item_id=%s" % item.get("id"))
            first_task = next(tasks, None)
            if not first_task:
                continue
            tasks = itertools.chain([first_task], tasks)

            parent = item.get(parent_key) or "None"
            parent_node = self.obj.task_model.root_node.find(parent)
            item_node = parent_node.find(item.get("item_name")) if parent_node else None
            if not parent_node:
                parent_node = ParentNode(parent, self.obj.task_model.root_node)
                # self.parent_combo.item_list.append(parent_node.name())
            if not item_node:
                item_node = EntityNode(item, parent_node)
                # self.entity_combo.item_list.append(item_node.name())

            for task in tasks:
                task_node = TaskNode(task, item_node)
                # self.task_combo.item_list.append(task_node.name())
        return True

    def __next_page_items(self):
        items = strack_server.item.select("p_id=%s and type=%s" % (self.obj.project.get("id"), self.obj.area.get("id")),
                                          page={"pagenum": self.obj.current_page, "pagesize": 20})
        self.obj.current_page += 1
        return items

if __name__ == "__main__":
    print "hello"
    app = QtGui.QApplication([])
    print app
    win = TaskManager()
    print win
    win.show()
    # print win.project_combo.__class__

    app.exec_()
