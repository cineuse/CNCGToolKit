# coding=utf8
# Copyright (c) 2016 CineUse

import logging
import cgtk_log

log = cgtk_log.cgtk_log(level=logging.INFO)


def nonAscii_to_utf(str_):
    return str_.encode('utf-8').decode('utf-8')


if __name__ == "__main__":
    print nonAscii_to_utf("你好")
