#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
import time
from waveshare_epd import epd2in13_V3
from PIL import Image,ImageDraw,ImageFont


logging.basicConfig(level=logging.DEBUG)

logging.info("hello world")
epd = epd2in13_V3.EPD()

image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
draw = ImageDraw.Draw(image)

draw.text((120, 60), 'Just a simple hello world example')

time.sleep(5)

logging.info("Clear...")
epd.init()
epd.Clear(0xFF)

logging.info("Goto Sleep...")
epd.sleep()