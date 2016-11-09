#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/9/21'
# version     :
# usage       :
# notes       :

# Built-in modules

# Third-party modules
from pymel.core import *

# Studio modules

# Local modules


def get_selected_channels():
    channel_box = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')  # fetch maya's main channel box
    attrs = channelBox(channel_box, q=True, sma=True)
    if not attrs:
        return []
    return attrs
