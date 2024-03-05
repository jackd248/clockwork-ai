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
    from waveshare_epd import epd2in13_V3


def init():
    """
    Initialize display
    :return:
    """
    if util.DRY_RUN:
        return type('new', (object,), {
            "width": 122,
            "height": 250
        })
    else:
        epd = epd2in13_V3.EPD()
        epd.init()
        return epd
