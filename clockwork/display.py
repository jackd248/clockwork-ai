#!/usr/bin/python
# -*- coding:utf-8 -*-
"""Module providing a function for display text on a epd screen."""

import os
import sys
import time
import textwrap3
from PIL import Image, ImageDraw, ImageFont
import util

FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
LIB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(LIB_DIR):
    sys.path.append(LIB_DIR)

if not util.DRY_RUN:
    from waveshare_epd import epd2in13_V3

EPD = None
FONT = None
MAX_CHAR_HEIGHT = None


def init():
    """
    Initialize display
    :return:
    """
    global EPD

    if util.DRY_RUN:
        EPD = type('new', (object,), {
            "width": 122,
            "height": 250
        })
    else:
        EPD = epd2in13_V3.EPD()
        EPD.init()


def intro():
    """
    Show intro image
    :return:
    """
    if EPD is None:
        init()

    image = Image.new('1', (EPD.height, EPD.width), 255)
    font = ImageFont.truetype(os.path.join(FONT_DIR, "Font.ttc"), 24)
    draw = ImageDraw.Draw(image)
    draw.text((52, 45), 'clockwork/ai', font=font, fill=0)

    draw.line([(39, 80), (110, 80)], fill=0, width=2)
    draw.line([(44, 85), (80, 85)], fill=0, width=2)
    draw.line([(39, 80), (39, 60)], fill=0, width=2)

    draw.line([(199, 40), (150, 40)], fill=0, width=2)
    draw.line([(199, 40), (199, 60)], fill=0, width=2)
    display(image, intro.__name__)

    time.sleep(2)

    # time.sleep(0.5)
    #
    # draw.line([(115, 80), (117, 80)], fill=0, width=2)
    # EPD.displayPartial(EPD.getbuffer(image))
    # time.sleep(0.5)
    #
    # draw.line([(120, 80), (122, 80)], fill=0, width=2)
    # EPD.displayPartial(EPD.getbuffer(image))
    # time.sleep(0.5)
    #
    # draw.line([(125, 80), (127, 80)], fill=0, width=2)
    # EPD.displayPartial(EPD.getbuffer(image))
    # time.sleep(0.5)
    #
    # EPD.init()
    # EPD.Clear(0xFF)


def draw_text(text, additional_text=False, additional_hint=False):
    """
    Draw text on display
    :param text:
    :param additional_text:
    :param additional_hint:
    :return:
    """
    if EPD is None:
        init()

    image = Image.new('1', (EPD.height, EPD.width), 255)
    draw = ImageDraw.Draw(image)

    lines = text_box(text, image)
    y_text = 2
    for line in lines:
        draw.text((2, y_text), line, font=FONT, fill=0)
        y_text += MAX_CHAR_HEIGHT * 1.4

    if additional_text:
        draw.text(
            (EPD.height, EPD.width),
            str(additional_text),
            font=ImageFont.truetype(os.path.join(FONT_DIR, "Font.ttc"), 10),
            fill=0,
            align="right",
            anchor="rb"
        )

    if additional_hint and bool(os.environ.get("CLOCKWORK_DEBUG")):
        # visual hint for reusing a stored poem
        draw.ellipse(
            [(EPD.height-4, 2), (EPD.height-2, 4)],
            fill=0
        )

    print(f"[draw] {text}")
    display(image, draw_text.__name__)


def text_box(text, image, font_size=36):
    """
    Calculate a fitting text box for the desired display size
    :param text:
    :param image:
    :param font_size:
    :return:
    """
    global FONT
    global MAX_CHAR_HEIGHT
    lines = []

    # consider line break in text
    tmp_lines = text.splitlines()

    FONT = get_font(os.environ.get("CLOCKWORK_FONT"), font_size)

    avg_char_width = sum(FONT.getsize(char)[0] for char in text) / len(text)
    max_char_count = int(image.size[0] / avg_char_width * .9)
    max_char_height = max(FONT.getsize(char)[0] for char in text)
    MAX_CHAR_HEIGHT = max_char_height
    max_lines = int(image.size[1] / (max_char_height * 1.5)) # + line height

    for tmp_line in tmp_lines:
        lines += textwrap3.wrap(tmp_line, width=max_char_count)

    # print(f"font_size: {font_size} // lines: {lines} // max_lines: {max_lines} // "
    #       f"char_count: {max_char_count}  // char_width: {avg_char_width} // char_height: {max_char_height}")
    if len(lines) > max_lines:
        font_size -= 2

        return text_box(text, image, font_size)

    return lines


def get_font(font_name, size):
    """
    Get local font
    :param font_name:
    :param size:
    :return:
    """
    return ImageFont.truetype(os.path.join(FONT_DIR, font_name), size)


def display(image, name=None):
    """
    Display the image on the screen or save them as image
    :param image:
    :param name:
    :return:
    """
    if EPD is None:
        init()

    if util.DRY_RUN:
        debugdir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
            'var/debug'
        )
        if not os.path.exists(debugdir):
            os.makedirs(debugdir)
        image.save(f"{debugdir}/{name}.jpg")
    else:
        EPD.display(EPD.getbuffer(image))


def clear():
    """
    Clear the display
    :return:
    """
    if util.DRY_RUN:
        return
    if EPD is None:
        init()

    print("[info] Clear display")
    EPD.init()
    EPD.Clear(0xFF)
    EPD.sleep()
