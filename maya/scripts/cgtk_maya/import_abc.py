#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/9/22'
# version     :
# usage       :
# notes       :

# Built-in modules
import os

# Third-party modules
from pymel.core import *

# Studio modules

# Local modules
from safe_load_plugin import safe_load_plugin


def import_abc(file_name):
    # 加载abc插件
    safe_load_plugin("AbcExport")

    if os.path.isfile(file_name):
        if os.path.splitext(file_name)[-1] == '.abc':
            return AbcImport(file_name)
    return False
