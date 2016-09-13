# coding=utf8
# Copyright (c) 2016 Strack
import sys
import os
import glob
import logging
import pymel.core as pm
import cgtk_log

log = cgtk_log.cgtk_log(level=logging.INFO)
log.info("CGTK_Maya initializing...")


PROJECT_ROOT_NAME = "CNCGToolKit"
MODULE_PATH = pm.getModulePath(moduleName=PROJECT_ROOT_NAME)
# find the root dir path
# todo: I hate this shit
root_path = os.path.join(MODULE_PATH.split(PROJECT_ROOT_NAME)[0], PROJECT_ROOT_NAME)
# add pyLibs path to env
pyLibs_path = os.path.join(root_path, "pyLibs")
egg_list = glob.glob(r"%s\*.egg" % pyLibs_path)
for egg_path in egg_list:
    log.debug("Add %s into PYTHONPATH." % egg_path)
    sys.path.append(egg_path)
log.info("Add all modules from pyLibs to PYTHONPATH Done.")
log.info("CGTK_Maya initialized...")
