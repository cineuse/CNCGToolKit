#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : aas_libs_maya_globals
# description : ''
# author      : Aaron Hui
# date        : 2015/11/24
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import logging

# Third-party modules
from PySide import QtGui
# Studio modules

# Local modules


logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'sg_shotgunEvents_maya_globals_log.txt'),
                    level=logging.WARN, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')


class MayaGlobals(object):
    def __init__(self):
        self.__dict = dict()

    def add(self, *args, **kwargs):
        for key in args:
            if key not in self.__dict:
                self.__dict[key] = None
        for key in kwargs:
            self.__dict[key] = kwargs[key]

    def update(self, **kwargs):
        for key in kwargs:
            if key not in self.__dict:
                logging.warning("No var name match %s,please add it first" % key)
                continue
            self.__dict[key] = kwargs[key]

    def get(self, key):
        if key not in self.__dict:
            logging.error("No var name match %s,please add it first" % key)
            raise ValueError("No var name match %s,please add it first" % key)
        return self.__dict[key]

    def pop(self, key):
        return self.__dict.pop(key)

    def keys(self):
        return self.__dict.keys()

    def exists(self, key):
        return key in self.__dict.keys()


def get_maya_globals():
    maya_app = QtGui.qApp
    if not hasattr(maya_app, "globals"):
        maya_app.globals = MayaGlobals()
    return maya_app.globals

if __name__ == "__main__":
    pass
