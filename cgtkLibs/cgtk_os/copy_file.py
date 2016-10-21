# coding=utf8
# Copyright (c) 2016 CineUse

import os
import shutil
import logging
import cgtk_log

log = cgtk_log.cgtk_log(level=logging.INFO)


def copy_file(source, destination, force=False):
    """
    Copies a file or directory from one path to another, created intermediate directories as required

    Args:
        source (basestring): file to copy from
        destination (basestring: file to copy too
        force (book): force the overwrite

    """
    log.info("Copy %s --> %s" % (source, destination))
    if not force and os.path.isfile(destination):
        log.info("destination already exists, will not overwrite")
        return

    if not os.path.isdir(os.path.dirname(destination)):
        try:
            log.info("Creating path %s", destination)
            os.makedirs(os.path.dirname(destination))
        except IOError:
            log.warning("Failed to create dir %s", destination)
    try:
        if os.path.isdir(source):
            log.info('Dir %s copy-> %s', source, destination)
            shutil.copytree(source, destination)
        else:
            log.info('File %s copy-> %s', source, destination)
            shutil.copy2(source, destination)
    except IOError:
        log.warning('File %s already exists!', destination)


if __name__ == "__main__":
    copy_file()
