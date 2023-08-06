#!/usr/bin/env python3
import os
from loadconf import Config


def get_user_settings(program, args):
    # Create user object to read files and get settings
    user = Config(program=program)
    # Define some basic settings, files, etc.
    user_settings = {
        "debug": False,
        "prompt_cmd": "fzf",
        "prompt_args": "",
        "format_list": "",
    }
    config_files = {
        "conf_file": "dfeedrc",
        "filters_file": "filters.conf",
    }
    files = [
        "conf_file",
        "filters_file",
    ]
    settings = list(user_settings.keys())
    # Fill out user object
    user.define_settings(settings=user_settings)
    user.define_files(user_files=config_files)
    user.create_files(create_files=files)
    user.read_conf(user_settings=settings, read_files=["conf_file"])
    user.store_files(files=["filters_file"])

    return user, args
