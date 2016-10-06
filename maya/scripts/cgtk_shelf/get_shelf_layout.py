# coding=utf8
# Copyright (c) 2016 CineUse

import pymel.core as pm
import logging
import cgtk_log

log = cgtk_log.cgtk_log(level=logging.INFO)


def get_shelf_layout():
    for shelfPrLayout in pm.lsUI(type='tabLayout'):
        return shelfPrLayout.shortName()
    log.warning("no shelf layout found.")
    return None


if __name__ == "__main__":
    get_shelf_layout()
