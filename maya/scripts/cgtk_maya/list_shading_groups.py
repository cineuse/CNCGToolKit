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


def list_shading_groups(selected_mode=True):
    shading_groups = []
    # 获取模式
    if selected_mode:
        selected_dags = [i for i in selected(dagObjects=True) if isinstance(i, (nt.NurbsSurface, nt.Mesh))]
        for dag in selected_dags:
            shading_groups.extend(dag.instObjGroups[0])
    else:
        shading_groups = ls(type='shadingEngine')
        shading_groups.remove('initialParticleSE')
        shading_groups.remove('initialShadingGroup')
    return shading_groups
