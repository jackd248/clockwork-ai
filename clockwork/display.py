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
import __main__

from PIL import Image, ImageDraw, ImageFont

if not __main__.dry_run:
    from waveshare_epd import epd2in13_V3

_epd = None
_font = None
_max_char_height = None


def init():
    global _epd

    if __main__.dry_run:
        _epd = type('new', (object,), {
            "width": 122,
            "height": 250
        })
    else:
        _epd = epd2in13_V3.EPD()
        _epd.init()


def intro():
    if _epd is None:
        init()

    image = Image.new('1', (_epd.height, _epd.width), 255)
    font = ImageFont.truetype(os.path.join(fontdir, "Font.ttc"), 24)
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
    # _epd.displayPartial(_epd.getbuffer(image))
    # time.sleep(0.5)
    #
    # draw.line([(120, 80), (122, 80)], fill=0, width=2)
    # _epd.displayPartial(_epd.getbuffer(image))
    # time.sleep(0.5)
    #
    # draw.line([(125, 80), (127, 80)], fill=0, width=2)
    # _epd.displayPartial(_epd.getbuffer(image))
    # time.sleep(0.5)
    #
    # _epd.init()
    # _epd.Clear(0xFF)


def draw_text(text, additional_text=False, additional_hint=False):
    if _epd is None:
        init()

    image = Image.new('1', (_epd.height, _epd.width), 255)
    draw = ImageDraw.Draw(image)

    lines = text_box(text, image)
    y_text = 2
    for line in lines:
        draw.text((2, y_text), line, font=_font, fill=0)
        y_text += _max_char_height * 1.4

    if additional_text:
        draw.text(
            (_epd.height, _epd.width),
            str(additional_text),
            font=ImageFont.truetype(os.path.join(fontdir, "Font.ttc"), 10),
            fill=0,
            align="right",
            anchor="rb"
        )

    if additional_hint and bool(os.environ.get("CLOCKWORK_DEBUG")):
        # visual hint for reusing a stored poem
        draw.ellipse(
            [(_epd.height-4, 2), (_epd.height-2, 4)],
            fill=0
        )

    print(f"[draw] {text}")
    display(image, draw_text.__name__)


def text_box(text, image, font_size=36):
    global _font
    global _max_char_height
    lines = []

    # consider line break in text
    tmp_lines = text.splitlines()

    _font = get_font(os.environ.get("CLOCKWORK_FONT"), font_size)

    avg_char_width = sum(_font.getsize(char)[0] for char in text) / len(text)
    max_char_count = int(image.size[0] / avg_char_width) * .9
    max_char_height = max(_font.getsize(char)[0] for char in text)
    _max_char_height = max_char_height
    max_lines = int(image.size[1] / (max_char_height * 1.5)) # + line height
    for tmp_line in tmp_lines:
        lines += textwrap3.wrap(tmp_line, width=max_char_count)

    # print(f"font_size: {font_size} // lines: {lines} // max_lines: {max_lines} // char_count: {max_char_count} // char_width: {avg_char_width} // char_height: {max_char_height}")
    if len(lines) > max_lines:
        font_size -= 2

        return text_box(text, image, font_size)

    return lines


def get_font(font_name, size):
    return ImageFont.truetype(os.path.join(fontdir, font_name), size)


def display(image, name=None):
    if _epd is None:
        init()

    if __main__.dry_run:
        debugdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'var/debug')
        if not os.path.exists(debugdir):
            os.makedirs(debugdir)
        image.save(f"{debugdir}/{name}.jpg")
    else:
        _epd.display(_epd.getbuffer(image))


def clear():
    if __main__.dry_run:
        return
    if _epd is None:
        init()

    print("[info] Clear display")
    _epd.init()
    _epd.Clear(0xFF)
    _epd.sleep()
