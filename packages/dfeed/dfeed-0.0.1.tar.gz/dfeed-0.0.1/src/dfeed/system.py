#!/usr/bin/env python3
import os
import pathlib
import re
import requests
import subprocess
import time
from typing import List


class OpenerError(Exception):
    """Exception raised when command fails"""

    def __init__(self, error, message="ERROR: Failed to run"):
        self.error = error
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} {self.error}"


def curl_links(
    raw_links: List[str],
    curl_regexs: List[str],
    temp_dir: str,
) -> List[str]:
    links = []
    for link in raw_links:
        match_found = False
        for regex in curl_regexs:
            link_match = re.search(regex, link)
            if link_match is not None:
                match_found = True
                break
        if match_found:
            links.append(curl_url(link, temp_dir))
        else:
            links.append(link)
    return links


def curl_url(url: str, temp_dir: str) -> str:
    result = re.search(r"/(.[^/]+$)", url)
    if result is None or len(result.groups()) == 0:
        return url
    curl_file = str(time.time()) + "_" + result.group(1)
    response = requests.get(url)
    temp_path = pathlib.Path(temp_dir)
    if not temp_path.exists():
        temp_path.mkdir(mode=0o700, parents=True)
    with open(f"{temp_dir}/{curl_file}", "wb") as out_file:
        out_file.write(response.content)
    return f"{temp_dir}/{curl_file}"


def get_files(path: pathlib.Path) -> List[pathlib.Path]:
    # list all files and directories under the given path
    entries = os.listdir(path)
    # filter out the directories
    files = [
        pathlib.Path(path, entry)
        for entry in entries
        if os.path.isfile(pathlib.Path(path, entry))
    ]
    return files


def open_process(opener: List[str], out=subprocess.DEVNULL, err=subprocess.STDOUT):
    """Open a program with the given opener list"""
    try:
        subprocess.Popen(opener, stdout=out, stderr=err)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise OpenerError(opener)


def return_cmd(cmd):
    """
    Run a command and return the the output as a dict
    """
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    return {"stdout": stdout.decode("utf-8"), "stderr": stderr.decode("utf-8")}


def run_cmd(cmd):
    subprocess.run(cmd)
