#!/usr/bin/env python3
import shlex
import sys

from .config import get_user_settings
from .sfeed import get_feeds

# from .media import
from .options import get_opts
from .system import open_process
from .utils import cprint


__license__ = "GPL-v3.0"
__program__ = "dfeed"


def process_opts(user, args):
    """
    Opts handler for main
    """
    if args.list:
        return get_feeds(user, args)
    else:
        return 1


def main():
    """
    Command line application to integrate dmenu into sfeed
    """
    # Set and get command line args
    args = get_opts(__program__)

    # Creates a UserSettings object. This will be used by various function
    # to access file paths, settings, filters, and command line args
    user, args = get_user_settings(program=__program__, args=args)

    # Execute the appropriate function based on command line options
    return process_opts(user, args=args)


if __name__ == "__main__":
    sys.exit(main())
