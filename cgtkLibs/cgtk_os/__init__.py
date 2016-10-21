# coding=utf8
# Copyright (c) 2016 Strack

import sys
sys.path.append("..")
sys.path.append(".../pyLibs")

from TemporaryDirectory import TemporaryDirectory

if sys.platform == 'darwin':
    from osx_modules import *
elif sys.platform == 'win32':
    from win_modules import *
elif 'linux' in sys.platform:
    from linux_modules import *
