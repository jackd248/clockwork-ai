#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
import logging
import time
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V3
from PIL import Image,ImageDraw,ImageFont


logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("hello world")
    epd = epd2in13_V3.EPD()

    font15 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 15)
    font24 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 24)

    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)

    draw.text((120, 10), 'Just a simple hello world example ...', font = font15, fill = 0)
    epd.init()
    epd.display(epd.getbuffer(image))

    time.sleep(5)

    logging.info("Clear...")
    epd.init()
    epd.Clear(0xFF)

    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)