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
import logging

# Third-party modules
from pymel.core import *

# Studio modules

# Local modules
from safe_load_plugin import safe_load_plugin

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def export_abc(file_name, attrs=(), selected_mode=False, start_frame=1, end_frame=1):
    """
    export selected dag nodes to abc.
    :param file_name:
    :param attrs:
    :param selected_mode:
    :param start_frame:
    :param end_frame:
    """
    # 检测参数
    if not (isinstance(attrs, list) or isinstance(attrs, tuple)):
        log.error("TypeError: Invalid arguments for attrs. Excepted list, got {type}".format(type=type(attrs)))
    # 加载abc插件
    safe_load_plugin("AbcExport")
    # 构建导出脚本
    if selected_mode:
        all_trans = selected(assemblies=True)
    else:
        all_trans = ls(assemblies=True)
    cameras = ls(cameras=True)
    cam_trans = [listRelatives(i, parent=True)[0] for i in cameras]
    model_groups = list(set(all_trans)-set(cam_trans))
    j_string = "-frameRange {start_frame} {end_frame} -stripNamespaces -uvWrite -worldSpace \
                -writeVisibility -file {tar_path} ".format(tar_path=file_name,
                                                           start_frame=start_frame,
                                                           end_frame=end_frame)
    # -添加导出属性
    for attr in attrs:
        j_string += "-attr %s " % attr
    # -添加选中组
    for root in model_groups:
        j_string += "-root %s " % root
    # 导出
    AbcExport(j=j_string)
