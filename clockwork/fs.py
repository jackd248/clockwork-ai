#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import json
import random
storagedir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'var/storage')
if not os.path.exists(storagedir):
    os.makedirs(storagedir)

lockfile = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'display.lock')


def write(time, poem):

    filename = time.replace(":", "")
    hourdir = time[:2]
    filepath = f"{storagedir}/{hourdir}/{filename}.json"
    print(f"[info] Write to storage: {filepath}")
    content = []

    if not os.path.exists(f"{storagedir}/{hourdir}"):
        os.mkdir(f"{storagedir}/{hourdir}")

    if os.path.isfile(filepath):
        with open(filepath, 'r') as openfile:
            content = json.load(openfile)

    content += [poem]

    json_object = json.dumps(content, indent=4)
    with open(filepath, "w") as outfile:
        outfile.write(json_object)


def read(time):
    filename = time.replace(":", "")
    hourdir = time[:2]
    filepath = f"{storagedir}/{hourdir}/{filename}.json"
    content = None

    if os.path.isfile(filepath):
        with open(filepath, 'r') as openfile:
            content = json.load(openfile)

    if content is not None:
        return random.choice(content)

    return False


def check_lock():
    if os.path.isfile(lockfile):
        return True
    return False


def lock():
    open(lockfile, "w")


def unlock():
    if os.path.exists(lockfile):
        os.remove(lockfile)