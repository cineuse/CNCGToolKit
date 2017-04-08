# coding=utf8
import os
from CGTKConfig import CGTKConfig


def get_studio_cfg_path():
    root_path = os.path.join(os.path.dirname(__file__), "../../", "configs", "studio.yml")
    return root_path


def StudioConfig():
    studio_yml_path = get_studio_cfg_path()
    return CGTKConfig(studio_yml_path)

if __name__ == "__main__":
    studio_cfg = StudioConfig()
    print studio_cfg.get("deadline")
    print studio_cfg.get("python")
