# coding=utf8
# Copyright (c) 2016 CineUse

import os
import sys
import subprocess
import logging
import cgtk_log

log = cgtk_log.cgtk_log(level=logging.INFO)


def start(file_path):
    """
    Uses to the default OS software defined tool to 'open/start' a path

    Args:
        file_path (basestring): path to open

    """
    cmd = "cmd /c start "
    if sys.platform == "darwin":
        cmd = "open "
    elif sys.platform == "linux2":
        cmd = "xdg-open "
    else:
        file_path = file_path.replace('/', '\\')
        if os.path.isfile(file_path):
            os.startfile(file_path)
            return
    command = (cmd + file_path)
    log.info("running command %s", command)
    subprocess.Popen(command, shell=True)


if __name__ == "__main__":
    start("e:/hello_world.py")
