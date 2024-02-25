#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Main script
"""

import argparse
import os
import display
import poem
import storage
import logging
from datetime import date
from dotenv import load_dotenv
envpath = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), ".env")
vardir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'var')
if not os.path.exists(vardir):
    os.mkdir(vardir)
logdir = os.path.join(vardir, 'log')
if not os.path.exists(logdir):
    os.mkdir(logdir)


def main():
    """
    Main entry point for the command line. Parse the arguments and call to the main process.
    :return:
    """
    args = get_arguments()

    load_dotenv(envpath)

    if bool(os.environ.get("CLOCKWORK_DEBUG")):
        logging.basicConfig(filename=f"{logdir}/app_{date.today()}.log", encoding='utf-8', level=logging.INFO)

    if args.function == "clear":
        display.clear()
    elif args.function == "intro":
        display.intro()
    elif args.function == "demo":
        display.intro()
        poem.demo()
        display.clear()
    elif args.function == "storage":
        storage.write("10:21", "Lorem ipsum")
        print(storage.read("10:21"))
    elif args.function == "display":
        print("[Info] Custom display")
        display.draw_text(args.additional, "Custom", True)
    elif args.function == "ask":
        print("[Info] Ask")
        answer = poem.ask_ai(os.environ.get("OPENAI_ASK_PROMPT"), args.additional)
        if answer:
            display.draw_text(answer, "Answer")
    else:
        poem.current_time_poem()


def get_arguments():
    """
    :return:
    """
    parser = argparse.ArgumentParser(prog='clockwork/ai',
                                     description='todo')
    parser.add_argument('function',
                        help='Additional functions to adjust the script',
                        nargs='?',
                        type=str)
    parser.add_argument('additional',
                        help='Additional arguments for function',
                        nargs='?',
                        type=str)

    return parser.parse_args()


if __name__ == "__main__":
    main()
