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


def safe_load_plugin(plugin_name):
    if not pluginInfo(plugin_name, q=1, loaded=True):
        loadPlugin(plugin_name)
