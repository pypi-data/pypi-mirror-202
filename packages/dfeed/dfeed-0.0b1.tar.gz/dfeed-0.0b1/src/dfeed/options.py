#!/usr/bin/env python3
import argparse


def get_opts(prog_name="dfeed"):
    parser = argparse.ArgumentParser(
        prog=prog_name,
        description="""dmenu + sfeed""",
        allow_abbrev=False,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="""
        List feeds. Will display feeds based on your configuration.
        """,
    )
    parser.add_argument(
        "-f",
        "--feed",
        metavar="FEED",
        action="store",
        help="""
        The FEED to use for other flags such as --list.
        """,
    )
    args = parser.parse_args()
    return args
