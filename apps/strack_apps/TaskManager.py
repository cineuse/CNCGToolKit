# coding=utf8
# Copyright (c) 2016 CineUse

import os
import logging
import Qt.QtGui as QtGui
import Qt.QtCore as QtCore
import cgtk_log
import cgtk_qt
from TaskTreeModel import TaskTreeModel, TaskFilterProxyModel, TaskNode, EntityNode, ParentNode, Node

log = cgtk_log.cgtk_log(level=logging.INFO)

UI = os.path.join(os.environ.get("CGTKUIPATH"), "task_manager.ui")
FormClass, BaseClass = cgtk_qt.load_ui_type(UI)


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
        # init combo data
        # fixme: get data via functions
        self.project_combo.item_list = ["bigBunny", "god", "hello"]
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
        self.project_combo.currentIndexChanged.connect(self.on_combo_index_changed)
        self.area_combo.currentIndexChanged.connect(self.update_task_tree)

        # update combos when task selected
        self.task_tree.clicked.connect(self.on_task_selected)

        # filter
        self.task_filter_edit.textChanged.connect(self.on_task_filter)
        self.my_task_check.clicked.connect(self.on_task_filter)
        self.unfinished_check.clicked.connect(self.on_task_filter)

        # set default data
        self.update_combo_model(self.area_combo)
        self.update_task_tree()

    @property
    def project(self):
        return self.project_combo.currentText()

    @property
    def area(self):
        return self.area_combo.currentText()

    def update_task_tree(self):
        self.task_model.clear()
        # fixme: get tasks
        tasks = TEST_TASKS[self.area]
        my_tasks_only = self.my_task_check.isChecked()
        if my_tasks_only:
            # tasks = strack_server.task.select(filter="assignee=%s" % strack_server.login)
            pass
        else:
            # tasks = strack_server.task.select()
            pass
        # todo: get entities and parents
        for task in tasks:
            entity = task.get("entity")
            parent = entity.get("parent")
            parent_node = self.task_model.root_node.find(parent)
            if parent_node:
                entity_node = parent_node.find(entity)
                if not entity_node:
                    entity_node = EntityNode(entity, parent_node)
            else:
                parent_node = ParentNode(parent, self.task_model.root_node)
                entity_node = EntityNode(entity, parent_node)

            TaskNode(task, entity_node)
        self.task_model.reset()
        self.task_tree.expandAll()

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
        # set combos
        self.set_combo("parent_combo", parent_name)
        self.set_combo("entity_combo", entity_name)
        self.set_combo("task_combo", task_name)

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
        self.proxy_model.setFilterKeyColumn(2)
        self.proxy_model.setFilterRegExp(name)
        self.task_tree.expandAll()

    def on_combo_index_changed(self):
        combo = self.sender()
        self.update_combo_model(combo)

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

    def __get_parent_items(self, project, area):
        # todo: get sequences or asset types via api
        if project and area:
            if area == "Asset":
                return ["Character", "Prop", "Environment"]  # fixme: get from strack
            else:
                # seq_list = strack_server.sequence.select("project=project")
                # return [i.get("name") for i in seq_list]
                return sorted(list(set([i["entity"]["parent"]["name"] for i in TEST_TASKS["Shot"]])))

    def __get_entity_items(self, project, area, parent):
        # todo: get shots via api
        if project and area and parent:
            if area == "Asset":
                # return strack_server.Asset.select("project=project and category=parent")
                return sorted(list(set([i["entity"]["name"] for i in TEST_TASKS["Asset"]])))
            else:
                # return strack_server.Shot.select("project=project and sequence=parent")
                return sorted(list(set([i["entity"]["name"] for i in TEST_TASKS["Shot"]])))

    def __get_task_items(self, project, area, parent, entity):
        # todo： get tasks via api
        if project and area and parent and entity:
            if area == "Asset":
                # return strack_server.Asset.select("project=project and category=parent")
                return sorted(list(set([i["name"] for i in TEST_TASKS["Asset"] if
                                        i["entity"]["name"] == entity and i["entity"]["parent"]["name"] == parent])))
            else:
                # return strack_server.Shot.select("project=project and sequence=parent")
                return sorted(list(set([i["name"] for i in TEST_TASKS["Shot"] if
                                        i["entity"]["name"] == entity and i["entity"]["parent"]["name"] == parent])))

    def update_versions(self):
        # todo: get versions in version path or via api
        pass


# todo: delete this
TEST_TASKS = {
    "Shot": [
        {"entity": {"name": "001",
                    "parent": {"name": "001"}
                    },
         "name": "Anim",
         "status": "in progress"
         },
        {"entity": {"name": "002",
                    "parent": {"name": "001"}
                    },
         "name": "Light",
         "status": "approved"
         },
        {"entity": {"name": "001",
                    "parent": {"name": "002"}
                    },
         "name": "Layout",
         "status": "reviewing"
         },
        {"entity": {"name": "002",
                    "parent": {"name": "002"}
                    },
         "name": "Anim",
         "status": "in progress"
         }
    ],
    "Asset": [
        {"entity": {"name": "Hero",
                    "parent": {"name": "Character"}
                    },
         "name": "Model",
         "status": "in progress"
         },
        {"entity": {"name": "Sword",
                    "parent": {"name": "Prop"}
                    },
         "name": "Rig",
         "status": "approved"
         },
    ]
}

if __name__ == "__main__":
    app = QtGui.QApplication([])
    win = TaskManager()
    win.show()
    # print win.project_combo.__class__

    app.exec_()
