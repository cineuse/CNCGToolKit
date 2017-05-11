#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/9/25'
# version     :
# usage       :
# notes       :

# Built-in modules

# Third-party modules
try:
    import PyQt4.QtCore as QtCore
except ImportError:
    import PySide.QtCore as QtCore

# Studio modules

# Local modules


def safe_to_string(value):
    """
    Safely convert the value to a string - handles
    unicode and QtCore.QString if using PyQt

    :param value:    The value to convert to a string
    :returns str:    utf8 encoded string of the input value
    """
    if isinstance(value, str):
        # it's a string anyway so just return
        return value

    if isinstance(value, unicode):
        # convert to utf-8
        return value.encode("utf8")

    if hasattr(QtCore, "QString"):
        # running PyQt!
        if isinstance(value, QtCore.QString):
            # QtCore.QString inherits from str but supports
            # unicode, go figure!  Lets play safe and return
            # a utf-8 string
            return str(value.toUtf8())

    # For everything else, just return as string
    return str(value)
