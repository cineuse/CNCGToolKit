# coding=utf8
import os
import platform
import cgtk_yaml

PROJECT_ROOT_NAME = "CNCGToolKit"


def get_studio_cfg_path():
    root_path = os.path.join(os.path.dirname(__file__), "../../", "configs", "studio.yml")
    return root_path


def get(item):
    studio_yml_path = get_studio_cfg_path()
    all_cfgs = cgtk_yaml.load_file(studio_yml_path)
    result = all_cfgs.get(item)
    return format_result(result)


def format_result(result):
    if isinstance(result, dict):
        for key, value in result.iteritems():
            if isinstance(value, dict):
                result[key] = format_result(value)
        if set(result.keys()).issubset({"windows", "linux", "osx"}):
            result = result.get(platform.system().lower())
    return result


if __name__ == "__main__":
    print get("deadline")
    print get("python")
