#!/usr/bin/env python3
import json
import pathlib
import re
import sys
from os.path import join as os_join
from .system import get_files


def cprint(color: str, string, out_file=sys.stdout):
    """
    Red: \033[31m
    Green: \033[32m
    Yellow: \033[33m
    Blue: \033[34m
    Magenta: \033[35m
    Cyan: \033[36m
    """
    format = ""
    end = "\033[0m"
    if color.lower() == "red":
        format = "\033[31m"
    elif color.lower() == "green":
        format = "\033[32m"
    elif color.lower() == "yellow":
        format = "\033[33m"
    elif color.lower() == "blue":
        format = "\033[34m"
    elif color.lower() == "magenta":
        format = "\033[35m"
    elif color.lower() == "cyan":
        format = "\033[36m"
    else:
        print(string, file=out_file)
        return
    print(format + string + end, file=out_file)


def key_value_list(dic, search_key=None):
    """
    Take a dicionary and return two lists one for keys and one for values
    """
    # While it is easiest if dic is a true dict
    # it need not be. As long as the items in dic
    # _are_ true dicts then we can make do
    def psuedo_dic():
        for item in dic:
            if isinstance(item, dict):
                true_dic(item)

    def true_dic(d=dic):
        if search_key is None:
            keys.extend(d.keys())
            values.extend(d.values())
        else:
            for key, value in d.items():
                if key == search_key:
                    keys.append(key)
                    values.append(value)

    keys = []
    values = []
    if isinstance(dic, dict):
        true_dic()
    else:
        psuedo_dic()

    return keys, values


def join(a, b):
    return os_join(a, b)


def pad_string(string: str):
    # convert input string to float, then back to string with 1 decimal place
    converted_string = "{:.1f}".format(float(string))
    # pad the string with zeros on the left to make it 3 characters long
    padded_string = converted_string.zfill(5)
    return padded_string
