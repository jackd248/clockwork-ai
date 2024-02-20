import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import display
import storage

envpath = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), ".env")

prompt = "Du bist eine Uhr, welche die Zeit in einem zweizeiligen Gedicht anzeigt. Die Gedichte sollen dabei die aktuelle Uhrzeit als numerische Ziffern oder als Text beinhalten und die Anzeige der Uhrzeit auch variieren. Das Thema und der Inhalt soll abwechslungsreich sein und sich nicht wiederholen. Das Gedicht soll sich auf jeden Fall reimen, allerdings nicht mit demselben Wort. "
model = "gpt-3.5-turbo"
client = None


def init():
    logging.info("Initialize openai client")
    global client
    load_dotenv(envpath)
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )


def current_time_poem():
    current_time = datetime.now().strftime("%H:%M")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": current_time
            },
        ],
        model=model,
    )
    poem = chat_completion.choices[0].message.content
    print("[" + current_time + "]\n" + poem)
    storage.write(current_time, poem)
    display.draw_text(poem)



