# coding=utf8
# Copyright (c) 2016 CineUse

import os
import shutil
import logging
import cgtk_log

log = cgtk_log.cgtk_log(level=logging.INFO)


def delete_folder(src):
    """
    Deletes all files from inside a folder

    .. warning::
         This will delete all files in the folder specified

    Args:
        src (basestring): directory to clean

    """
    if os.path.isfile(src):
        try:
            os.remove(src)
            log.info(src)
        except IOError:
            pass
    elif os.path.isdir(src):
        try:
            shutil.rmtree(src)
            log.info(src)
        except IOError:
            for roots, dirs, files in os.walk(src):
                for d in dirs:
                    itemsrc = os.path.join(roots, d)
                    for f in os.listdir(itemsrc):
                        itemfile = os.path.join(itemsrc, f)
                        try:
                            delete_folder(itemfile)
                        except IOError:
                            pass


if __name__ == "__main__":
    delete_folder(r"E:\temp\needclear")
