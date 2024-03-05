#!/usr/bin/python
# -*- coding:utf-8 -*-
""""""
import util
import os
import sys

LIB_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(LIB_DIR):
    sys.path.append(LIB_DIR)

if not util.DRY_RUN:
    from waveshare_epd import epd7in5_V2


def init():
    """
    Initialize display
    :return:
    """
    if util.DRY_RUN:
        return type('new', (object,), {
            "width": 800,
            "height": 480
        })
    else:
        epd = epd7in5_V2.EPD()
        epd.init()
        return epd
