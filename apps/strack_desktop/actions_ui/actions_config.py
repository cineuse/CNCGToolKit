# coding=utf8
# Copyright (c) 2017 Strack

import os
from cgtk_config.CGTKConfig import CGTKConfig


def get_cfg_path():
    root_path = os.environ.get("strack_action_config_path", "d:/context_actions.yml")      # get from env fixme: default path should not be hard coded.
    return root_path


def ActionConfig():
    studio_yml_path = get_cfg_path()
    return CGTKConfig(studio_yml_path)


if __name__ == "__main__":
    action_cfg = ActionConfig()
    print action_cfg.get("")
    print action_cfg.get("")
