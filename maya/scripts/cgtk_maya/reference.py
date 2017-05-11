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


def reference(file_name):
    if os.path.isfile(file_name):
        name_space = os.path.splitext(os.path.basename(file_name))[0]
        return createReference(file_name, reference=True, force=True, namespace=name_space)