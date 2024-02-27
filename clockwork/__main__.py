#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Main script
"""

import argparse
import os
import sys
import re
import util
import fs


def main():
    """
    Main entry point for the command line. Parse the arguments and call to the main process.
    :return:
    """
    print("### \033[1m\033[4mclockwork\033[0m\033[1m/ai\033[0m ###")
    args = get_arguments()
    util.init()

    if args.dry_run:
        util.DRY_RUN = True

    if fs.check_lock():
        print("[warning] Display is currently locked, skipping execution")
        return
    else:
        fs.lock()

    try:
        run_function(args)
    finally:
        fs.unlock()


def run_function(args):
    import display
    import poem
    override_time = None

    if args.function is not None and args.function not in util.SUPPORTED_FUNCTIONS:
        if re.match(r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$", args.function):
            override_time = args.function
        else:
            sys.exit("[error] Not supported function")

    if args.function == "clear":
        display.clear()
    elif args.function == "intro":
        display.intro()
    elif args.function == "demo":
        display.intro()
        poem.demo()
        display.clear()
    elif args.function == "display":
        print("[info] Custom display")
        display.draw_text(args.additional, "Custom", True)
    elif args.function == "ask":
        print("[info] Ask")
        answer = poem.ask_ai(os.environ.get("OPENAI_ASK_PROMPT"), args.additional)
        if answer:
            display.draw_text(answer, "Answer")
    else:
        poem.current_time_poem(override_time)


def get_arguments():
    """
    :return:
    """
    parser = argparse.ArgumentParser(prog='clockwork/ai',
                                     description='Generate ai poems by current time for displaying them on a '
                                                 'e-ink display.')
    parser.add_argument('function',
                        help='Functions to adjust the script',
                        nargs='?',
                        type=str)
    parser.add_argument('additional',
                        help='Additional arguments for function',
                        nargs='?',
                        type=str)
    parser.add_argument('-dr', '--dry-run',
                        help='Skipping drawing image to e-ink display',
                        required=False,
                        action='store_true')

    return parser.parse_args()


if __name__ == "__main__":
    main()
