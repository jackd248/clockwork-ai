#!/usr/bin/python
# -*- coding:utf-8 -*-

"""Module providing a function for utilities."""

import os
import logging
from dotenv import load_dotenv
from datetime import date

__homepage__ = "https://github.com/jackd248/clockwork-ai"
__version__ = "1.0.0"

ENV_PATH = None
VAR_DIR = None
LOG_DIR = None
# Dry run mode to prevent display image on e-ink display
DRY_RUN = False
SUPPORTED_FUNCTIONS = ["clear", "intro", "demo", "display", "ask"]


def init():
    """
    Initialize app
    :return:
    """
    global ENV_PATH
    global VAR_DIR
    global LOG_DIR
    ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), ".env")
    VAR_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'var')
    if not os.path.exists(VAR_DIR):
        os.mkdir(VAR_DIR)
    LOG_DIR = os.path.join(VAR_DIR, 'log')
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)

    load_dotenv(ENV_PATH)

    if bool(os.environ.get("CLOCKWORK_DEBUG")):
        logging.basicConfig(filename=f"{LOG_DIR}/app_{date.today()}.log", encoding='utf-8', level=logging.INFO)

