# coding=utf8
# Copyright (c) 2016 CineUse

import os
import logging
import cgtk_log

log = cgtk_log.cgtk_log(level=logging.INFO)


def touch(filename):
    """
    As unix system touch, create a file if it does not exist, and update is mtime if it does.

    Args:
        filename (basestring): path to the file to be updated
    """
    try:
        os.utime(filename, None)
    except OSError:
        open(filename, 'a').close()


if __name__ == "__main__":
    touch("e:/hello_world.py")
