# coding=utf8
# Copyright (c) 2016 CineUse

import os
import logging
import cgtk_log

log = cgtk_log.cgtk_log(level=logging.INFO)


os.environ["CGTKUIPATH"] = os.path.join(os.path.dirname(__file__), "..", "uis")


if __name__ == "__main__":
    pass
