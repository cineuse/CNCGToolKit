# coding=utf8
# Copyright (c) 2016 Strack
import os
import yaml


def load_file(yml_file):
    if os.path.isfile(yml_file):
        with open(yml_file) as f:
            load(f.read())


def load(yml_str):
    cfg = yaml.load(yml_str)
    for inc in cfg.get("includes", []):
        cfg.update(yaml.load(open(inc)))


if __name__ == "__main__":
    pass
