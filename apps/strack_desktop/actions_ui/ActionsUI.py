# coding=utf8

import os
import re

import subprocess

import cgtk_os
import Qt.QtGui as QtGui
import Qt.QtCore as QtCore
import cgtk_qt
from actions_config import ActionConfig

import cg_apps_rc   # it is qt resources, do not remove this

current_dir = os.path.dirname(__file__)
UI = os.path.join(current_dir, "actions.ui")
FormClass, BaseClass = cgtk_qt.load_ui_type(UI)


class ActionsUI(FormClass, BaseClass):
    def __init__(self, parent=None):
        super(ActionsUI, self).__init__(parent)

        # get action config
        self.action_cfg = ActionConfig()

        # setup ui
        self.setupUi(self)

        # update context combo box
        contexts = self.list_contexts()
        self.context_combo.addItems(contexts)

        # connections
        self.context_combo.currentIndexChanged[str].connect(self.update_actions)
        self.actions_list.itemDoubleClicked.connect(self.execute_item_command)

        # show actions
        self.update_actions(self.context_combo.currentText())

    def list_contexts(self):
        return self.action_cfg.keys()

    @staticmethod
    def execute_item_command(item):
        return item.execute()

    def update_actions(self, selected_context):
        # clear list
        self.actions_list.clear()

        # list actions
        selected_context_dict = self.action_cfg.get(selected_context)
        action_list = selected_context_dict.get("actions", [])
        for action_name in action_list:
            action_info = action_list.get(action_name)
            action_info.update(name=action_name)
            action_item = ActionItem(action_info)
            self.actions_list.addItem(action_item)


class ActionItem(QtGui.QListWidgetItem):

    def __init__(self, action_info):
        super(ActionItem, self).__init__()

        # set item attributes
        self.setText(action_info.get("name"))

        icon_dir = ":/thumbnails/cg_apps"  # fixme: get this from strack config
        icon_path = "%s/%s.png" % (icon_dir, action_info.get("icon"))
        icon = QtGui.QIcon(icon_path)
        self.setIcon(icon)

        self.command = action_info.get("command")

    def execute(self):
        print self.command
        self.thread = RunCommandTread(self.command)
        # thread.info_signal.connect(self.push_log)
        self.thread.start()


class RunCommandTread(QtCore.QThread):
    info_signal = QtCore.Signal(basestring)

    def __init__(self, command=None, parent=None):
        super(RunCommandTread, self).__init__(parent)
        self.command = command

        self.finished.connect(self.show_finish_info)

    def show_finish_info(self):
        self.info_signal.emit("<font color=#00FF00 size=4><b>All Done...</b></font>")

    def run(self):
        p = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            return_code = p.poll()
            if return_code == 0:
                break
            elif return_code == 1:
                command_info = "Task `%s` was terminated for some reason." % self.command
                self.info_signal.emit("<font color=#FF0000>%s</font>" % command_info)
                break
                # raise Exception(convert_error_info(command_info))
            elif return_code is not None:
                command_info = "exit return code is: %s" % str(return_code)
                self.info_signal.emit("<font color=#FF0000>%s</font>" % command_info)
                break
                # raise Exception(convert_error_info(command_info))
            line = p.stdout.readline()
            if line.strip():
                if line.startswith("Action error"):
                    self.info_signal.emit("<font color=#FF0000>%s</font>" % line)
                if line.startswith("Action warning"):
                    self.info_signal.emit("<font color=#F0E68C>%s</font>" % line)


if __name__ == "__main__":
    pass
