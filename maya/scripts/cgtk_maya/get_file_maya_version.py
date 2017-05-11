#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/7/24'
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import re

# Third-party modules

# Studio modules

# Local modules


def get_file_maya_version(file_path):
    if os.path.isfile(file_path) and (file_path.endswith(".ma") or file_path.endswith(".mb")):
        ext = os.path.splitext(file_path)[1].lower()
        r = None
        with open(file_path) as f:
            if ext == ".ma":
                r = re.findall(r'//Maya ASCII (\d+) scene', f.readline(), re.I)
            else:
                for i in xrange(3):
                    r = re.findall(r'.+product\x00Maya (\d+).+', f.readline(), re.I)
                    if r:
                        break
        return int(r[0])

    else:
        raise ValueError('param "file_path" must aimed at a exist file.')


if __name__ == "__main__":
    pass
