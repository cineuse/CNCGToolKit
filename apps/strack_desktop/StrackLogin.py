# coding=utf8
# Copyright (c) 2016 CineUse

# temp
import sys
sys.path.append(r"E:\repos\strack_python_api\src\strack_api")
# temp-end

import logging

logger = logging.getLogger("strack_connection")


def strack_auth(url, login, api_key):
    server = strack.Strack(base_url=url, login=login, api_key=api_key)
    if server:
        return StrackLogin(login, server)
    else:
        return False


class StrackLogin(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(StrackLogin, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, name=None, strack_server=None):
        if self.__initialized:
            return
        if not (name and strack_server):
            raise RuntimeError("You must login first.")

        self.__initialized = True

        self.__name = name
        self.__strack_server = strack_server

    @property
    def name(self):
        return self.__name

    @property
    def strack_server(self):
        return self.__strack_server

    @property
    def avatar_path(self):
        # TODO: get path
        return "E:/avatar.jpg"


if __name__ == "__main__":
    StrackLogin()
