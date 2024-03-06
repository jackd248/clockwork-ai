#!/usr/bin/python
# -*- coding:utf-8 -*-

"""Module providing a function for accessing the filesystem."""

import os
import datetime
import json
import random
storagedir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'var/storage')
if not os.path.exists(storagedir):
    os.makedirs(storagedir)

lockfile = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'display.lock')


def write(time, poem):
    """
    Write poem to time file
    :param time:
    :param poem:
    :return:
    """
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
    """
    Read poems from time file
    :param time:
    :return:
    """
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
    """
    Check if lock file is present and is not older then 5 minutes
    :return:
    """
    if os.path.isfile(lockfile):
        if check_file_expired(lockfile):
            unlock()
            return False
        else:
            return True
    return False


def check_file_expired(file_path, expired_threshold=300):
    """
    Check if file is older then an expired threshold
    """
    if not os.path.exists(file_path):
            return False

    last_modified_time = os.path.getmtime(file_path)
    last_modified_datetime = datetime.datetime.fromtimestamp(last_modified_time)
    time_difference = datetime.datetime.now() - last_modified_datetime
    if time_difference.total_seconds() > expired_threshold:
        return True
    else:
        return False


def lock():
    """
    Create lock file
    :return:
    """
    open(lockfile, "w")


def unlock():
    """
    Delete lock file
    :return:
    """
    if os.path.exists(lockfile):
        os.remove(lockfile)
