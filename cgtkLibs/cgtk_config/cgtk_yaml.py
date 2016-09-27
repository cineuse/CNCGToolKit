# coding=utf8
# Copyright (c) 2016 Strack
import os
import re
import yaml


def load(yml_str):
    cfg = yaml.load(yml_str)
    for include_file in cfg.get("includes", []):
        yml_file = _format_yml_path(include_file)
        _update_configs(cfg, load_file(yml_file))
    return cfg


def load_file(yml_file):
    if os.path.isfile(yml_file):
        with open(yml_file) as f:
            return load(f.read())
    return []


def _format_yml_path(file_path):
    # todo: 目前只能处理环境变量，以后需要可以处理其它类型的配置
    # todo: 需要支持相对路径
    file_path = file_path.replace("\\", "/")
    env_vars = re.findall(r"\{env-(.+?)\}", file_path)
    for env_var in env_vars:
        replace_string = os.environ.get(env_var, "")
        replace_string = replace_string.replace("\\", "/")
        file_path = re.sub(r"\{env-%s\}" % env_var, replace_string, file_path)
    return file_path


def _update_configs(cfg_dict, new_dict):
    for key, value in new_dict.iteritems():
        if key not in cfg_dict:
            cfg_dict.update({key: value})


if __name__ == "__main__":
    print load_file(r"E:/repos/configs/studio.yml")
