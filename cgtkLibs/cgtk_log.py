# coding=utf8
# Copyright (c) 2016 Strack

import os
import sys
import logging
import logging.handlers

LOG_FILE = os.path.join(os.environ.get("TMP"), 'CNCGToolkit.log')


def cgtk_log(logger_name=None, level=logging.DEBUG,
             log_format='%(asctime)s - %(name)s - %(filename)s:%(lineno)s - %(message)s'):
    if not logger_name:
        logger_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler

    formatter = logging.Formatter(log_format)  # 实例化formatter
    handler.setFormatter(formatter)  # 为handler添加formatter

    logger = logging.getLogger(logger_name)  # 获取名为tst的logger
    logger.addHandler(handler)  # 为logger添加handler
    logger.setLevel(level)
    return logger


if __name__ == "__main__":
    test_log = cgtk_log()
    test_log.debug("test debug")
    test_log.info("test info")
    test_log.warning("test warning")
    test_log.error("test error")
    test_log.critical("test critical")
