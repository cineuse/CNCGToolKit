# coding=utf8
# Copyright (c) 2016 CineUse

import sys
import logging
import cgtk_log

log = cgtk_log.cgtk_log(level=logging.INFO)

sys.path.append(r"E:\repos\strack_python_api\src\strack_api")
import strack


def get_strack_server():
    return strack.Strack(base_url="http://172.16.1.168/strack",
                         login="aaron", api_key="0924761d-a2dc-416f-afa6-3eb60ce6dcee")


if __name__ == "__main__":
    get_strack_server()
