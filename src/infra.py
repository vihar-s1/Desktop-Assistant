#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Infra
===============

This module contains implementations for various support functions and features of the Assistant.

"""

import json
import os
import sys

from voice_interface import VoiceInterface

__CONFIG_DIR = os.path.join(os.path.abspath(__file__), "config")


def __is_windows() -> bool:
    """Returns True if the operating system is Windows"""
    return sys.platform in ["win32", "cygwin"]


def __is_darwin() -> bool:
    """Returns True if the operating system is Darwin"""
    return sys.platform in ["darwin", "ios"]


def __is_posix() -> bool:
    """Returns True if the operating system is POSIX"""
    return sys.platform in ["aix", "android", "emscripten", "linux", "darwin", "wasi"]


def __system_os() -> str:
    """Returns the name of the operating system"""
    return sys.platform


def clear_screen() -> None:
    """Clears the screen based on the operating system"""
    if __is_windows():
        os.system("cls")
    else:
        os.system("clear")


def listen(vi: VoiceInterface) -> str:
    """Listens for microphone input and return string of the input

    Returns:
        str: the query string obtained from the speech input
    """
    query = vi.listen(True)
    if query:
        print(f"User:")
        vi.speak(query)
    else:
        vi.speak("Say that again please...")
    return query


def load_json_config(config_path: str) -> dict:
    """Load Json from the configs folder

    Args:
        file_path (str): json doc path relative to config folder

    Returns:
        dict: json document deserialized as dictionary
    """
    file_path = os.path.join(__CONFIG_DIR, config_path)

    if not os.path.isfile(file_path):
        return dict()

    with open(config_path, "r") as json_doc:
        return json.load(json_doc)
