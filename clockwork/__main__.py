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


def main():
    """
    Main entry point for the command line. Parse the arguments and call to the main process.
    :return:
    """
    args = get_arguments()

    display.intro()

    if args.function == "clear":
        display.clear()
    elif args.function == "demo":
        poem.demo()
        display.clear()
    elif args.function == "storage":
        storage.write("10:21", "Lorem ipsum")
        print(storage.read("10:21"))
    elif args.function == "display":
        print("[Info] Custom display")
        display.draw_text(args.additional, "Custom")
    elif args.function == "ask":
        print("[Info] Ask")
        poem.init()
        answer = poem.ask_ai(os.environ.get("OPENAI_ASK_PROMPT"), args.additional)
        if answer:
            display.draw_text(answer, "Answer")
    else:
        poem.init()
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
