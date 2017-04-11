# coding=utf8
import logging

import Qt.QtGui as QtGui

import cgtk_qt
import main_ui
from pw_multiScriptEditor import scriptEditor


class StrackTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, parent=None):
        super(StrackTrayIcon, self).__init__(parent)

        strack_icon = QtGui.QIcon(':/icons/strack.png')
        self.setIcon(strack_icon)
        self.create_context_menu()
        self.setContextMenu(self.trayIconMenu)
        self.activated.connect(self.iconActivated)

        self.main_window = None
        self.config_window = None
        self.help_window = None
        self.feedback_window = None


    def create_actions(self):
        app = QtGui.QApplication.instance()

        ACTIONS_MAP = [
            ("Strack&Connection", self.call_mainUI),
            ("&ScriptEditor", self.call_script_editor),
            ("&Config", self.call_configUI),
            ("&Help", self.call_helpUI),
            ("&FeedBack", self.call_feedbackUI),
            ("&Quit", app.quit),
        ]

        action_list = []
        for label, command in ACTIONS_MAP:
            action_list.append(QtGui.QAction(label, self, triggered=command))

        return action_list

    def create_context_menu(self):
        actions = self.create_actions()
        self.trayIconMenu = QtGui.QMenu()
        self.trayIconMenu.addActions(actions)

    def iconActivated(self, reason):
        if reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick):
            self.call_mainUI()

    def call_script_editor(self):
        app = QtGui.QApplication.instance()
        cgtk_qt.render_gui(GUIClass=scriptEditor.scriptEditorClass, app=app, singleton=True)

    def call_mainUI(self):
        app = QtGui.QApplication.instance()
        self.main_window = cgtk_qt.render_gui(GUIClass=main_ui.MainUI, app=app, style="strack_main",
                                              color_scheme="default", singleton=True)

    def call_configUI(self):
        # todo: show config UI
        print "show config UI here..."

    def call_helpUI(self):
        # todo: show config UI
        print "show help UI here..."

    def call_feedbackUI(self):
        # todo: show config UI
        print "show feedback UI here..."


if __name__ == '__main__':
    cgtk_qt.render_gui(StrackTrayIcon)
