#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
import logging
import time
import textwrap3

slogans = [
    'Am Horizont, wo Lichter blüh\'n,\nzeigt die Uhr 17:17, in Abendglüh\'n.',
    'Beim Dämmerlicht, so zart und fein, \nschlägt es 17:16, der Tag neigt sich dem Sein.',
    'Die Schatten lang, der Abend naht, \n17:15, in stiller Stadt.',
    'Das Tageslicht schwindet sacht,\n17:14, die Nacht erwacht.',
    'In sanftem Licht, das Abendrot, \nzeigt 17:13, der Tag im Lot.',
    'Der Tag neigt sich, leis und mild,\num 17:12, die Welt verhüllt.'
]

fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V3
from PIL import Image, ImageDraw, ImageFont


def intro(epd):
    image = Image.new('intro', (epd.height, epd.width), 255)
    font = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 18)
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), 'clockwork/1', font=font, fill=0)
    epd.display(epd.getbuffer(image))


def draw_text(image, text, width=20, size=24):
    draw = ImageDraw.Draw(image)
    lines = textwrap3.wrap(text, width=width)

    if len(lines) > 4:
        lines = textwrap3.wrap(text, width=25)
        font = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 20)
    else:
        font = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), size)

    y_text = 5
    for line in lines:
        width, height = font.getsize(line)
        draw.text((5, y_text), line, font=font, fill=0)
        y_text += height


def main():
    logging.basicConfig(level=logging.INFO)

    try:
        logging.info("hello world")
        epd = epd2in13_V3.EPD()
        epd.init()

        intro(epd)

        for slogan in slogans:
            logging.info('new slogan')
            image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
            draw_text(image, slogan)
            epd.displayPartial(epd.getbuffer(image))
            time.sleep(2)

        logging.info("Clear...")
        epd.init()
        epd.Clear(0xFF)

        logging.info("Goto Sleep...")
        epd.sleep()

    except IOError as e:
        logging.info(e)


if __name__ == "__main__":
    main()
