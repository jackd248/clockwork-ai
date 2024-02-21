#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
import textwrap3
import time

from waveshare_epd import epd2in13_V3
from PIL import Image, ImageDraw, ImageFont

epd = None
font_size = 20
font_size_line_config = {
    24: {
        "lines": 4,
        "width": 20
    },
    20: {
        "lines": 5,
        "width": 24
    },
    16: {
        "lines": 6,
        "width": 28
    },
    12: {
        "lines": 7,
        "width": 32
    },
    8: {
        "lines": 8,
        "width": 36
    }
}


def init():
    print("[Info] Initialize display")
    global epd
    epd = epd2in13_V3.EPD()
    epd.init()


def intro():
    if epd is None:
        init()

    image = Image.new('1', (epd.height, epd.width), 255)
    font = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 24)
    draw = ImageDraw.Draw(image)
    draw.text((52, 45), 'clockwork/ai', font=font, fill=0)

    draw.line([(39, 80), (110, 80)], fill=0, width=2)
    draw.line([(44, 85), (80, 85)], fill=0, width=2)
    draw.line([(39, 80), (39, 60)], fill=0, width=2)

    draw.line([(199, 40), (150, 40)], fill=0, width=2)
    draw.line([(199, 40), (199, 60)], fill=0, width=2)
    epd.display(epd.getbuffer(image))
    time.sleep(3)


def draw_text(text):
    global font_size
    font_size = 24
    if epd is None:
        init()

    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)

    lines = splint_lines(text)
    font = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), font_size)
    y_text = 5
    for line in lines:
        width, height = font.getsize(line)
        draw.text((5, y_text), line, font=font, fill=0)
        y_text += height


    epd.display(epd.getbuffer(image))


def splint_lines(text):
    global font_size
    lines = []

    # consider line break in text
    tmp_lines = text.splitlines()
    for tmp_line in tmp_lines:
        lines += textwrap3.wrap(tmp_line, width=font_size_line_config[font_size]["width"])

    if len(lines) > font_size_line_config[font_size]["lines"]:
        font_size -= 4

        return splint_lines(text)
    return lines


def clear():
    if epd is None:
        init()

    print("[Info] Clear display")
    epd.init()
    epd.Clear(0xFF)
    epd.sleep()
