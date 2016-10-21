# coding=utf8

from types import MethodType


def implant_method(obj, func, func_name):
    base_class = obj.__class__
    event = MethodType(func, obj, base_class)
    setattr(obj, func_name, event)


if __name__ == "__main__":
    pass
