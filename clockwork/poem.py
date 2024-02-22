#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys

import openai
import random
from dotenv import load_dotenv
from datetime import datetime
import display
import time
import storage

envpath = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), ".env")

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
    print("[Info] Initialize openai client")
    global client
    load_dotenv(envpath)

    if os.environ.get("OPENAI_API_KEY") == "":
        sys.exit("[Error] Missing openai api key")

    client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )


def current_time_poem():
    print("[Info] Create current time poem")
    current_time = datetime.now().strftime("%H:%M")
    chat_completion = None

    # check if option for CLOCKWORK_REUSE is enabled and random source decision (api vs storage)
    if bool(os.environ.get("CLOCKWORK_REUSE")) and bool(random.getrandbits(1)):
        # reuse previous poems to save rate limit
        previous_poem = storage.read(current_time)
        if previous_poem:
            print("[" + current_time + "]\n" + previous_poem)
            display.draw_text(previous_poem)
            return

    poem = ask_ai(os.environ.get("OPENAI_CLOCKWORK_PROMPT"), current_time)
    if poem:
        if bool(os.environ.get("CLOCKWORK_VALIDATE")):
            poem = ask_ai(
                os.environ.get("OPENAI_CLOCKWORK_PROMPT"),
                current_time,
                poem,
                os.environ.get("OPENAI_CLOCKWORK_VALIDATION_PROMPT").replace("<current_time>", current_time)
            )

        print("[Poem] " + current_time + "\n" + poem)
        storage.write(current_time, poem)
        display.draw_text(poem, (current_time if bool(os.environ.get("CLOCKWORK_SHOW_TIME")) else False))


def ask_ai(system, user, assistant=None, validation=None):
    print("[Info] Ask AI")
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
        print("[Error] The server could not be reached")
        print(e.__cause__)
        return False
    except openai.RateLimitError as e:
        print("[Error] RateLimit reached")
        return False
    except openai.APIStatusError as e:
        print("[Error]")
        print(e.status_code)
        print(e.response)
        return False

    if chat_completion is not None:
        return chat_completion.choices[0].message.content
    return False


def demo():
    print("[Info] Demo")
    for slogan in demo_poems:
        display.draw_text(slogan, "Demo")
        time.sleep(3)
