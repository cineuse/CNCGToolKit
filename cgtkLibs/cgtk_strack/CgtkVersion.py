# coding=utf8
# Copyright (c) 2016 CineUse

import os
import logging

import cgtk_log

log = cgtk_log.cgtk_log(level=logging.INFO)


class CgtkVersion(object):

    @classmethod
    def list_versions(cls):
        # todo: list all versions of this task
        pass

    @property
    def work_path(self):
        # todo: get work path
        return

    @property
    def publish_path(self):
        # todo: get publish path
        return

    @property
    def virtual_work_file(self):
        # todo: return first version path
        return

    def register(self):
        # todo: register to strack or shotgun, I need get api obj first
        pass

    def make_dir(self):
        if self.work_path:
            os.makedirs(os.path.dirname(self.work_path))

if __name__ == "__main__":
    CgtkVersion()
