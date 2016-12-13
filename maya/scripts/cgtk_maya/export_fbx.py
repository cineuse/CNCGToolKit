#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/9/21'
# version     :
# usage       :
# notes       :

# Built-in modules

# Third-party modules
from pymel.core import *

# Studio modules

# Local modules
from safe_load_plugin import safe_load_plugin


def export_fbx(file_name, selected_mode=False,):
    # 加载插件
    safe_load_plugin("fbxmaya")
    # 导出
    if selected_mode:
        mel.eval("FBXExport -f %s -s" % file_name)
    else:
        mel.eval("FBXExport -f %s" % file_name)
