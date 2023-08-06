#!/usr/bin/env python3
from promptx import PromptX
from .utils import cprint


class InvalidCmdPrompt(Exception):
    """Exception raised when user has invalid command prompt"""

    def __init__(self, error, message="ERROR: prompt_cmd not recognized"):
        self.error = error
        self.message = message

    def __str__(self):
        return f'{self.message} "{self.error}"'


class InputError(Exception):
    """Exception fzf or dmenu prompt fails"""

    def __init__(self, error, message="ERROR: Could not get user input", prefix=""):
        self.error = error
        self.prefix = prefix
        self.message = message

    def __str__(self):
        return f"{self.prefix}{self.message}{self.error}"


def user_choice(
    options,
    user,
    prompt,
):
    """
    Give user a prompt to choose from a list of options.  Uses dmenu, fzf, or
    rofi
    """
    cmd = user.settings["prompt_cmd"]
    cmd_args = user.settings["prompt_args"]
    p = PromptX(prompt_cmd=cmd)
    if cmd == "dmenu" and cmd_args == "":
        cmd_args = "-l 20 -i"

    choice = p.ask(
        options=options,
        prompt=prompt,
        additional_args=cmd_args,
    )

    return choice
