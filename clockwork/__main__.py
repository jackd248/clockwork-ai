#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Main script
"""

import argparse
import display
import ai
import storage


def main():
    """
    Main entry point for the command line. Parse the arguments and call to the main process.
    :return:
    """
    args = get_arguments()

    if args.function == "intro":
        display.intro()
    elif args.function == "clear":
        display.clear()
    elif args.function == "demo":
        display.demo()
    elif args.function == "storage":
        storage.write("10:21", "Lorem ipsum")
        print(storage.read("10:21"))
    elif args.function == "time":
        ai.init()
        ai.current_time_poem()


def get_arguments():
    """
    :return:
    """
    parser = argparse.ArgumentParser(prog='clockwork',
                                     description='todo')
    parser.add_argument('function',
                        help='todo',
                        nargs='?',
                        type=str)

    return parser.parse_args()


if __name__ == "__main__":
    main()
