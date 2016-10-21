# coding=utf8

import _winreg


def scan_installed_apps():
    """
    scan installed apps in windows system
    :return:
    """
    apps_list = []
    for key_root in [_winreg.HKEY_CURRENT_USER, _winreg.HKEY_LOCAL_MACHINE]:
        for key_path in ["SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
                         "SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall"]:
            try:
                key = _winreg.OpenKey(key_root, key_path)
                # list all installed Apps
                i = 0
                while True:
                    app = {}
                    sub_key_name = _winreg.EnumKey(key, i)
                    sub_key = _winreg.OpenKey(key, sub_key_name)
                    try:
                        app["display_name"] = _winreg.QueryValueEx(sub_key, "DisplayName")[0]
                        app["path"] = _winreg.QueryValueEx(sub_key, "InstallLocation")[0]
                        apps_list.append(app)
                    except WindowsError:
                        pass
                    i += 1
            except WindowsError:
                pass
    return apps_list


if __name__ == "__main__":
    pass
