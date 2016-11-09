#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : aas_repos_get_current_camera
# description : ''
# author      : Aaron Hui
# date        : 2016/1/14
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import logging

# Third-party modules
import pymel.core as pm

# Studio modules

# Local modules


logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'aas_repos_get_current_camera_log.txt'),
                    level=logging.WARN, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')


def get_current_camera():
    current_cam = pm.PyNode(pm.modelPanel(pm.getPanel(wf=True), q=True, cam=True))
    return current_cam


if __name__ == "__main__":
    pass
