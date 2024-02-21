#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import json
import random
vardir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'var')
if not os.path.exists(vardir):
    os.mkdir(vardir)


def write(time, poem):
    print("[Info] Write to storage")

    filename = time.replace(":", "")
    hourdir = time[:2]
    filepath = f"{vardir}/{hourdir}/{filename}.json"
    content = []

    if not os.path.exists(f"{vardir}/{hourdir}"):
        os.mkdir(f"{vardir}/{hourdir}")

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
    filepath = f"{vardir}/{hourdir}/{filename}.json"
    content = None

    if os.path.isfile(filepath):
        with open(filepath, 'r') as openfile:
            content = json.load(openfile)

    if content is not None:
        return random.choice(content)

    return False
