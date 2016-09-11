# coding=utf8
# Copyright (c) 2016 Strack

import sys
import os
import glob
import pymel.core as pm
import cgtk_log

log = cgtk_log.cgtk_log()
log.info("CGTK_Maya initializing...")


MODULE_PATH = pm.getModulePath(moduleName="CNCGToolKit")
PROJECT_ROOT_NAME = "CNCGToolKit"
# find the root dir path
root_path = os.path.join(MODULE_PATH.split(PROJECT_ROOT_NAME)[0], PROJECT_ROOT_NAME)
# add pyLibs path to env
pyLibs_path = os.path.join(root_path, "pyLibs")
log.debug("Add %s into PYTHONPATH." % pyLibs_path)
sys.path.append(pyLibs_path)
module_path_list = glob.glob(r"%s\*" % pyLibs_path)
for module_path in module_path_list:
    if module_path.endswith(".egg"):
        log.debug("Add %s into PYTHONPATH." % module_path)
        sys.path.append(module_path)
log.info("Add all modules from pyLibs to PYTHONPATH Done.")
log.info("CGTK_Maya initialized...")
