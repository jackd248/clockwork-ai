#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import logging
import openai
from dotenv import load_dotenv
from datetime import datetime
import display
import time
import storage

envpath = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), ".env")

model = "gpt-3.5-turbo"
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
    logging.info("Initialize openai client")
    global client
    load_dotenv(envpath)
    client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )


def current_time_poem():
    current_time = datetime.now().strftime("%H:%M")
    chat_completion = None

    # reuse previous poems to save rate limit
    if bool(os.environ.get("OPENAI_PROMPT")):
        previous_poem = storage.read(current_time)
        if previous_poem:
            print("[" + current_time + "]\n" + previous_poem)
            display.draw_text(previous_poem)
            return

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": os.environ.get("OPENAI_PROMPT"),
                },
                {
                    "role": "user",
                    "content": current_time
                },
            ],
            model=model,
        )
    except openai.APIConnectionError as e:
        print("[Error] The server could not be reached")
        print(e.__cause__)
        return
    except openai.RateLimitError as e:
        print("[Error] RateLimit reached")
        return
    except openai.APIStatusError as e:
        print("[Error]")
        print(e.status_code)
        print(e.response)
        return

    if chat_completion is not None:
        poem = chat_completion.choices[0].message.content
        print("[" + current_time + "]\n" + poem)
        storage.write(current_time, poem)
        display.draw_text(poem)


def demo():
    logging.info('Demo')
    for slogan in demo_poems:
        logging.info('Demo')
        display.draw_text(slogan)
        time.sleep(3)
