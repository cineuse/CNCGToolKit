#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/9/25'
# version     :
# usage       :
# notes       :

# Built-in modules

# Third-party modules
from pymel.core import *

# Studio modules

# Local modules


def clear_useless_anim_curves(anim_curves=None):
    if not anim_curves:
        anim_curves = ls(type="animCurve")
    for anim_curve in anim_curves:
        anim_curve = PyNode(anim_curve)
        # 删除只有一个关键点的动画曲线
        if anim_curve.numKeyframes() <= 1:
            delete(anim_curve)
            continue
        # 删除完全水平的动画曲线
        # -判断值是否有变化
        value_set = set([anim_curve.getValue(i) for i in xrange(anim_curve.numKeyframes())])
        is_same_value = len(value_set) == 1
        # -判断手柄是否水平
        is_horizontal = sum(keyTangent(anim_curve, q=True, ia=True, oa=True)) == 0
        if is_same_value and is_horizontal:
            delete(anim_curve)