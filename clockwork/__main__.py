#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Main script
"""

import argparse
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
    else:
        poem.init()
        poem.current_time_poem()


def get_arguments():
    """
    :return:
    """
    parser = argparse.ArgumentParser(prog='clockwork',
                                     description='todo')
    parser.add_argument('function',
                        help='Additional function to test the script',
                        nargs='?',
                        type=str)

    return parser.parse_args()


if __name__ == "__main__":
    main()
