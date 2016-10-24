# coding=utf8
# Copyright (c) 2016 CineUse

import os
import sys


current_dir = os.path.dirname(__file__)
APPS_PATH = os.path.dirname(current_dir)
PROJECT_PATH = os.path.dirname(APPS_PATH)
PYLIBS_PATH = os.path.join(PROJECT_PATH, "pyLibs")
LIBS_PATH = os.path.join(PROJECT_PATH, "cgtkLibs")
sys.path.append(os.path.join(APPS_PATH, "images"))
sys.path.append(APPS_PATH)
sys.path.append(PYLIBS_PATH)
sys.path.append(LIBS_PATH)


os.environ["CGTKUIPATH"] = os.path.join(os.path.dirname(__file__), "..", "..", "uis")


if __name__ == "__main__":
    pass
