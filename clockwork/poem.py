#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys

import openai
import random
from datetime import datetime
import display
import requests
import time
import storage
import logging

client = None

demo_poems = [
    "Am Horizont, wo Lichter blüh\'n,\nzeigt die Uhr 17:17, in Abendglüh\'n.",
    "Beim Dämmerlicht, so zart und fein, \nschlägt es 17:16, der Tag neigt sich dem Sein.",
    "Die Schatten lang, der Abend naht, \n17:15, in stiller Stadt.",
    "Das Tageslicht schwindet sacht,\n17:14, die Nacht erwacht.",
    "In sanftem Licht, das Abendrot, \nzeigt 17:13, der Tag im Lot.",
    "Der Tag neigt sich, leis und mild,\num 17:12, die Welt verhüllt."
]


def init():
    global client

    if os.environ.get("OPENAI_API_KEY") == "":
        sys.exit("[error] Missing openai api key")

    client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )


def current_time_poem(override_time=None):
    logging.info("[info] Create current time poem")
    current_time = datetime.now().strftime("%H:%M") if override_time is None else override_time
    chat_completion = None

    if reuse_poem(current_time):
        return

    poem = ask_ai(os.environ.get("OPENAI_CLOCKWORK_PROMPT"), current_time)
    if poem:
        if bool(os.environ.get("CLOCKWORK_VALIDATE")):
            original_poem = poem
            new_poem = ask_ai(
                os.environ.get("OPENAI_CLOCKWORK_PROMPT"),
                current_time,
                poem,
                os.environ.get("OPENAI_CLOCKWORK_VALIDATION_PROMPT").replace("<current_time>", current_time)
            )
            if new_poem:
                poem = new_poem
                logging.info(
                    "[openai] %s (correct) //  \"%s\" --> \"%s\"",
                    current_time,
                    original_poem.replace('\r', '').replace('\n', ''),
                    poem.replace('\r', '').replace('\n', '')
                )

        logging.info(
            "[openai] %s // \"%s\"",
            current_time,
            poem.replace('\r', '').replace('\n', '')
        )
        storage.write(current_time, poem)
        display.draw_text(poem, (current_time if bool(os.environ.get("CLOCKWORK_SHOW_TIME")) else False))


def ask_ai(system, user, assistant=None, validation=None):
    if client is None:
        init()

    logging.info(
        "[openai] request: %s",
        user
    )
    messages = [
        {
            "role": "system",
            "content": system,
        },
        {
            "role": "user",
            "content": user
        },
    ]
    if assistant is not None and validation is not None:
        messages += [
            {
                "role": "assistant",
                "content": assistant,
            },
            {
                "role": "user",
                "content": validation
            },
        ]

    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=os.environ.get("OPENAI_API_MODEL"),
        )
    except openai.APIConnectionError as e:
        logging.error("The server could not be reached: %s", e.__cause__)
        return False
    except openai.RateLimitError as e:
        logging.error("RateLimit reached")
        return False
    except openai.APIStatusError as e:
        logging.error("API error (%s): %s", e.status_code, e.response)
        return False

    if chat_completion is not None:
        return chat_completion.choices[0].message.content
    return False


def reuse_poem(current_time):
    # check if option for CLOCKWORK_REUSE is enabled and random source decision (api vs storage)
    # or try to use a stored poem if internet connection is not available (offline mode)
    if (bool(os.environ.get("CLOCKWORK_REUSE")) and bool(random.getrandbits(1))) or not check_connection():
        # reuse previous poems to save rate limit
        previous_poem = storage.read(current_time)
        if previous_poem:
            logging.info(
                "[local] %s // \"%s\"",
                current_time,
                previous_poem.replace('\r', '').replace('\n', '')
            )
            display.draw_text(
                previous_poem,
                additional_text=(current_time if bool(os.environ.get("CLOCKWORK_SHOW_TIME")) else False),
                additional_hint=True)
            return True
    return False


def check_connection():
    """Detect an internet connection."""
    connection = None
    try:
        r = requests.get("https://openai.com")
        r.raise_for_status()
        connection = True
    except:
        logging.error("Internet connection not detected.")
        connection = False
    finally:
        return connection


def demo():
    print("[info] Demo")
    for slogan in demo_poems:
        display.draw_text(slogan, "Demo")
        time.sleep(4)
