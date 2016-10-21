# coding=utf8

import os
import re
import cgtk_os
import Qt.QtGui as QtGui
import cgtk_qt
import cg_apps_rc

current_dir = os.path.dirname(__file__)
UI = os.path.join(current_dir, "actions.ui")
FormClass, BaseClass = cgtk_qt.load_ui_type(UI)


class ActionsUI(FormClass, BaseClass):
    def __init__(self, parent=None):
        super(ActionsUI, self).__init__(parent)

        # setup ui
        self.setupUi(self)
        # automatic scan apps
        self.update_apps()

    def update_apps(self):
        # todo: get from config or scan apps

        # update apps by scan
        cg_apps = self.list_cg_apps()
        # update the items
        self.actions_list.clear()
        for cg_app in cg_apps:
            # get icon
            app_name = cg_app.get("name")
            icon_path = ":/thumbnails/cg_apps/{app_name}.png".format(app_name=app_name.lower())
            icon = QtGui.QIcon(icon_path)
            app_item = QtGui.QListWidgetItem(icon, app_name)
            # todo: connect a launch with env slot
            self.actions_list.addItem(app_item)

    def list_cg_apps(self):
        all_cg_apps = []
        # get supported app list
        supported_app_list = ["Maya", "Nuke", "Mari", "Photoshop"]  # todo: should be getting from config
        # scan all apps
        all_installed_apps = cgtk_os.scan_installed_apps()
        # filter supported apps
        for app in all_installed_apps:
            for cg_app in supported_app_list:
                matched_info = re.match(r".*(%s.*) ([\d.]+)" % cg_app, app["display_name"])
                if matched_info:
                    app_name, app_version = matched_info.groups()
                    if app["path"]:
                        all_cg_apps.append({"name": app_name, "version": app_version, "path": app["path"]})
        return all_cg_apps


if __name__ == "__main__":
    pass
