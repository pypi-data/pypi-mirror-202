#!/usr/bin/env python3
import pathlib

from .system import get_files
from .utils import cprint


def get_feeds(user, args):
    feed_dir = pathlib.Path(pathlib.Path.home() / ".sfeed/feeds")
    feed_files = get_files(feed_dir)
    for file in feed_files:
        cprint("green", f"Got feed_files: {file}")
    return 0
    return get_files(feed_dir)
