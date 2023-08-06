#!/usr/bin/env python3
import csv
import datetime
import pathlib
import re
import sys
import time
from typing import Dict, List

from .args import Args
from .prompts import user_choice, InvalidCmdPrompt, InputError
from .system import get_files
from .user import User
from .utils import cprint


def apply_feed_filter(row: List[str]) -> List[str]:
    filters_dict = get_filters_dict()
    row_dict = get_row_dict(row)
    for key, val in filters_dict.items():
        if row_dict.get(key) is None:
            continue
        match_flag = False
        for regex in val:
            if re.search(regex, row_dict[key]) is None:
                continue
            match_flag = True
            break
        if match_flag:
            return row if Args.invert() else []
    return [] if Args.invert() else row


def get_args_feeds() -> List[pathlib.Path]:
    ret_list = []
    sfeed_dir = User.settings_str("sfeed_dir")
    if sfeed_dir != "":
        for feed in Args.feed().split(","):
            if feed.startswith("/"):
                ret_list.append(pathlib.Path(feed))
            else:
                if sfeed_dir.startswith("~"):
                    ret_list.append(pathlib.Path(f"{sfeed_dir}/{feed}").expanduser())
                else:
                    ret_list.append(pathlib.Path(f"{sfeed_dir}/{feed}"))
    return ret_list


def get_feed_files() -> List[pathlib.Path]:
    if Args.feed() != "":
        return get_args_feeds()
    sfeed_dir = User.settings_str("sfeed_dir")
    if sfeed_dir == "":
        cprint("red", f"ERROR: bad setting 'sfeed_dir': {sfeed_dir}", sys.stderr)
        return []
    if sfeed_dir.startswith("~"):
        feed_dir = pathlib.Path(sfeed_dir).expanduser()
    elif not sfeed_dir.startswith("/"):
        feed_dir = pathlib.Path(pathlib.Path.home() / sfeed_dir)
    else:
        feed_dir = pathlib.Path(sfeed_dir)
    return get_files(feed_dir)


def get_feed_info(
    feed_files: List[pathlib.Path],
    sort_time: bool,
) -> List[List[str]]:
    feed_info = []
    for feed_file in feed_files:
        if not feed_file.is_file():
            cprint(
                "red",
                f"ERROR: feed is not a file: {feed_file}",
                sys.stderr,
            )
            continue
        with open(feed_file) as f:
            reader = csv.reader(
                f,
                delimiter="\t",
                quoting=csv.QUOTE_NONE,
            )
            for row in reader:
                feed_info.append(get_row_info(row, feed_file.name))
    if sort_time == True:
        feed_info = sorted(feed_info, key=lambda x: x[1], reverse=True)
    if Args.apply_filters() != "":
        feed_info = filter_feed_info(feed_info)
    return feed_info


def get_feed_links(
    feed_info: List[List[str]],
    rows: List[int],
) -> List[str]:
    links = []
    link_index = 3
    for row in rows:
        links.append(feed_info[row][link_index])
    return links


def get_filters_dict() -> Dict[str, List[str]]:
    filters_dict = {}
    for filter_file in get_filter_files():
        if not filter_file.is_file():
            cprint("yellow", f"WARNING: '{filter_file}' is not a file, skipping")
            continue
        with filter_file.open() as f:
            for line in f.readlines():
                try:
                    key, val = line.strip("\n").split("=", 1)
                except ValueError:
                    cprint(
                        "yellow", f'WARNING: "{filter_file}" badly formatted: {line}'
                    )
                    continue
                if filters_dict.get(key.rstrip()) is None:
                    filters_dict[key.rstrip()] = [val.lstrip()]
                else:
                    filters_dict[key.rstrip()].append(val.lstrip())
    return filters_dict


def get_filter_files() -> List[pathlib.Path]:
    filter_files = []
    for filter_file in Args.apply_filters().split(","):
        if filter_file.startswith("/"):
            filter_files.append(pathlib.Path(filter_file))
        else:
            filter_file_path = User.get_config_dir() + "/filter_files/" + filter_file
            filter_files.append(pathlib.Path(filter_file_path))
    return filter_files


def get_row_dict(row: List[str]) -> Dict[str, str]:
    key_list = [
        "status",
        "feed_file",
        "time",
        "title",
        "link",
        "content",
        "content_type",
        "id",
        "author",
        "enclosure",
        "category",
    ]
    return {key: value for key, value in zip(key_list, row)}


def get_row_info(row: List[str], file_name: str) -> List[str]:
    time_index = 0
    if row_is_new(int(row[time_index])):
        status = User.settings_str("new_indicator")
    else:
        status = User.settings_str("old_indicator")
    ret_list = [status, file_name]
    ret_list.extend(row)
    return ret_list


def filter_feed_info(feed_info: List[List[str]]) -> List[List[str]]:
    ret_info = []
    for row in feed_info:
        ret_row = apply_feed_filter(row)
        if ret_row == []:
            continue
        ret_info.append(ret_row)
    return ret_info


def format_feed_info(
    feed_info: List[List[str]],
    format_string: str,
    max_length: int,
) -> List[str]:
    formated_info = []
    for row in feed_info:
        formated_info.append(
            format_feed_row(
                row,
                format_string,
                max_length,
            )
        )
    return formated_info


def format_feed_row(
    row: List[str],
    format_string: str,
    max_length: int,
) -> str:
    ret_str = format_string
    format_dict = get_row_dict(row)
    format_keys = re.findall("{([^}]+)}", ret_str)
    for format_key in format_keys:
        # Check if item_key is a known key
        format_parts = format_key.split(":", 1)
        parts_flag = True if len(format_parts) == 2 else False
        if parts_flag:
            format_key = format_parts[0]
            format_fmt = format_parts[1]
        else:
            format_fmt = ""
        key_flag = True if format_key in format_dict.keys() else False
        if key_flag and not parts_flag:
            replace_str = format_dict[format_key]
        elif key_flag and parts_flag:
            if format_key == "time":
                format_str = datetime.datetime.fromtimestamp(
                    float(
                        format_dict[format_key],
                    )
                )
            else:
                format_str = format_dict[format_key]
            try:
                replace_str = f"{{:{format_fmt}}}".format(
                    format_str,
                )
            except ValueError:
                bad_fmt = f"{{{format_key}:{format_fmt}}}"
                cprint(
                    "red",
                    f"ERROR: Malfored formatting: {{{bad_fmt}}}",
                )
                replace_str = format_dict[format_key]
            ret_str = ret_str.replace(
                f"{{{format_key}:{format_fmt}}}", f"{{{format_key}}}"
            )
        else:
            format_key = f"{format_key}:{format_fmt}"
            content_str = format_dict["content"]
            replace_match = re.search(format_key, content_str)
            if replace_match is None:
                replace_str = ""
            else:
                replace_str = replace_match.group()
        if max_length != -1 and len(replace_str) > max_length:
            replace_str = replace_str[:max_length] + "..."
        ret_str = ret_str.replace(f"{{{format_key}}}", replace_str)
    return ret_str


def pick_feed_files(
    feed_files: List[pathlib.Path],
) -> List[pathlib.Path]:
    ret_list = []
    feed_list = [x.name for x in feed_files]
    loop_list = feed_list
    while True:
        if loop_list == []:
            break
        try:
            choices = user_choice(loop_list, "Pick a feed:")
        except (InvalidCmdPrompt, InputError) as err:
            cprint("red", f"ERROR: {err.message}", sys.stderr)
            return []
        if not isinstance(choices, list):
            cprint(
                "red",
                f"ERROR: got unexpected choice: {choices}",
                sys.stderr,
            )
            return []
        if choices == []:
            break
        ret_list.extend([feed_files[feed_list.index(x)] for x in choices])
        loop_list = [x for x in loop_list if x not in choices]
    return ret_list


def row_is_new(row_time: int) -> bool:
    try:
        return int(time.time()) - User.settings_int("new_time") < row_time
    except ValueError:
        cprint(
            "yellow",
            f"WARNING: value of 'new_time' is not an int: {User.settings_int('new_time')}",
        )
        return False
    # Unreachable
    return False


def store_matching_links(
    regex: str,
    links: List[str],
    store_list: List[str],
) -> None:
    for link in links:
        link_match = re.search(regex, link)
        if link_match is None:
            continue
        store_list.append(link)
