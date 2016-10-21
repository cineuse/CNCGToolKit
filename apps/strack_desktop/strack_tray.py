# coding=utf8

import Qt.QtGui as QtGui
import Qt.QtCore as QtCore
import icons_rc

import cgtk_qt
import main_ui


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
        # todo: 重构为表驱动
        app = QtGui.QApplication.instance()
        action_list = []
        configAction = QtGui.QAction("&Config", self, triggered=self.call_configUI)
        helpAction = QtGui.QAction("&Help", self, triggered=self.call_helpUI)
        feedbackAction = QtGui.QAction("&FeedBack", self, triggered=self.call_feedbackUI)
        quitAction = QtGui.QAction("&Quit", self, triggered=app.quit)
        action_list.append(configAction)
        action_list.append(helpAction)
        action_list.append(feedbackAction)
        action_list.append(quitAction)
        return action_list

    def create_context_menu(self):
        actions = self.create_actions()
        self.trayIconMenu = QtGui.QMenu()
        self.trayIconMenu.addActions(actions)

    def iconActivated(self, reason):
        if reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick):
            self.call_mainUI()

    def call_mainUI(self):
        app = QtGui.QApplication.instance()
        self.main_window = cgtk_qt.render_gui(GUIClass=main_ui.MainUI, app=app, singleton=True)

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
