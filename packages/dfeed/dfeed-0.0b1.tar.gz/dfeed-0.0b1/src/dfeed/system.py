#!/usr/bin/env python3
import mimetypes
import os
import pathlib
import re
import requests
import subprocess
import sys
import shlex
import shutil
import time


class OpenerError(Exception):
    """Exception raised when command fails"""

    def __init__(self, error, message="ERROR: Failed to run"):
        self.error = error
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} {self.error}"


def curl_torrent(torrent_url, user):
    result = re.search(r"/(.[^/]+\.torrent$)", torrent_url)
    if result is None or len(result.groups()) == 0:
        return
    torrent_file = str(int(time.time())) + "_" + result.group(1)
    response = requests.get(torrent_url)
    with open(f'{user.settings["temp_dir"]}/{torrent_file}', "wb") as out_file:
        out_file.write(response.content)


def get_files(path: pathlib.Path):
    # list all files and directories under the given path
    entries = os.listdir(path)
    # filter out the directories
    files = [
        pathlib.Path(path, entry)
        for entry in entries
        if os.path.isfile(pathlib.Path(path, entry))
    ]
    return files


def open_process(opener, out=subprocess.DEVNULL, err=subprocess.STDOUT):
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
