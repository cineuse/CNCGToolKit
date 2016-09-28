# coding=utf8
# Copyright (c) 2016 CineUse

import os
import logging
import cgtk_log

log = cgtk_log.cgtk_log(level=logging.INFO)


def get_config_path(config_name="studio"):
    ext = "yml"
    config_dir = get_config_dir()
    config_file_name = "%s.%s" % (config_name, ext)
    config_path = os.path.join(config_dir, config_file_name)
    return config_path


def get_config_dir():
    current_dir = os.path.dirname(__file__)
    lib_dir = os.path.dirname(current_dir)
    pack_dir = os.path.dirname(lib_dir)
    conf_dir = os.path.join(pack_dir, "configs")
    return conf_dir

if __name__ == "__main__":
    get_config_path()
