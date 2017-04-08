# coding=utf8
# Copyright (c) 2017 Strack
import platform
import cgtk_yaml


class CGTKConfig(object):
    def __init__(self, yml_path):
        self.yml_path = yml_path
        self.__all_cfgs = cgtk_yaml.load_file(self.yml_path)

    def keys(self):
        return self.__all_cfgs.keys()

    def get(self, item):
        result = self.__all_cfgs.get(item)
        return self.format_result(result)

    def format_result(self, result):
        if isinstance(result, dict):
            for key, value in result.iteritems():
                if isinstance(value, dict):
                    result[key] = self.format_result(value)
            if set(result.keys()).issubset({"windows", "linux", "osx"}):
                result = result.get(platform.system().lower())
        return result
