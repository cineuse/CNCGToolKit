# coding=utf8
# Copyright (c) 2016 CineUse

import sys
import re
import subprocess
import logging
import cgtk_log

log = cgtk_log.cgtk_log(level=logging.INFO)


def path_to_unc(path):
    """
    Convert a path with a driver letter to a UNC path, so driver letters should need not be mapped

    Args:
        path (basestring):  path to convert

    Returns:
        (basestring): input path converted

    """
    if sys.platform == "win32":  # fixme: lets make it cross platform
        path = path.replace('/', '\\')
        drive_re = re.compile(r"(?P<drive>[A-Z]:) +(?P<map>\S+)")
        mappings = {}
        p = subprocess.Popen("net use",
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)
        p.wait()

        for line in p.stdout:
            search = drive_re.search(line)
            if search:
                gd = search.groupdict()
                mappings[gd['drive']] = gd['map']
        for key in mappings:
            if key in path:
                path = path.replace(key, mappings[key])
    return path


if __name__ == "__main__":
    print path_to_unc("E:\\USB/AaronWork/aas_playblast")
